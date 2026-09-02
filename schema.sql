-- =====================================================================
-- schema.sql
-- PostgreSQL schema for the Assignment Design Assistant
-- Unit: H6S9 46 Computing: Applications Development
-- =====================================================================
-- Run with:  psql "$DATABASE_URL" -f schema.sql
-- (The Flask app also creates this table automatically on first run
--  via SQLAlchemy, so running this file by hand is optional.)
-- =====================================================================

CREATE TABLE IF NOT EXISTS assignment_responses (
    id                      SERIAL PRIMARY KEY,

    -- ---- Student / cover sheet details -------------------------------
    student_usn             VARCHAR(50)  NOT NULL,
    student_name            VARCHAR(150) NOT NULL,
    tutor_name              VARCHAR(150),
    unit_code               VARCHAR(50)  DEFAULT 'H6S9 46',
    unit_title               VARCHAR(200) DEFAULT 'Computing: Applications Development',
    date_due                DATE,
    date_submitted          DATE,

    -- ---- Application basics -------------------------------------------
    app_name                VARCHAR(200),
    app_type                VARCHAR(100),   -- Mobile / Game / Business / Web / Other
    dev_environment         VARCHAR(150),   -- e.g. Python (VS Code), MIT App Inventor, Scratch, Java (BlueJ)

    -- ---- Task A: Outcome 1 - Design Document ---------------------------
    task_1_1_proposal              TEXT,   -- Application proposal (>=300 words)
    task_1_2_resources             TEXT,   -- Resources list & justification
    task_1_3_action_plan           TEXT,   -- Action plan / milestones / timescales
    task_1_4_design_diagrams       TEXT,   -- Description / links to design diagrams

    -- ---- Task B: Outcome 2 - Application Development --------------------
    task_2_1_build_summary         TEXT,   -- Summary of what was built, constructs used
    task_2_2_project_log           TEXT,   -- Decisions, problems, solutions log

    -- ---- Task C: Outcome 3 - Testing -------------------------------------
    task_3_1_testing_evidence      TEXT,   -- Test case summary (full cases live in Excel)
    task_3_2_error_log             TEXT,   -- Errors found & fixes made
    task_3_3_demo_notes            TEXT,   -- Notes on the 2-3 min demo video

    -- ---- Task D: Outcome 4 - Evaluation Report -----------------------------
    task_4_1_eval_design           TEXT,   -- Evaluation of the design document
    task_4_2_eval_process          TEXT,   -- Evaluation of the development process
    task_4_3_eval_application      TEXT,   -- Evaluation of the final application
    task_4_4_future_actions        TEXT,   -- Action points for future development
    task_4_5_self_evaluation       TEXT,   -- Self-evaluation of personal performance

    -- ---- Bookkeeping -----------------------------------------------------
    status                  VARCHAR(20)  DEFAULT 'draft',   -- draft / submitted
    created_at              TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_assignment_responses_usn ON assignment_responses (student_usn);
CREATE INDEX IF NOT EXISTS idx_assignment_responses_status ON assignment_responses (status);

-- Keep updated_at current on every UPDATE
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_assignment_responses_updated_at ON assignment_responses;
CREATE TRIGGER trg_assignment_responses_updated_at
    BEFORE UPDATE ON assignment_responses
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();
