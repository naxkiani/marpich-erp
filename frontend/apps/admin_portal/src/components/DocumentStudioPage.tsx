"use client";

import { PageLayout } from "@marpich/core";
import {
  DataTable,
  EmptyState,
  PrintButton,
  ProgressBar,
  SkeletonTable,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useState } from "react";
import { DocumentTiptapEditor } from "@/components/DocumentTiptapEditor";
import {
  ensureHtmlDocument,
  htmlFileName,
  sanitizeStudioHtml,
} from "@/lib/documentStudioHtml";
import {
  addDocumentVersion,
  assignPhysicalLocation,
  createDocument,
  fetchDocumentDetail,
  fetchFolderContents,
  fetchPhysicalLocation,
  fetchRootFolder,
  fetchTenantBranding,
  loadDocumentsSession,
  loginDocumentsSession,
  previewDocument,
  saveDocumentsSession,
  signDocument,
  verifyDocumentPublic,
  type ApiSession,
  type DocumentDetail,
  type DocumentPreview,
  type DocumentSummary,
  type FolderContents,
  type PhysicalLocation,
  type TenantBranding,
  type VerifyResult,
} from "@/lib/documentsClient";

const DEFAULT_HTML =
  "<p>Official letter draft — Document Studio P4</p><p>Use toolbar for <strong>bold</strong> and <em>italic</em>.</p>";

export function DocumentStudioPage() {
  const { push } = useToast();
  const { dir } = useLocale();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("docs-demo");
  const [email, setEmail] = useState("docs@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [contents, setContents] = useState<FolderContents | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<DocumentDetail | null>(null);
  const [preview, setPreview] = useState<DocumentPreview | null>(null);
  const [verify, setVerify] = useState<VerifyResult | null>(null);
  const [branding, setBranding] = useState<TenantBranding | null>(null);

  const [title, setTitle] = useState("Official letter");
  const [fileName, setFileName] = useState("letter.html");
  const [contentHtml, setContentHtml] = useState(DEFAULT_HTML);
  const [signer, setSigner] = useState("signer@demo.dev");
  const [verifyToken, setVerifyToken] = useState("");
  const [physicalLocation, setPhysicalLocation] = useState<PhysicalLocation | null>(null);
  const [siteCode, setSiteCode] = useState("HQ-VAULT");
  const [room, setRoom] = useState("B2");
  const [cabinet, setCabinet] = useState("C-12");
  const [shelf, setShelf] = useState("3");
  const [box, setBox] = useState("BX-09");
  const [fileRef, setFileRef] = useState("FOLDER-A/12");

  const loadFolder = useCallback(
    async (active: ApiSession) => {
      setLoading(true);
      setProgress(40);
      setError(null);
      try {
        const [root, brand] = await Promise.all([
          fetchRootFolder(active),
          fetchTenantBranding(active),
        ]);
        const folder = await fetchFolderContents(active, root.id);
        setContents(folder);
        setBranding(brand);
        setProgress(100);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load Document Studio");
        setProgress(100);
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  useEffect(() => {
    const existing = loadDocumentsSession();
    if (!existing) {
      setLoading(false);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadFolder(existing);
  }, [loadFolder]);

  async function onLogin() {
    try {
      const next = await loginDocumentsSession(tenantId, email, password);
      saveDocumentsSession(next);
      setSession(next);
      push({ message: `Connected to tenant ${next.tenantId}` });
      await loadFolder(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  async function onCreate() {
    if (!session || !contents) return;
    try {
      const html = sanitizeStudioHtml(contentHtml);
      const created = await createDocument(session, {
        folder_id: contents.folder.id,
        title,
        file_name: htmlFileName(fileName),
        content: html,
        content_type: "text/html",
      });
      push({ message: `Document created: ${created.document.title}` });
      setSelectedId(created.document.id);
      setVerifyToken(created.document.qr_token ?? "");
      await loadFolder(session);
      await onSelect(created.document.id);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Create failed" });
    }
  }

  async function onSelect(documentId: string) {
    if (!session) return;
    setSelectedId(documentId);
    try {
      const [d, p, loc] = await Promise.all([
        fetchDocumentDetail(session, documentId),
        previewDocument(session, documentId),
        fetchPhysicalLocation(session, documentId),
      ]);
      setDetail(d);
      setPreview(p);
      setContentHtml(sanitizeStudioHtml(ensureHtmlDocument(p.content, p.content_type)));
      setPhysicalLocation(loc.physical_location);
      if (loc.physical_location) {
        setSiteCode(loc.physical_location.site_code);
        setRoom(loc.physical_location.room ?? "");
        setCabinet(loc.physical_location.cabinet ?? "");
        setShelf(loc.physical_location.shelf ?? "");
        setBox(loc.physical_location.box ?? "");
        setFileRef(loc.physical_location.file_ref ?? "");
      }
      setVerifyToken(d.document.qr_token ?? "");
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Load failed" });
    }
  }

  async function onAssignLocation() {
    if (!session || !selectedId) return;
    try {
      const updated = await assignPhysicalLocation(session, selectedId, {
        site_code: siteCode,
        room,
        cabinet,
        shelf,
        box,
        file_ref: fileRef,
      });
      setPhysicalLocation(updated.physical_location);
      push({ message: `Vault location set: ${siteCode}` });
      await onSelect(selectedId);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Location assign failed" });
    }
  }

  async function onVersion() {
    if (!session || !selectedId) return;
    try {
      const html = sanitizeStudioHtml(contentHtml);
      await addDocumentVersion(session, selectedId, {
        file_name: htmlFileName(fileName),
        content: `${html}<p><em>Revised ${new Date().toISOString()}</em></p>`,
        content_type: "text/html",
      });
      push({ message: "Version added" });
      await onSelect(selectedId);
      await loadFolder(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Version failed" });
    }
  }

  async function onSign() {
    if (!session || !selectedId) return;
    try {
      const signed = await signDocument(session, selectedId, [signer]);
      push({ message: `Signed with ${String(signed.algorithm ?? "HMAC-SHA256")}` });
      setVerifyToken(String(signed.qr_token ?? verifyToken));
      await onSelect(selectedId);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Sign failed" });
    }
  }

  async function onVerify() {
    if (!verifyToken) return;
    try {
      const result = await verifyDocumentPublic(verifyToken);
      setVerify(result);
      push({
        message: result.valid
          ? `Valid: ${result.title ?? result.document_id}`
          : "Integrity check failed",
      });
    } catch (err) {
      setVerify(null);
      push({ message: err instanceof Error ? err.message : "Verify failed" });
    }
  }

  const rows =
    contents?.documents.map((doc: DocumentSummary) => ({
      id: doc.id,
      title: doc.title,
      status: doc.status,
      qr: doc.qr_token ? "yes" : "—",
      open: doc.id,
    })) ?? [];

  const letterheadName = branding?.app_name || tenantId;
  const previewHtml = sanitizeStudioHtml(
    preview ? ensureHtmlDocument(preview.content, preview.content_type) : contentHtml,
  );

  return (
    <PageLayout
      title="Document Studio"
      subtitle="Document Exchange — rich HTML draft, A4/RTL preview, sign, QR, vault location."
      breadcrumb={[
        { label: "Enterprise", href: "/enterprise/federation" },
        { label: "Document Studio" },
      ]}
    >
      <ProgressBar value={progress} label="Loading documents" />

      {!session ? (
        <section className="mp-stack" aria-label="Sign in">
          <h2>Session</h2>
          <label>
            Tenant
            <input value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
          </label>
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="button" className="mp-btn" onClick={() => void onLogin()}>
            Sign in
          </button>
        </section>
      ) : null}

      {error ? <p role="alert">{error}</p> : null}

      {loading ? (
        <SkeletonTable rows={4} />
      ) : session && contents ? (
        <>
          <section className="mp-stack" aria-label="Create document">
            <h2>New document</h2>
            <label>
              Title
              <input value={title} onChange={(e) => setTitle(e.target.value)} />
            </label>
            <label>
              File name
              <input value={fileName} onChange={(e) => setFileName(e.target.value)} />
            </label>
            <DocumentTiptapEditor
              value={contentHtml}
              dir={dir}
              onChange={setContentHtml}
              placeholder="Write the official letter…"
            />
            <button type="button" className="mp-btn" onClick={() => void onCreate()}>
              Upload HTML version
            </button>
          </section>

          {rows.length === 0 ? (
            <EmptyState
              title="No documents yet"
              description="Compose an HTML letter and upload it through Document Exchange."
            />
          ) : (
            <DataTable
              columns={[
                { key: "title", header: "Title" },
                { key: "status", header: "Status" },
                { key: "qr", header: "QR" },
                {
                  key: "open",
                  header: "Open",
                  render: (row) => (
                    <button
                      type="button"
                      className="mp-btn"
                      onClick={() => void onSelect(String(row.id))}
                    >
                      Open
                    </button>
                  ),
                },
              ]}
              rows={rows}
            />
          )}

          <section className="mp-stack mp-doc-print-root" aria-label="A4 preview">
            <div className="mp-row">
              <h2>A4 preview</h2>
              <PrintButton label="Print A4" />
            </div>
            <article className="mp-doc-a4" dir={dir}>
              <header className="mp-doc-letterhead">
                {branding?.logo_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={String(branding.logo_url)} alt="" className="mp-doc-logo" />
                ) : null}
                <strong>{letterheadName}</strong>
                {branding?.primary_color ? (
                  <span
                    className="mp-doc-brand-bar"
                    style={{ background: String(branding.primary_color) }}
                  />
                ) : null}
              </header>
              <div
                className="mp-doc-a4-body"
                dangerouslySetInnerHTML={{ __html: previewHtml }}
              />
              {preview?.watermark ? (
                <p className="mp-doc-watermark">{String(preview.watermark.text)}</p>
              ) : null}
            </article>
          </section>

          {selectedId ? (
            <section className="mp-stack" aria-label="Document actions">
              <h2>Selected document</h2>
              <p>{detail?.document.title ?? selectedId}</p>
              <label>
                Signer email
                <input value={signer} onChange={(e) => setSigner(e.target.value)} />
              </label>
              <div className="mp-row">
                <button type="button" className="mp-btn" onClick={() => void onVersion()}>
                  Add HTML version
                </button>
                <button type="button" className="mp-btn" onClick={() => void onSign()}>
                  Sign (HMAC)
                </button>
              </div>
              {detail?.verify_path ? (
                <p>
                  Verify path: <code>{detail.verify_path}</code>
                </p>
              ) : null}
              {detail?.signatures?.length ? (
                <div>
                  <h3>Signatures</h3>
                  <pre>{JSON.stringify(detail.signatures, null, 2)}</pre>
                </div>
              ) : null}

              <h3>Physical vault location</h3>
              {physicalLocation ? (
                <p>
                  Current:{" "}
                  <code>
                    {physicalLocation.site_code} / {physicalLocation.room} /{" "}
                    {physicalLocation.cabinet} / {physicalLocation.shelf} /{" "}
                    {physicalLocation.box} / {physicalLocation.file_ref}
                  </code>
                </p>
              ) : (
                <p>No physical custody assigned yet.</p>
              )}
              <label>
                Site
                <input value={siteCode} onChange={(e) => setSiteCode(e.target.value)} />
              </label>
              <label>
                Room
                <input value={room} onChange={(e) => setRoom(e.target.value)} />
              </label>
              <label>
                Cabinet
                <input value={cabinet} onChange={(e) => setCabinet(e.target.value)} />
              </label>
              <label>
                Shelf
                <input value={shelf} onChange={(e) => setShelf(e.target.value)} />
              </label>
              <label>
                Box
                <input value={box} onChange={(e) => setBox(e.target.value)} />
              </label>
              <label>
                File ref
                <input value={fileRef} onChange={(e) => setFileRef(e.target.value)} />
              </label>
              <button type="button" className="mp-btn" onClick={() => void onAssignLocation()}>
                Assign vault location
              </button>
            </section>
          ) : null}

          <section className="mp-stack" aria-label="Public verify">
            <h2>Public QR verify</h2>
            <label>
              Token
              <input value={verifyToken} onChange={(e) => setVerifyToken(e.target.value)} />
            </label>
            <button type="button" className="mp-btn" onClick={() => void onVerify()}>
              Verify authenticity
            </button>
            {verify ? <pre>{JSON.stringify(verify, null, 2)}</pre> : null}
          </section>
        </>
      ) : null}
    </PageLayout>
  );
}
