-- P5.2 — University + Inventory Postgres schemas (tenant-isolated, no cross-schema joins)

CREATE SCHEMA IF NOT EXISTS university;
CREATE SCHEMA IF NOT EXISTS inventory;

CREATE TABLE IF NOT EXISTS university.students (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    student_number VARCHAR(32) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    email VARCHAR(256) NOT NULL,
    program_code VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'enrolled',
    identity_user_id VARCHAR(64),
    document_id VARCHAR(64),
    lms_external_id VARCHAR(128),
    lms_provider VARCHAR(64),
    delivery_model VARCHAR(32) NOT NULL DEFAULT 'degree',
    cohort_ref VARCHAR(64),
    enrolled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, student_number)
);

CREATE TABLE IF NOT EXISTS university.courses (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    course_code VARCHAR(32) NOT NULL,
    title VARCHAR(256) NOT NULL,
    credits INT NOT NULL,
    term VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    lms_external_id VARCHAR(128),
    lms_provider VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, course_code)
);

CREATE TABLE IF NOT EXISTS university.grades (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    student_id UUID NOT NULL REFERENCES university.students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES university.courses(id) ON DELETE CASCADE,
    letter_grade VARCHAR(8) NOT NULL,
    posted_by VARCHAR(64),
    posted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_university_students_tenant ON university.students (tenant_id);
CREATE INDEX IF NOT EXISTS idx_university_students_lms
    ON university.students (tenant_id, lms_provider, lms_external_id);
CREATE INDEX IF NOT EXISTS idx_university_courses_tenant ON university.courses (tenant_id);
CREATE INDEX IF NOT EXISTS idx_university_courses_lms
    ON university.courses (tenant_id, lms_provider, lms_external_id);
CREATE INDEX IF NOT EXISTS idx_university_grades_tenant_student
    ON university.grades (tenant_id, student_id);

CREATE TABLE IF NOT EXISTS inventory.stock_levels (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    sku VARCHAR(64) NOT NULL,
    quantity_on_hand NUMERIC(18, 4) NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, sku)
);

CREATE INDEX IF NOT EXISTS idx_inventory_stock_tenant ON inventory.stock_levels (tenant_id);
CREATE INDEX IF NOT EXISTS idx_inventory_stock_tenant_sku ON inventory.stock_levels (tenant_id, sku);
