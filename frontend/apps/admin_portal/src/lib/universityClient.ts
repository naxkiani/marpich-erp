import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadUniversitySession,
  saveSession as saveUniversitySession,
} from "./clientAuth";

export type { ApiSession };

export const loginUniversitySession = createClientLogin("University Admin");
export { loadUniversitySession, saveUniversitySession };

export type UniversityStudent = {
  id: string;
  student_number: string;
  full_name?: string;
  email: string;
  program_code: string;
  lms_provider?: string | null;
  [key: string]: unknown;
};

export type UniversityCourse = {
  id: string;
  course_code: string;
  title: string;
  credits: number;
  term: string;
  lms_provider?: string | null;
  [key: string]: unknown;
};

export async function fetchUniversityStudents(session: ApiSession): Promise<UniversityStudent[]> {
  return apiGet("/api/v1/university/students", session);
}

export async function fetchUniversityCourses(session: ApiSession): Promise<UniversityCourse[]> {
  return apiGet("/api/v1/university/courses", session);
}

export async function registerMoodleConnector(
  session: ApiSession,
  config: { base_url: string; environment?: string },
): Promise<{ instance_ref: string }> {
  return apiPost("/api/v1/enterprise-connector-framework/connectors", session, {
    connector_type: "moodle",
    display_name: "Campus Moodle",
    config: { environment: "sandbox", ...config },
  });
}

export async function executeLmsSync(
  session: ApiSession,
  instanceRef: string,
  operation: string,
): Promise<Record<string, unknown>> {
  return apiPost(
    `/api/v1/enterprise-connector-framework/connectors/${instanceRef}/execute`,
    session,
    { operation, payload: {} },
  );
}
