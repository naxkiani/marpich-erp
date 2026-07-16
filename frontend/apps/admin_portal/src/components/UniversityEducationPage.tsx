"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useState } from "react";
import {
  executeLmsSync,
  fetchUniversityCourses,
  fetchUniversityStudents,
  loadUniversitySession,
  loginUniversitySession,
  registerMoodleConnector,
  saveUniversitySession,
  type ApiSession,
  type UniversityCourse,
  type UniversityStudent,
} from "@/lib/universityClient";

export function UniversityEducationPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("uni-demo");
  const [email, setEmail] = useState("registrar@uni.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [moodleUrl, setMoodleUrl] = useState("https://moodle.example.edu");
  const [instanceRef, setInstanceRef] = useState<string | null>(null);
  const [students, setStudents] = useState<UniversityStudent[]>([]);
  const [courses, setCourses] = useState<UniversityCourse[]>([]);

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [s, c] = await Promise.all([
        fetchUniversityStudents(active),
        fetchUniversityCourses(active),
      ]);
      setStudents(s);
      setCourses(c);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load university data");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const existing = loadUniversitySession();
    if (!existing) {
      setLoading(false);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadData(existing);
  }, [loadData]);

  async function onLogin() {
    try {
      const next = await loginUniversitySession(tenantId, email, password);
      saveUniversitySession(next);
      setSession(next);
      push({ message: `Connected to ${next.tenantId}` });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  async function onRegisterAndSync() {
    if (!session) return;
    try {
      const registered = await registerMoodleConnector(session, { base_url: moodleUrl });
      setInstanceRef(registered.instance_ref);
      await executeLmsSync(session, registered.instance_ref, "courses_sync");
      await executeLmsSync(session, registered.instance_ref, "enrollments_sync");
      await executeLmsSync(session, registered.instance_ref, "grades_push");
      push({ message: "Moodle sync completed via Integration Platform" });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "LMS sync failed" });
    }
  }

  return (
    <PageLayout
      title="University Education"
      subtitle="CAP-EDU-001 students/courses plus Moodle sync through the Connector Framework (no domain HTTP)."
      breadcrumb={[
        { label: "Education", href: "/education/university" },
        { label: "University" },
      ]}
    >
      <ProgressBar value={progress} label="Loading university" />

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

      {session ? (
        <section className="mp-stack" aria-label="LMS sync">
          <h2>Moodle sync (ECF)</h2>
          <label>
            Moodle base URL
            <input value={moodleUrl} onChange={(e) => setMoodleUrl(e.target.value)} />
          </label>
          <button type="button" className="mp-btn" onClick={() => void onRegisterAndSync()}>
            Register connector + sync courses/enrollments/grades
          </button>
          {instanceRef ? (
            <p>
              Instance: <code>{instanceRef}</code>
            </p>
          ) : null}
          <p>
            SSO remains on Identity Federation (register Moodle/Google as OIDC IdP) — separate from
            grade/course sync.
          </p>
        </section>
      ) : null}

      {loading ? (
        <SkeletonTable rows={4} />
      ) : session ? (
        <>
          <h2>Courses</h2>
          {courses.length === 0 ? (
            <EmptyState title="No courses" description="Run Moodle courses_sync to import." />
          ) : (
            <DataTable
              columns={[
                { key: "course_code", header: "Code" },
                { key: "title", header: "Title" },
                { key: "term", header: "Term" },
                { key: "lms_provider", header: "LMS" },
              ]}
              rows={courses.map((c) => ({
                id: c.id,
                course_code: c.course_code,
                title: c.title,
                term: c.term,
                lms_provider: c.lms_provider ?? "—",
              }))}
            />
          )}

          <h2>Students</h2>
          {students.length === 0 ? (
            <EmptyState title="No students" description="Run enrollments_sync to import." />
          ) : (
            <DataTable
              columns={[
                { key: "student_number", header: "Number" },
                { key: "full_name", header: "Name" },
                { key: "email", header: "Email" },
                { key: "lms_provider", header: "LMS" },
              ]}
              rows={students.map((s) => ({
                id: s.id,
                student_number: s.student_number,
                full_name: s.full_name ?? `${s.first_name ?? ""} ${s.last_name ?? ""}`.trim(),
                email: s.email,
                lms_provider: s.lms_provider ?? "—",
              }))}
            />
          )}
        </>
      ) : null}
    </PageLayout>
  );
}
