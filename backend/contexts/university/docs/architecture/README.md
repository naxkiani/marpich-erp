"""University module architecture — CAP-EDU-001 Student Lifecycle (P0).

Owns student enrollment, course offerings, and grade posting.
Communicates via integration events only; reuses Core identity, documents,
workflow, and audit — never duplicates them.

## Persistence (P5.2)

- Memory: default for tests / local without DB
- Postgres: `university.students|courses|grades` when `PERSISTENCE_BACKEND=postgres`
  (migration `034_university_inventory_postgres.sql`)
- Schema isolation: never join `inventory_*` or peer schemas

## Admin UI depth (P17)

`UniversityEducationPage` mirrors Lab/Pharmacy/Clinic care depth for the
academic pipeline — UI-only, no new aggregates:

- StepProgress derived from catalog state (enroll → offer → grade → complete)
- Status filter + StatusChip on students/courses
- Selectable student → detail panel (grades count, jump to post grade)
- `useAutosave` draft for enroll/offer/grade forms (`marpich.university.education.draft`)
"""
