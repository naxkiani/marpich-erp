import {
  type ApiSession,
  apiGet,
  apiPost,
  apiPut,
  createClientLogin,
  loadSession as loadDocumentsSession,
  saveSession as saveDocumentsSession,
} from "./clientAuth";

export type { ApiSession };

export const loginDocumentsSession = createClientLogin("Document Studio Admin");
export { loadDocumentsSession, saveDocumentsSession };

export type DocumentFolder = {
  id: string;
  name: string;
  is_root?: boolean;
  [key: string]: unknown;
};

export type DocumentSummary = {
  id: string;
  title: string;
  status: string;
  qr_token?: string | null;
  current_version_id?: string | null;
  [key: string]: unknown;
};

export type FolderContents = {
  folder: DocumentFolder;
  subfolders: DocumentFolder[];
  documents: DocumentSummary[];
};

export type DocumentDetail = {
  document: DocumentSummary;
  versions: Array<Record<string, unknown>>;
  signatures: Array<Record<string, unknown>>;
  verify_path?: string | null;
};

export type DocumentPreview = {
  file_name: string;
  content_type: string;
  checksum: string;
  content: string;
  watermark?: Record<string, unknown> | null;
  obligations?: string[];
  stored_mutated?: boolean;
};

export type VerifyResult = {
  valid: boolean;
  title?: string;
  document_id?: string;
  checksum_matches?: boolean;
  signature?: Record<string, unknown> | null;
  [key: string]: unknown;
};

export async function fetchRootFolder(session: ApiSession): Promise<DocumentFolder> {
  return apiGet("/api/v1/documents/folders/root", session);
}

export async function fetchFolderContents(
  session: ApiSession,
  folderId: string,
): Promise<FolderContents> {
  return apiGet(`/api/v1/documents/folders/${folderId}/contents`, session);
}

export async function createDocument(
  session: ApiSession,
  body: {
    folder_id: string;
    title: string;
    file_name: string;
    content: string;
    description?: string;
    content_type?: string;
  },
): Promise<{ document: DocumentSummary; current_version: Record<string, unknown> }> {
  return apiPost("/api/v1/documents/documents", session, {
    description: "",
    content_type: body.content_type ?? "text/html",
    ...body,
  });
}

export async function addDocumentVersion(
  session: ApiSession,
  documentId: string,
  body: { file_name: string; content: string; content_type?: string },
): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/documents/documents/${documentId}/versions`, session, {
    content_type: body.content_type ?? "text/html",
    ...body,
  });
}

export type TenantBranding = {
  app_name?: string;
  primary_color?: string;
  logo_url?: string;
  [key: string]: unknown;
};

export async function fetchTenantBranding(session: ApiSession): Promise<TenantBranding> {
  try {
    return await apiGet("/api/v1/settings/branding", session);
  } catch {
    return { app_name: session.tenantId };
  }
}

export async function fetchDocumentDetail(
  session: ApiSession,
  documentId: string,
): Promise<DocumentDetail> {
  return apiGet(`/api/v1/documents/documents/${documentId}`, session);
}

export async function signDocument(
  session: ApiSession,
  documentId: string,
  signers: string[],
): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/documents/documents/${documentId}/sign`, session, { signers });
}

export async function previewDocument(
  session: ApiSession,
  documentId: string,
): Promise<DocumentPreview> {
  return apiGet(`/api/v1/documents/documents/${documentId}/preview`, session);
}

export async function verifyDocumentPublic(token: string): Promise<VerifyResult> {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
  const res = await fetch(`${base}/api/v1/documents/verify/${encodeURIComponent(token)}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Verify failed (${res.status})`);
  }
  const json = (await res.json()) as { data: VerifyResult };
  return json.data;
}

export type PhysicalLocation = {
  site_code: string;
  room?: string;
  cabinet?: string;
  shelf?: string;
  box?: string;
  file_ref?: string;
};

export async function assignPhysicalLocation(
  session: ApiSession,
  documentId: string,
  location: PhysicalLocation,
): Promise<{ physical_location: PhysicalLocation | null; [key: string]: unknown }> {
  return apiPut(`/api/v1/documents/documents/${documentId}/physical-location`, session, location);
}

export async function fetchPhysicalLocation(
  session: ApiSession,
  documentId: string,
): Promise<{ document_id: string; physical_location: PhysicalLocation | null }> {
  return apiGet(`/api/v1/documents/documents/${documentId}/physical-location`, session);
}
