#!/usr/bin/env python3
"""Minimal S3-compatible PUT/GET/LIST (SigV4). No boto3/aws CLI required.

Env:
  AWS_ACCESS_KEY_ID / MEOS_S3_ACCESS_KEY
  AWS_SECRET_ACCESS_KEY / MEOS_S3_SECRET_KEY
  MEOS_S3_ENDPOINT_URL  (MinIO / S3-compatible; empty = AWS)
  AWS_REGION            (default us-east-1)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def _creds() -> tuple[str, str]:
    key = os.environ.get("AWS_ACCESS_KEY_ID") or os.environ.get("MEOS_S3_ACCESS_KEY") or ""
    secret = os.environ.get("AWS_SECRET_ACCESS_KEY") or os.environ.get("MEOS_S3_SECRET_KEY") or ""
    if not key or not secret:
        raise SystemExit("FAIL: set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY (or MEOS_S3_* )")
    return key, secret


def parse_s3_uri(uri: str) -> tuple[str, str]:
    if not uri.startswith("s3://"):
        raise SystemExit(f"FAIL: expected s3:// URI, got {uri!r}")
    rest = uri[5:]
    bucket, _, key = rest.partition("/")
    if not bucket:
        raise SystemExit("FAIL: missing bucket in S3 URI")
    return bucket, key


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _signing_key(secret: str, datestamp: str, region: str) -> bytes:
    k_date = _sign(("AWS4" + secret).encode("utf-8"), datestamp)
    k_region = hmac.new(k_date, region.encode("utf-8"), hashlib.sha256).digest()
    k_service = hmac.new(k_region, b"s3", hashlib.sha256).digest()
    return hmac.new(k_service, b"aws4_request", hashlib.sha256).digest()


def _request(
    method: str,
    bucket: str,
    key: str,
    *,
    body: bytes = b"",
    query: dict[str, str] | None = None,
) -> bytes:
    access, secret = _creds()
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    endpoint = (os.environ.get("MEOS_S3_ENDPOINT_URL") or "").rstrip("/")
    if key:
        path_key = "/" + "/".join(urllib.parse.quote(p, safe="") for p in key.split("/") if p)
    else:
        path_key = ""
    if endpoint:
        host = urllib.parse.urlparse(endpoint).netloc
        url_path = f"/{bucket}{path_key}"
        url = f"{endpoint}{url_path}"
    else:
        host = f"{bucket}.s3.{region}.amazonaws.com"
        url_path = path_key or "/"
        url = f"https://{host}{url_path}"
        base = f"https://{host}"
    if query:
        url = url + "?" + urllib.parse.urlencode(query)
    now = dt.datetime.now(dt.UTC)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(body).hexdigest()
    canonical_query = urllib.parse.urlencode(sorted((query or {}).items()))
    canonical_headers = f"host:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    canonical_request = "\n".join(
        [method, url_path, canonical_query, canonical_headers, signed_headers, payload_hash]
    )
    credential_scope = f"{datestamp}/{region}/s3/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    signature = hmac.new(
        _signing_key(secret, datestamp, region),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    auth = (
        f"AWS4-HMAC-SHA256 Credential={access}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    req = urllib.request.Request(
        url,
        data=body if method in {"PUT", "POST"} else None,
        method=method,
        headers={
            "Authorization": auth,
            "x-amz-date": amz_date,
            "x-amz-content-sha256": payload_hash,
            "Host": host,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"FAIL: S3 {method} {url} -> {exc.code} {detail[:500]}") from exc


def cmd_put(src: str, dest_uri: str) -> None:
    bucket, key = parse_s3_uri(dest_uri)
    if not key or key.endswith("/"):
        key = key.rstrip("/") + "/" + os.path.basename(src)
        dest_uri = f"s3://{bucket}/{key}"
    with open(src, "rb") as f:
        body = f.read()
    _request("PUT", bucket, key, body=body)
    print(f"PUT {src} → {dest_uri} ({len(body)} bytes)")


def cmd_get(src_uri: str, dest: str) -> None:
    bucket, key = parse_s3_uri(src_uri)
    data = _request("GET", bucket, key)
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    print(f"GET {src_uri} → {dest} ({len(data)} bytes)")


def cmd_ls(uri: str) -> None:
    bucket, prefix = parse_s3_uri(uri)
    body = _request(
        "GET",
        bucket,
        "",
        query={"list-type": "2", "prefix": prefix},
    )
    root = ET.fromstring(body)
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"
    keys = [el.text or "" for el in root.findall(f".//{ns}Key")]
    if not keys:
        print(f"(empty) {uri}")
        return
    for k in keys:
        print(f"s3://{bucket}/{k}")


def main(argv: list[str]) -> None:
    if len(argv) < 2 or argv[0] in {"-h", "--help"}:
        print("usage: meos_s3.py put LOCAL s3://bucket/key | get s3://bucket/key LOCAL | ls s3://bucket/prefix")
        raise SystemExit(2)
    op = argv[0]
    if op == "put" and len(argv) == 3:
        cmd_put(argv[1], argv[2])
    elif op == "get" and len(argv) == 3:
        cmd_get(argv[1], argv[2])
    elif op == "ls" and len(argv) == 2:
        cmd_ls(argv[1])
    else:
        raise SystemExit("usage: meos_s3.py put|get|ls ...")


if __name__ == "__main__":
    main(sys.argv[1:])
