"""Financial document generation engine."""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime


DOCUMENT_TYPE_PREFIX = {
    "invoice": "INV",
    "bill": "BILL",
    "voucher": "VCH",
    "receipt": "RCT",
    "payment_order": "PO",
    "purchase_invoice": "PI",
    "sales_invoice": "SI",
    "credit_note": "CN",
    "debit_note": "DN",
    "journal_voucher": "JV",
    "cash_voucher": "CV",
    "bank_voucher": "BV",
}

SIGNING_SECRET = "marpich-financial-doc-signing-v1"


def generate_document_number(document_type: str, sequence: int) -> str:
    prefix = DOCUMENT_TYPE_PREFIX.get(document_type, "FD")
    year = datetime.now(UTC).year
    return f"{prefix}-{year}-{sequence:06d}"


def checksum_content(content: dict) -> str:
    import json

    payload = json.dumps(content, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_pdf(document: dict) -> str:
    """Return base64-encoded minimal valid PDF for a financial document."""
    lines = [
        f"Document: {document.get('document_number', '')}",
        f"Type: {document.get('document_type', '')}",
        f"Date: {document.get('created_at', datetime.now(UTC).isoformat())}",
        f"Counterparty: {document.get('counterparty_name', '')}",
        f"Amount: {document.get('currency', 'USD')} {document.get('total_amount', 0):.2f}",
        f"Reference: {document.get('reference', '')}",
        "",
        "Line Items:",
    ]
    for line in document.get("lines", []):
        desc = line.get("description", "")
        qty = line.get("quantity", 1)
        unit = line.get("unit_price", 0)
        amount = line.get("amount", qty * unit)
        lines.append(f"  - {desc}: {qty} x {unit:.2f} = {amount:.2f}")

    text = "\n".join(lines)
    stream = f"BT /F1 10 Tf 50 750 Td ({_escape_pdf_text(text)}) Tj ET"
    stream_bytes = stream.encode("latin-1", errors="replace")

    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        (
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        ),
        f"4 0 obj << /Length {len(stream_bytes)} >> stream\n".encode()
        + stream_bytes
        + b"\nendstream endobj\n",
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
    ]

    pdf = b"%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj

    xref_start = len(pdf)
    pdf += f"xref\n0 {len(offsets)}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        pdf += f"{offset:010d} 00000 n \n".encode()

    pdf += (
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF\n"
    ).encode()

    return base64.b64encode(pdf).decode("ascii")


def generate_qr_token(*, document_id: str, version_number: int, checksum: str, tenant_id: str) -> str:
    payload = f"{tenant_id}:{document_id}:{version_number}:{checksum}"
    sig = hmac.new(SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:24]
    raw = f"{payload}:{sig}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def verify_qr_token(token: str) -> dict | None:
    try:
        padded = token + "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(padded.encode()).decode()
        parts = raw.rsplit(":", 1)
        if len(parts) != 2:
            return None
        payload, sig = parts
        expected = hmac.new(SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:24]
        if not hmac.compare_digest(sig, expected):
            return None
        tenant_id, document_id, version_number, checksum = payload.split(":", 3)
        return {
            "tenant_id": tenant_id,
            "document_id": document_id,
            "version_number": int(version_number),
            "checksum": checksum,
            "valid": True,
        }
    except (ValueError, UnicodeDecodeError):
        return None


def sign_document(*, document_id: str, version_checksum: str, signer_id: str, algorithm: str = "RS256") -> dict:
    payload = f"{document_id}:{version_checksum}:{signer_id}"
    signature = hmac.new(SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return {
        "signer_id": signer_id,
        "algorithm": algorithm,
        "signature": signature,
        "signed_at": datetime.now(UTC).isoformat(),
        "document_id": document_id,
        "version_checksum": version_checksum,
    }


def requires_approval(document_type: str) -> bool:
    return document_type in {
        "journal_voucher",
        "cash_voucher",
        "bank_voucher",
        "payment_order",
        "purchase_invoice",
        "sales_invoice",
        "credit_note",
        "debit_note",
    }


def new_workflow_id() -> str:
    return f"wf-fin-doc-{secrets.token_hex(8)}"
