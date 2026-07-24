"use client";

import Link from "next/link";
import { useAuth } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ExportButton,
  PrintButton,
  ProgressBar,
  SkeletonTable,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  clearUniversitySession,
  enrollUniversityStudent,
  executeLmsSync,
  fetchUniversityCourses,
  fetchUniversityDashboard,
  fetchUniversityGrades,
  fetchUniversityStudents,
  isAuthFailure,
  loadUniversitySession,
  loginUniversitySession,
  offerUniversityCourse,
  postUniversityGrade,
  registerMoodleConnector,
  saveUniversitySession,
  seedEducationPersonas,
  seedUniversityDemo,
  type ApiSession,
  type UniversityCourse,
  type UniversityDashboard,
  type UniversityGrade,
  type UniversityStudent,
} from "@/lib/universityClient";

type TabId = "overview" | "students" | "courses" | "grades" | "lms";

const METRIC_JEWELS = ["royal", "emerald", "gold", "forest", "orange", "purple"] as const;
const DRAFT_KEY = "marpich.university.education.draft";

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "enrolled" || status === "active"
      ? "ok"
      : status === "graduated" || status === "completed"
        ? "muted"
        : "warn";
  return (
    <span className={`ue-chip ue-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function UniversityEducationPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const {
    session: authSession,
    isAuthenticated,
    isLoading: authLoading,
    login,
    logout,
  } = useAuth();

  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [needsReconnect, setNeedsReconnect] = useState(false);
  const [tab, setTab] = useState<TabId>("overview");
  const [filterQ, setFilterQ] = useState("");

  const [localSession, setLocalSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("uni-demo");
  const [email, setEmail] = useState("registrar@uni.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [moodleUrl, setMoodleUrl] = useState("https://moodle.example.edu");
  const [instanceRef, setInstanceRef] = useState<string | null>(null);

  const [dashboard, setDashboard] = useState<UniversityDashboard | null>(null);
  const [students, setStudents] = useState<UniversityStudent[]>([]);
  const [courses, setCourses] = useState<UniversityCourse[]>([]);
  const [grades, setGrades] = useState<UniversityGrade[]>([]);

  const [studentForm, setStudentForm] = useState({
    student_number: "",
    first_name: "",
    last_name: "",
    email: "",
    program_code: "CS",
  });
  const [courseForm, setCourseForm] = useState({
    course_code: "",
    title: "",
    credits: "3",
    term: "FALL2026",
  });
  const [gradeForm, setGradeForm] = useState({
    student_id: "",
    course_id: "",
    letter_grade: "A",
  });
  const [selectedStudentId, setSelectedStudentId] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [draftReady, setDraftReady] = useState(false);

  const session = needsReconnect ? null : localSession ?? (isAuthenticated ? authSession : null);

  const draft = useMemo(
    () => ({ studentForm, courseForm, gradeForm }),
    [courseForm, gradeForm, studentForm],
  );

  const persistDraft = useCallback(
    async (values: typeof draft) => {
      if (!draftReady) return;
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
      } catch {
        /* ignore quota */
      }
    },
    [draftReady],
  );

  const { saving: draftSaving } = useAutosave(draft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof draft>;
        if (parsed.studentForm) setStudentForm((f) => ({ ...f, ...parsed.studentForm }));
        if (parsed.courseForm) setCourseForm((f) => ({ ...f, ...parsed.courseForm }));
        if (parsed.gradeForm) setGradeForm((f) => ({ ...f, ...parsed.gradeForm }));
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const resetAuthState = useCallback(async () => {
    setNeedsReconnect(true);
    clearUniversitySession();
    setLocalSession(null);
    setDashboard(null);
    setStudents([]);
    setCourses([]);
    setGrades([]);
    setSelectedStudentId("");
    try {
      await logout();
    } catch {
      /* session may already be invalid */
    }
  }, [logout]);

  const loadData = useCallback(
    async (active: ApiSession) => {
      setLoading(true);
      setProgress(35);
      setError(null);
      try {
        const [dash, s, c, g] = await Promise.all([
          fetchUniversityDashboard(active),
          fetchUniversityStudents(active),
          fetchUniversityCourses(active),
          fetchUniversityGrades(active),
        ]);
        setDashboard(dash);
        const studentItems = Array.isArray(s) ? s : [];
        setStudents(studentItems);
        setCourses(Array.isArray(c) ? c : []);
        setGrades(Array.isArray(g) ? g : []);
        setSelectedStudentId((prev) => {
          if (prev && studentItems.some((x) => x.id === prev)) return prev;
          return studentItems[0]?.id || "";
        });
        setNeedsReconnect(false);
        setProgress(100);
      } catch (err) {
        const message = err instanceof Error ? err.message : t("university.loadFailed");
        setError(message);
        setProgress(100);
        if (isAuthFailure(message)) {
          await resetAuthState();
          setError(t("university.sessionExpired"));
        }
      } finally {
        setLoading(false);
      }
    },
    [resetAuthState, t],
  );

  useEffect(() => {
    if (authLoading) return;
    if (needsReconnect) {
      setLoading(false);
      setProgress(100);
      return;
    }
    const stored = loadUniversitySession();
    if (stored) {
      setLocalSession(stored);
      void loadData(stored);
      return;
    }
    if (authSession && isAuthenticated) {
      void loadData(authSession);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [authLoading, authSession, isAuthenticated, loadData, needsReconnect]);

  const q = filterQ.toLowerCase().trim();

  const stats = useMemo(() => {
    const summary = dashboard?.summary;
    return [
      { label: t("university.stat.students"), value: summary?.student_count ?? students.length },
      { label: t("university.stat.courses"), value: summary?.course_count ?? courses.length },
      { label: t("university.stat.grades"), value: summary?.grade_count ?? grades.length },
      { label: t("university.stat.programs"), value: summary?.program_count ?? 0 },
      { label: t("university.stat.activeCourses"), value: summary?.active_courses ?? 0 },
    ];
  }, [courses.length, dashboard, grades.length, students.length, t]);

  const studentRows = useMemo(
    () =>
      students
        .filter((s) => {
          const status = s.status ?? "enrolled";
          if (statusFilter && status !== statusFilter) return false;
          if (!q) return true;
          const hay =
            `${s.student_number} ${s.full_name ?? ""} ${s.email} ${s.program_code} ${status}`.toLowerCase();
          return hay.includes(q);
        })
        .map((s) => ({
          id: s.id,
          student_number: s.student_number,
          full_name: s.full_name ?? `${s.first_name ?? ""} ${s.last_name ?? ""}`.trim(),
          email: s.email,
          program_code: s.program_code,
          status: s.status ?? "enrolled",
          lms_provider: s.lms_provider ?? "—",
        })),
    [q, statusFilter, students],
  );

  const selectedStudent = useMemo(
    () => students.find((s) => s.id === selectedStudentId) ?? null,
    [selectedStudentId, students],
  );

  const selectedStudentGrades = useMemo(
    () => grades.filter((g) => g.student_id === selectedStudentId),
    [grades, selectedStudentId],
  );

  const lifecycleStep = useMemo(() => {
    if (!students.length) return 0;
    if (!courses.length) return 1;
    if (!selectedStudent) return 1;
    if (selectedStudentGrades.length === 0) return 2;
    return 3;
  }, [courses.length, selectedStudent, selectedStudentGrades.length, students.length]);

  const workflowSteps = useMemo(
    () => [
      t("university.step.enroll"),
      t("university.step.offer"),
      t("university.step.grade"),
      t("university.step.complete"),
    ],
    [t],
  );

  useEffect(() => {
    if (!selectedStudentId) return;
    setGradeForm((f) =>
      f.student_id === selectedStudentId ? f : { ...f, student_id: selectedStudentId },
    );
  }, [selectedStudentId]);

  const courseRows = useMemo(
    () =>
      courses
        .filter((c) => {
          if (!q) return true;
          const hay = `${c.course_code} ${c.title} ${c.term}`.toLowerCase();
          return hay.includes(q);
        })
        .map((c) => ({
          id: c.id,
          course_code: c.course_code,
          title: c.title,
          credits: c.credits,
          term: c.term,
          status: c.status ?? "active",
          lms_provider: c.lms_provider ?? "—",
        })),
    [courses, q],
  );

  const gradeRows = useMemo(
    () =>
      grades
        .filter((g) => {
          if (!q) return true;
          const hay =
            `${g.student_number ?? ""} ${g.student_name ?? ""} ${g.course_code ?? ""} ${g.letter_grade}`.toLowerCase();
          return hay.includes(q);
        })
        .map((g) => ({
          id: g.id,
          student: g.student_name ?? g.student_number ?? g.student_id,
          course: g.course_code ?? g.course_title ?? g.course_id,
          letter_grade: g.letter_grade,
          posted_at: g.posted_at ? String(g.posted_at).slice(0, 10) : "—",
        })),
    [grades, q],
  );

  const exportRows = useMemo(() => {
    if (tab === "courses") return courseRows;
    if (tab === "grades") return gradeRows;
    if (tab === "students") return studentRows;
    return stats.map((s) => ({ metric: s.label, value: String(s.value) }));
  }, [courseRows, gradeRows, stats, studentRows, tab]);

  const tabs: { id: TabId; label: string }[] = [
    { id: "overview", label: t("university.tab.overview") },
    { id: "students", label: t("university.tab.students") },
    { id: "courses", label: t("university.tab.courses") },
    { id: "grades", label: t("university.tab.grades") },
    { id: "lms", label: t("university.tab.lms") },
  ];

  async function onConnect() {
    setBusy(true);
    setError(null);
    try {
      const next = await loginUniversitySession(tenantId, email, password);
      setLocalSession(next);
      saveUniversitySession(next);
      setNeedsReconnect(false);
      try {
        await login({
          tenantId,
          email,
          password,
          displayName: "University Admin",
          registerIfMissing: true,
        });
      } catch {
        /* module session is enough */
      }
      try {
        await seedEducationPersonas(next);
      } catch {
        /* admin may already have roles; continue */
      }
      try {
        await seedUniversityDemo(next);
      } catch {
        /* dashboard auto-seeds on read */
      }
      push({ message: t("university.connected") });
      await loadData(next);
    } catch (err) {
      const message = err instanceof Error ? err.message : t("university.connectFailed");
      setError(message);
      push({ message });
    } finally {
      setBusy(false);
    }
  }

  async function onRegisterAndSync() {
    if (!session) return;
    setBusy(true);
    try {
      const registered = await registerMoodleConnector(session, { base_url: moodleUrl });
      setInstanceRef(registered.instance_ref);
      await executeLmsSync(session, registered.instance_ref, "courses_sync");
      await executeLmsSync(session, registered.instance_ref, "enrollments_sync");
      await executeLmsSync(session, registered.instance_ref, "grades_push");
      push({ message: t("university.lmsDone") });
      await loadData(session);
    } catch (err) {
      const message = err instanceof Error ? err.message : t("university.lmsFailed");
      if (isAuthFailure(message)) {
        await resetAuthState();
        setError(t("university.sessionExpired"));
      }
      push({ message });
    } finally {
      setBusy(false);
    }
  }

  async function onEnrollStudent() {
    if (!session) return;
    setBusy(true);
    try {
      await enrollUniversityStudent(session, studentForm);
      setStudentForm({
        student_number: "",
        first_name: "",
        last_name: "",
        email: "",
        program_code: "CS",
      });
      push({ message: t("university.studentEnrolled") });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : t("university.failed") });
    } finally {
      setBusy(false);
    }
  }

  async function onOfferCourse() {
    if (!session) return;
    setBusy(true);
    try {
      await offerUniversityCourse(session, {
        ...courseForm,
        credits: Number(courseForm.credits) || 3,
      });
      setCourseForm({ course_code: "", title: "", credits: "3", term: "FALL2026" });
      push({ message: t("university.courseOffered") });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : t("university.failed") });
    } finally {
      setBusy(false);
    }
  }

  async function onPostGrade() {
    if (!session) return;
    setBusy(true);
    try {
      await postUniversityGrade(session, gradeForm);
      setGradeForm({ student_id: "", course_id: "", letter_grade: "A" });
      push({ message: t("university.gradePosted") });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : t("university.failed") });
    } finally {
      setBusy(false);
    }
  }

  return (
    <PageLayout
      title={t("university.title")}
      subtitle={t("university.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("university.breadcrumb"), href: "/education/university" },
        { label: t("university.university") },
      ]}
      actions={
        <>
          <ExportButton label={t("common.export")} rows={exportRows} filename="university-education.csv" />
          <PrintButton label={t("common.print")} />
          {session ? (
            <button
              type="button"
              className="mp-btn"
              disabled={loading || busy}
              onClick={() => void loadData(session)}
            >
              {t("common.refresh")}
            </button>
          ) : (
            <Link href="/login?returnTo=/education/university" className="mp-btn mp-btn-primary">
              {t("dashboard.signIn")}
            </Link>
          )}
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading || authLoading ? t("university.loading") : t("university.ready")}
      />

      {error ? (
        <p className="ue-alert" role="alert">
          {error}
        </p>
      ) : null}

      {!session && !authLoading ? (
        <section className="ue-session" aria-label={t("dashboard.session")}>
          <div className="ue-session-banner">
            <h2>{t("university.connectHint")}</h2>
            <p>{t("university.connectHelp")}</p>
          </div>
          <div className="ue-session-body">
            <div className="mp-form ue-form-grid">
              <div className="mp-field">
                <label htmlFor="ue-tenant">{t("dashboard.tenant")}</label>
                <input
                  id="ue-tenant"
                  className="mp-input"
                  value={tenantId}
                  onChange={(e) => setTenantId(e.target.value)}
                />
              </div>
              <div className="mp-field">
                <label htmlFor="ue-email">{t("dashboard.email")}</label>
                <input
                  id="ue-email"
                  className="mp-input"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="mp-field">
                <label htmlFor="ue-password">{t("dashboard.password")}</label>
                <input
                  id="ue-password"
                  className="mp-input"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
            <div className="ue-actions">
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy}
                onClick={() => void onConnect()}
              >
                {t("university.connect")}
              </button>
              <Link href="/login?returnTo=/education/university" className="mp-btn">
                {t("dashboard.openLogin")}
              </Link>
            </div>
          </div>
        </section>
      ) : null}

      {session && (loading || authLoading) ? <SkeletonTable rows={6} cols={4} /> : null}

      {session && !loading ? (
        <div className="ue-layout">
          <aside className="ue-aside" aria-label={t("university.rail")}>
            <section className="ue-panel-card">
              <header className="ue-panel-head ue-jewel-bar--royal">
                <h2>{t("university.workflow")}</h2>
              </header>
              <div className="ue-panel-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("university.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("university.workflowHint")}</p>
                )}
                {selectedStudent ? (
                  <p className="mp-field-help">
                    <StatusChip status={selectedStudent.status ?? "enrolled"} /> ·{" "}
                    {selectedStudent.student_number} · {selectedStudentGrades.length}{" "}
                    {t("university.stat.grades").toLowerCase()}
                  </p>
                ) : (
                  <p className="mp-field-help">{t("university.selectStudentHint")}</p>
                )}
              </div>
            </section>

            <section className="ue-panel-card">
              <header className="ue-panel-head ue-jewel-bar--emerald">
                <h2>{t("university.rail.status")}</h2>
              </header>
              <div className="ue-panel-body">
                <div className="ue-status-row">
                  <span>{t("dashboard.tenant")}</span>
                  <strong>{session.tenantId}</strong>
                </div>
                <div className="ue-status-row">
                  <span>{t("university.capability")}</span>
                  <strong>CAP-EDU-001</strong>
                </div>
                <p className="ue-headline">
                  {t("university.stat.students")}: {dashboard?.summary.student_count ?? students.length} ·{" "}
                  {t("university.stat.courses")}: {dashboard?.summary.course_count ?? courses.length}
                </p>
              </div>
            </section>

            <section className="ue-panel-card">
              <header className="ue-panel-head ue-jewel-bar--gold">
                <h2>{t("university.rail.lms")}</h2>
              </header>
              <div className="ue-panel-body">
                <p className="mp-field-help">{t("university.lmsHint")}</p>
                <button
                  type="button"
                  className="mp-btn"
                  disabled={busy}
                  onClick={() => setTab("lms")}
                >
                  {t("university.openLms")}
                </button>
              </div>
            </section>
          </aside>

          <div className="ue-main">
            <section className="ue-metrics" aria-label={t("university.metrics")}>
              {stats.map((s, i) => {
                const jewel = METRIC_JEWELS[i % METRIC_JEWELS.length]!;
                return (
                  <div key={s.label} className={`ue-metric ue-metric--${jewel}`}>
                    <span className="ue-metric-label">{s.label}</span>
                    <strong>{s.value}</strong>
                  </div>
                );
              })}
            </section>

            <div className="ue-filters">
              <AdvancedFilterBar
                filters={[{ id: "q", label: t("common.filter"), type: "text" }]}
                onChange={(values) => setFilterQ(values.q ?? "")}
              />
              <label className="mp-filter-item ue-status-filter">
                <span>{t("university.col.status")}</span>
                <select
                  className="mp-input"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  aria-label={t("university.col.status")}
                >
                  <option value="">{t("university.filterAll")}</option>
                  <option value="enrolled">enrolled</option>
                  <option value="active">active</option>
                  <option value="graduated">graduated</option>
                  <option value="completed">completed</option>
                </select>
              </label>
            </div>

            <div className="ue-tabs" role="tablist" aria-label={t("university.title")}>
              {tabs.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  role="tab"
                  aria-selected={tab === item.id}
                  className={`ue-tab ${tab === item.id ? "ue-tab--on" : ""}`}
                  onClick={() => setTab(item.id)}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <div className="ue-panel mp-animate-in" role="tabpanel">
              {tab === "overview" ? (
                <div className="ue-overview">
                  <section className="ue-card">
                    <h2>{t("university.tab.overview")}</h2>
                    {students.length === 0 && courses.length === 0 ? (
                      <EmptyState
                        title={t("university.emptyCatalog")}
                        description={t("university.emptyCatalogHint")}
                      />
                    ) : (
                      <DataTable
                        columns={[
                          { key: "program", header: t("university.col.program"), sortable: true },
                          { key: "count", header: t("university.col.count"), sortable: true },
                        ]}
                        rows={Object.entries(dashboard?.by_program ?? {}).map(([program, count]) => ({
                          id: program,
                          program,
                          count,
                        }))}
                      />
                    )}
                  </section>
                  <section className="ue-card">
                    <h2>{t("university.tab.grades")}</h2>
                    {gradeRows.length === 0 ? (
                      <EmptyState
                        title={t("university.noGrades")}
                        description={t("university.noGradesHint")}
                      />
                    ) : (
                      <DataTable
                        columns={[
                          { key: "student", header: t("university.col.student"), sortable: true },
                          { key: "course", header: t("university.col.course"), sortable: true },
                          { key: "letter_grade", header: t("university.col.grade"), sortable: true },
                        ]}
                        rows={gradeRows.slice(0, 8)}
                      />
                    )}
                  </section>
                </div>
              ) : null}

              {tab === "students" ? (
                <section className="ue-stack">
                  <form
                    className="mp-form ue-form-grid"
                    onSubmit={(e) => {
                      e.preventDefault();
                      void onEnrollStudent();
                    }}
                  >
                    <div className="mp-field">
                      <label htmlFor="ue-s-num">{t("university.col.number")}</label>
                      <input
                        id="ue-s-num"
                        className="mp-input"
                        required
                        value={studentForm.student_number}
                        onChange={(e) =>
                          setStudentForm((f) => ({ ...f, student_number: e.target.value }))
                        }
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-s-first">{t("university.col.firstName")}</label>
                      <input
                        id="ue-s-first"
                        className="mp-input"
                        required
                        value={studentForm.first_name}
                        onChange={(e) =>
                          setStudentForm((f) => ({ ...f, first_name: e.target.value }))
                        }
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-s-last">{t("university.col.lastName")}</label>
                      <input
                        id="ue-s-last"
                        className="mp-input"
                        required
                        value={studentForm.last_name}
                        onChange={(e) =>
                          setStudentForm((f) => ({ ...f, last_name: e.target.value }))
                        }
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-s-email">{t("dashboard.email")}</label>
                      <input
                        id="ue-s-email"
                        className="mp-input"
                        type="email"
                        required
                        value={studentForm.email}
                        onChange={(e) => setStudentForm((f) => ({ ...f, email: e.target.value }))}
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-s-prog">{t("university.col.program")}</label>
                      <input
                        id="ue-s-prog"
                        className="mp-input"
                        required
                        value={studentForm.program_code}
                        onChange={(e) =>
                          setStudentForm((f) => ({ ...f, program_code: e.target.value }))
                        }
                      />
                    </div>
                    <div className="ue-actions">
                      <button type="submit" className="mp-btn mp-btn-primary" disabled={busy}>
                        {t("university.enroll")}
                      </button>
                    </div>
                  </form>
                  {studentRows.length === 0 ? (
                    <EmptyState
                      title={t("university.noStudents")}
                      description={t("university.noStudentsHint")}
                    />
                  ) : (
                    <>
                      <DataTable
                        columns={[
                          {
                            key: "student_number",
                            header: t("university.col.number"),
                            sortable: true,
                          },
                          { key: "full_name", header: t("university.col.name"), sortable: true },
                          { key: "email", header: t("dashboard.email"), sortable: true },
                          {
                            key: "program_code",
                            header: t("university.col.program"),
                            sortable: true,
                          },
                          {
                            key: "status",
                            header: t("university.col.status"),
                            sortable: true,
                            render: (row) => <StatusChip status={String(row.status)} />,
                          },
                          { key: "lms_provider", header: t("university.col.lms"), sortable: true },
                        ]}
                        rows={studentRows}
                        selectable
                        onSelectionChange={(ids) => {
                          if (ids[0]) setSelectedStudentId(ids[0]);
                        }}
                      />
                      {selectedStudent ? (
                        <section
                          className="ue-detail-panel mp-animate-in"
                          aria-label={t("university.studentDetail")}
                        >
                          <header>{t("university.studentDetail")}</header>
                          <dl className="ue-detail-dl">
                            <div>
                              <dt>{t("university.col.number")}</dt>
                              <dd>{selectedStudent.student_number}</dd>
                            </div>
                            <div>
                              <dt>{t("university.col.name")}</dt>
                              <dd>
                                {selectedStudent.full_name ??
                                  `${selectedStudent.first_name ?? ""} ${selectedStudent.last_name ?? ""}`.trim()}
                              </dd>
                            </div>
                            <div>
                              <dt>{t("university.col.status")}</dt>
                              <dd>
                                <StatusChip status={selectedStudent.status ?? "enrolled"} />
                              </dd>
                            </div>
                            <div>
                              <dt>{t("university.col.program")}</dt>
                              <dd>{selectedStudent.program_code}</dd>
                            </div>
                            <div>
                              <dt>{t("dashboard.email")}</dt>
                              <dd>{selectedStudent.email}</dd>
                            </div>
                            <div>
                              <dt>{t("university.stat.grades")}</dt>
                              <dd>{selectedStudentGrades.length}</dd>
                            </div>
                          </dl>
                          <div className="ue-actions">
                            <button
                              type="button"
                              className="mp-btn"
                              onClick={() => setTab("grades")}
                            >
                              {t("university.postGrade")}
                            </button>
                          </div>
                        </section>
                      ) : null}
                    </>
                  )}
                </section>
              ) : null}

              {tab === "courses" ? (
                <section className="ue-stack">
                  <form
                    className="mp-form ue-form-grid"
                    onSubmit={(e) => {
                      e.preventDefault();
                      void onOfferCourse();
                    }}
                  >
                    <div className="mp-field">
                      <label htmlFor="ue-c-code">{t("university.col.code")}</label>
                      <input
                        id="ue-c-code"
                        className="mp-input"
                        required
                        value={courseForm.course_code}
                        onChange={(e) =>
                          setCourseForm((f) => ({ ...f, course_code: e.target.value }))
                        }
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-c-title">{t("university.col.title")}</label>
                      <input
                        id="ue-c-title"
                        className="mp-input"
                        required
                        value={courseForm.title}
                        onChange={(e) => setCourseForm((f) => ({ ...f, title: e.target.value }))}
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-c-credits">{t("university.col.credits")}</label>
                      <input
                        id="ue-c-credits"
                        className="mp-input"
                        type="number"
                        min={1}
                        max={12}
                        required
                        value={courseForm.credits}
                        onChange={(e) => setCourseForm((f) => ({ ...f, credits: e.target.value }))}
                      />
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-c-term">{t("university.col.term")}</label>
                      <input
                        id="ue-c-term"
                        className="mp-input"
                        required
                        value={courseForm.term}
                        onChange={(e) => setCourseForm((f) => ({ ...f, term: e.target.value }))}
                      />
                    </div>
                    <div className="ue-actions">
                      <button type="submit" className="mp-btn mp-btn-primary" disabled={busy}>
                        {t("university.offerCourse")}
                      </button>
                    </div>
                  </form>
                  {courseRows.length === 0 ? (
                    <EmptyState
                      title={t("university.noCourses")}
                      description={t("university.noCoursesHint")}
                    />
                  ) : (
                    <DataTable
                      columns={[
                        { key: "course_code", header: t("university.col.code"), sortable: true },
                        { key: "title", header: t("university.col.title"), sortable: true },
                        { key: "credits", header: t("university.col.credits"), sortable: true },
                        { key: "term", header: t("university.col.term"), sortable: true },
                        {
                          key: "status",
                          header: t("university.col.status"),
                          sortable: true,
                          render: (row) => <StatusChip status={String(row.status)} />,
                        },
                        { key: "lms_provider", header: t("university.col.lms"), sortable: true },
                      ]}
                      rows={courseRows}
                    />
                  )}
                </section>
              ) : null}

              {tab === "grades" ? (
                <section className="ue-stack">
                  <form
                    className="mp-form ue-form-grid"
                    onSubmit={(e) => {
                      e.preventDefault();
                      void onPostGrade();
                    }}
                  >
                    <div className="mp-field">
                      <label htmlFor="ue-g-student">{t("university.col.student")}</label>
                      <select
                        id="ue-g-student"
                        className="mp-input"
                        required
                        value={gradeForm.student_id}
                        onChange={(e) =>
                          setGradeForm((f) => ({ ...f, student_id: e.target.value }))
                        }
                      >
                        <option value="">{t("university.selectStudent")}</option>
                        {students.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.student_number} — {s.full_name ?? s.email}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-g-course">{t("university.col.course")}</label>
                      <select
                        id="ue-g-course"
                        className="mp-input"
                        required
                        value={gradeForm.course_id}
                        onChange={(e) => setGradeForm((f) => ({ ...f, course_id: e.target.value }))}
                      >
                        <option value="">{t("university.selectCourse")}</option>
                        {courses.map((c) => (
                          <option key={c.id} value={c.id}>
                            {c.course_code} — {c.title}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="mp-field">
                      <label htmlFor="ue-g-letter">{t("university.col.grade")}</label>
                      <select
                        id="ue-g-letter"
                        className="mp-input"
                        value={gradeForm.letter_grade}
                        onChange={(e) =>
                          setGradeForm((f) => ({ ...f, letter_grade: e.target.value }))
                        }
                      >
                        {["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F", "P"].map(
                          (g) => (
                            <option key={g} value={g}>
                              {g}
                            </option>
                          ),
                        )}
                      </select>
                    </div>
                    <div className="ue-actions">
                      <button type="submit" className="mp-btn mp-btn-primary" disabled={busy}>
                        {t("university.postGrade")}
                      </button>
                    </div>
                  </form>
                  {gradeRows.length === 0 ? (
                    <EmptyState
                      title={t("university.noGrades")}
                      description={t("university.noGradesHint")}
                    />
                  ) : (
                    <DataTable
                      columns={[
                        { key: "student", header: t("university.col.student"), sortable: true },
                        { key: "course", header: t("university.col.course"), sortable: true },
                        { key: "letter_grade", header: t("university.col.grade"), sortable: true },
                        { key: "posted_at", header: t("university.col.posted"), sortable: true },
                      ]}
                      rows={gradeRows}
                    />
                  )}
                </section>
              ) : null}

              {tab === "lms" ? (
                <section className="ue-stack">
                  <p className="mp-field-help">{t("university.lmsDetail")}</p>
                  <div className="mp-field">
                    <label htmlFor="ue-moodle">{t("university.moodleUrl")}</label>
                    <input
                      id="ue-moodle"
                      className="mp-input"
                      value={moodleUrl}
                      onChange={(e) => setMoodleUrl(e.target.value)}
                    />
                  </div>
                  <div className="ue-actions">
                    <button
                      type="button"
                      className="mp-btn mp-btn-primary"
                      disabled={busy}
                      onClick={() => void onRegisterAndSync()}
                    >
                      {t("university.syncMoodle")}
                    </button>
                  </div>
                  {instanceRef ? (
                    <p className="mp-field-help">
                      {t("university.instance")}: <code>{instanceRef}</code>
                    </p>
                  ) : null}
                </section>
              ) : null}
            </div>
          </div>
        </div>
      ) : null}

      <style jsx>{`
        .ue-alert {
          color: var(--mp-danger, #b42318);
          margin-block: 0.75rem;
        }
        .ue-session {
          border: 1px solid var(--mp-border, #d0d5dd);
          border-radius: 12px;
          overflow: hidden;
          margin-block: 1rem;
          background: var(--mp-surface, #fff);
        }
        .ue-session-banner {
          padding: 1rem 1.25rem;
          background: linear-gradient(
            120deg,
            color-mix(in srgb, var(--mp-royal, #1e3a8a) 18%, transparent),
            color-mix(in srgb, var(--mp-emerald, #059669) 12%, transparent)
          );
        }
        .ue-session-banner h2 {
          margin: 0 0 0.35rem;
          font-size: 1.1rem;
        }
        .ue-session-banner p,
        .ue-headline,
        .mp-field-help {
          margin: 0;
          color: var(--mp-muted, #667085);
          font-size: 0.9rem;
        }
        .ue-session-body {
          padding: 1rem 1.25rem 1.25rem;
        }
        .ue-form-grid {
          display: grid;
          gap: 0.75rem;
          grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        }
        .ue-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-block-start: 0.75rem;
        }
        .ue-layout {
          display: grid;
          gap: 1rem;
          grid-template-columns: minmax(220px, 280px) 1fr;
          margin-block-start: 1rem;
        }
        @media (max-width: 960px) {
          .ue-layout {
            grid-template-columns: 1fr;
          }
        }
        .ue-aside,
        .ue-main {
          min-width: 0;
        }
        .ue-panel-card {
          border: 1px solid var(--mp-border, #d0d5dd);
          border-radius: 12px;
          overflow: hidden;
          background: var(--mp-surface, #fff);
          margin-block-end: 0.75rem;
        }
        .ue-panel-head {
          padding: 0.65rem 0.9rem;
        }
        .ue-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .ue-jewel-bar--royal {
          border-block-start: 3px solid var(--mp-royal, #1e3a8a);
          background: color-mix(in srgb, var(--mp-royal, #1e3a8a) 8%, transparent);
        }
        .ue-jewel-bar--emerald {
          border-block-start: 3px solid var(--mp-emerald, #059669);
          background: color-mix(in srgb, var(--mp-emerald, #059669) 8%, transparent);
        }
        .ue-jewel-bar--gold {
          border-block-start: 3px solid var(--mp-gold, #ca8a04);
          background: color-mix(in srgb, var(--mp-gold, #ca8a04) 10%, transparent);
        }
        .ue-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          align-items: end;
        }
        .ue-status-filter {
          display: grid;
          gap: 0.25rem;
          min-inline-size: 10rem;
        }
        .ue-chip {
          display: inline-block;
          padding: 0.1rem 0.45rem;
          border-radius: 0.25rem;
          font-size: 0.8em;
          border: 1px solid var(--mp-border, #e2e8f0);
        }
        .ue-chip--ok {
          background: color-mix(in srgb, var(--mp-success, #16a34a) 18%, transparent);
        }
        .ue-chip--warn {
          background: color-mix(in srgb, var(--mp-warning, #ca8a04) 18%, transparent);
        }
        .ue-chip--muted {
          color: var(--mp-fg-muted, #64748b);
        }
        .ue-detail-panel {
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 0.5rem;
          padding: 0.75rem 1rem;
          display: grid;
          gap: 0.65rem;
        }
        .ue-detail-panel header {
          font-weight: 600;
        }
        .ue-detail-dl {
          display: grid;
          gap: 0.45rem;
          margin: 0;
          grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
        }
        .ue-detail-dl dt {
          font-size: 0.8em;
          color: var(--mp-fg-muted, #64748b);
        }
        .ue-detail-dl dd {
          margin: 0;
          font-weight: 500;
        }
        .ue-panel-body {
          padding: 0.85rem 0.9rem 1rem;
        }
        .ue-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          margin-block-end: 0.4rem;
          font-size: 0.9rem;
        }
        .ue-metrics {
          display: grid;
          gap: 0.65rem;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          margin-block-end: 0.85rem;
        }
        .ue-metric {
          border-radius: 10px;
          padding: 0.75rem 0.85rem;
          border: 1px solid var(--mp-border, #d0d5dd);
          background: var(--mp-surface, #fff);
        }
        .ue-metric-label {
          display: block;
          font-size: 0.75rem;
          color: var(--mp-muted, #667085);
          margin-block-end: 0.25rem;
        }
        .ue-metric strong {
          font-size: 1.25rem;
        }
        .ue-metric--royal {
          border-block-start: 3px solid var(--mp-royal, #1e3a8a);
        }
        .ue-metric--emerald {
          border-block-start: 3px solid var(--mp-emerald, #059669);
        }
        .ue-metric--gold {
          border-block-start: 3px solid var(--mp-gold, #ca8a04);
        }
        .ue-metric--forest {
          border-block-start: 3px solid var(--mp-forest, #166534);
        }
        .ue-metric--orange {
          border-block-start: 3px solid var(--mp-orange, #ea580c);
        }
        .ue-metric--purple {
          border-block-start: 3px solid var(--mp-purple, #7c3aed);
        }
        .ue-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
          margin-block: 0.75rem;
        }
        .ue-tab {
          border: 1px solid var(--mp-border, #d0d5dd);
          background: var(--mp-surface, #fff);
          border-radius: 999px;
          padding: 0.35rem 0.75rem;
          cursor: pointer;
          font-size: 0.85rem;
        }
        .ue-tab--on {
          background: color-mix(in srgb, var(--mp-royal, #1e3a8a) 14%, transparent);
          border-color: color-mix(in srgb, var(--mp-royal, #1e3a8a) 40%, transparent);
        }
        .ue-panel {
          border: 1px solid var(--mp-border, #d0d5dd);
          border-radius: 12px;
          padding: 1rem;
          background: var(--mp-surface, #fff);
        }
        .ue-overview {
          display: grid;
          gap: 1rem;
          grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        }
        .ue-card h2,
        .ue-stack > :global(h2) {
          margin-block: 0 0.75rem;
          font-size: 1rem;
        }
        .ue-stack {
          display: grid;
          gap: 1rem;
        }
      `}</style>
    </PageLayout>
  );
}
