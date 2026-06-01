-- =============================================================
--  Hospital Patient Database  –  PostgreSQL Schema v2
--  Includes: DICOM fields, created_by/updated_by/updated_at,
--            audit_log table and automatic trigger
-- =============================================================

-- Enable pgcrypto for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- =============================================================
--  SECTION 1 – LOOKUP / REFERENCE TABLES
-- =============================================================

-- ------------------------------------------------------------------
--  department
-- ------------------------------------------------------------------
CREATE TABLE department (
    department_id       UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    name                VARCHAR(120)    NOT NULL,
    code                VARCHAR(20)     NOT NULL UNIQUE,
    location            VARCHAR(120),
    head_clinician_id   UUID,                       -- FK added below (forward ref)
    created_by          UUID            NOT NULL,   -- FK to clinician
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID,                       -- FK to clinician
    updated_at          TIMESTAMPTZ
);

-- ------------------------------------------------------------------
--  clinician
-- ------------------------------------------------------------------
CREATE TABLE clinician (
    clinician_id        UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name          VARCHAR(80)     NOT NULL,
    last_name           VARCHAR(80)     NOT NULL,
    role                VARCHAR(80)     NOT NULL,   -- e.g. 'Consultant', 'Registrar', 'Nurse'
    department_id       UUID            NOT NULL REFERENCES department(department_id),
    gmc_number          VARCHAR(20)     UNIQUE,     -- NMC pin for nurses, GMC for doctors
    created_by          UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID            REFERENCES clinician(clinician_id),
    updated_at          TIMESTAMPTZ
);

-- Now that clinician exists, add the deferred FK on department
ALTER TABLE department
    ADD CONSTRAINT fk_dept_head    FOREIGN KEY (head_clinician_id) REFERENCES clinician(clinician_id),
    ADD CONSTRAINT fk_dept_created FOREIGN KEY (created_by)        REFERENCES clinician(clinician_id),
    ADD CONSTRAINT fk_dept_updated FOREIGN KEY (updated_by)        REFERENCES clinician(clinician_id);


-- =============================================================
--  SECTION 2 – PATIENT
-- =============================================================

CREATE TABLE patient (
    patient_id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    nhs_number          CHAR(10)        NOT NULL UNIQUE,    -- 10-digit NHS number
    first_name          VARCHAR(80)     NOT NULL,
    last_name           VARCHAR(80)     NOT NULL,
    date_of_birth       DATE            NOT NULL,
    sex                 VARCHAR(20),                        -- 'Male','Female','Non-binary', etc.
    address             TEXT,
    postcode            VARCHAR(10),
    phone               VARCHAR(20),
    email               VARCHAR(120),
    emergency_contact   TEXT,
    blood_type          VARCHAR(5),                         -- e.g. 'A+', 'O-'
    allergies           TEXT,                               -- free text; structured allergy table optional
    created_by          UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID            REFERENCES clinician(clinician_id),
    updated_at          TIMESTAMPTZ
);

CREATE INDEX idx_patient_nhs    ON patient(nhs_number);
CREATE INDEX idx_patient_name   ON patient(last_name, first_name);
CREATE INDEX idx_patient_dob    ON patient(date_of_birth);


-- =============================================================
--  SECTION 3 – VISIT
-- =============================================================

CREATE TABLE visit (
    visit_id                UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id              UUID            NOT NULL REFERENCES patient(patient_id),
    department_id           UUID            NOT NULL REFERENCES department(department_id),
    attending_clinician_id  UUID            NOT NULL REFERENCES clinician(clinician_id),
    admitted_at             TIMESTAMPTZ     NOT NULL DEFAULT now(),
    discharged_at           TIMESTAMPTZ,
    visit_type              VARCHAR(40)     NOT NULL,   -- 'Inpatient','Outpatient','Emergency','Day case'
    reason                  TEXT,
    discharge_notes         TEXT,
    created_by              UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at              TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by              UUID            REFERENCES clinician(clinician_id),
    updated_at              TIMESTAMPTZ
);

CREATE INDEX idx_visit_patient ON visit(patient_id);
CREATE INDEX idx_visit_dept    ON visit(department_id);
CREATE INDEX idx_visit_dates   ON visit(admitted_at, discharged_at);


-- =============================================================
--  SECTION 4 – TREATMENT
-- =============================================================

CREATE TABLE treatment (
    treatment_id        UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id            UUID            NOT NULL REFERENCES visit(visit_id),
    department_id       UUID            NOT NULL REFERENCES department(department_id),
    clinician_id        UUID            NOT NULL REFERENCES clinician(clinician_id),
    treatment_type      VARCHAR(80)     NOT NULL,   -- e.g. 'Medication','Surgery','Physiotherapy'
    description         VARCHAR(255)    NOT NULL,
    notes               TEXT,
    performed_at        TIMESTAMPTZ     NOT NULL DEFAULT now(),
    created_by          UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID            REFERENCES clinician(clinician_id),
    updated_at          TIMESTAMPTZ
);

CREATE INDEX idx_treatment_visit ON treatment(visit_id);


-- =============================================================
--  SECTION 5 – MEASUREMENT
--  Flexible type/value/unit model – add new measurement kinds
--  without any schema changes.
-- =============================================================

CREATE TABLE measurement (
    measurement_id      UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id            UUID            NOT NULL REFERENCES visit(visit_id),
    clinician_id        UUID            NOT NULL REFERENCES clinician(clinician_id),
    measured_at         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    type                VARCHAR(80)     NOT NULL,   -- 'Height','Weight','Systolic BP','SpO2', etc.
    value               NUMERIC(10,4)   NOT NULL,
    unit                VARCHAR(20)     NOT NULL,   -- 'cm','kg','mmHg','%', etc.
    notes               TEXT,
    created_by          UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID            REFERENCES clinician(clinician_id),
    updated_at          TIMESTAMPTZ
);

CREATE INDEX idx_measurement_visit ON measurement(visit_id);
CREATE INDEX idx_measurement_type  ON measurement(type);


-- =============================================================
--  SECTION 6 – LAB RESULT
--  One row per analyte; group related tests with the same
--  sample_type + collected_at + panel combination.
-- =============================================================

CREATE TABLE lab_result (
    result_id           UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id            UUID            NOT NULL REFERENCES visit(visit_id),
    clinician_id        UUID            NOT NULL REFERENCES clinician(clinician_id),
    sample_type         VARCHAR(40)     NOT NULL,   -- 'Blood','Urine','Biopsy','CSF', etc.
    collected_at        TIMESTAMPTZ     NOT NULL,
    resulted_at         TIMESTAMPTZ,
    panel               VARCHAR(80),                -- e.g. 'FBC','U&E','LFT','Histology'
    analyte             VARCHAR(80)     NOT NULL,   -- e.g. 'Haemoglobin','Sodium','ALT'
    value               NUMERIC(12,4),              -- NULL for qualitative results
    value_text          VARCHAR(120),               -- for qualitative: 'Positive','No growth', etc.
    unit                VARCHAR(20),
    reference_range     VARCHAR(40),                -- e.g. '130-170'
    flag                VARCHAR(10),                -- 'H','L','HH','LL','A' (abnormal), etc.
    created_by          UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID            REFERENCES clinician(clinician_id),
    updated_at          TIMESTAMPTZ
);

CREATE INDEX idx_labresult_visit   ON lab_result(visit_id);
CREATE INDEX idx_labresult_analyte ON lab_result(analyte);


-- =============================================================
--  SECTION 7 – MEDICAL IMAGE
--  File content is stored on the file system / PACS / object store.
--  This table holds metadata and the path/URI to the file.
--
--  DICOM standard identifiers:
--    dicom_study_uid    – StudyInstanceUID   (groups all series in one study)
--    dicom_series_uid   – SeriesInstanceUID  (groups images in one acquisition run)
--    dicom_sop_uid      – SOPInstanceUID     (uniquely identifies one image/object)
--    dicom_patient_id   – PatientID tag in the DICOM header (may differ from NHS no.)
--    dicom_accession_no – AccessionNumber    (links to the radiology order / RIS)
--    dicom_institution  – InstitutionName    (sending site, useful in multi-site setups)
-- =============================================================

CREATE TABLE medical_image (
    image_id            UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id            UUID            NOT NULL REFERENCES visit(visit_id),
    clinician_id        UUID            NOT NULL REFERENCES clinician(clinician_id),
    modality            VARCHAR(20)     NOT NULL,   -- 'CR','DX','CT','MR','US','NM','PT', etc.
    body_part           VARCHAR(80),                -- e.g. 'Chest','Left knee'
    captured_at         TIMESTAMPTZ     NOT NULL,

    -- File reference
    file_path           TEXT            NOT NULL,   -- absolute path, relative path, or s3:// URI
    file_format         VARCHAR(20),                -- 'DICOM','JPEG','PNG','TIFF'
    file_size_bytes     BIGINT,

    -- DICOM identifiers
    dicom_study_uid     VARCHAR(64),                -- StudyInstanceUID  (up to 64 chars, UID syntax)
    dicom_series_uid    VARCHAR(64),                -- SeriesInstanceUID
    dicom_sop_uid       VARCHAR(64) UNIQUE,         -- SOPInstanceUID – globally unique per object
    dicom_patient_id    VARCHAR(64),                -- PatientID tag inside DICOM header
    dicom_accession_no  VARCHAR(64),                -- AccessionNumber – ties to radiology order
    dicom_institution   VARCHAR(120),               -- InstitutionName from DICOM header

    -- Radiologist report
    report              TEXT,
    report_by           VARCHAR(120),               -- reporting radiologist name / GMC

    created_by          UUID            NOT NULL REFERENCES clinician(clinician_id),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_by          UUID            REFERENCES clinician(clinician_id),
    updated_at          TIMESTAMPTZ
);

CREATE INDEX idx_image_visit         ON medical_image(visit_id);
CREATE INDEX idx_image_study_uid     ON medical_image(dicom_study_uid);
CREATE INDEX idx_image_series_uid    ON medical_image(dicom_series_uid);
CREATE INDEX idx_image_sop_uid       ON medical_image(dicom_sop_uid);
CREATE INDEX idx_image_accession     ON medical_image(dicom_accession_no);


-- =============================================================
--  SECTION 8 – AUDIT LOG
--
--  One row is written for every INSERT, UPDATE, or DELETE on
--  any of the clinical tables.  The trigger function below
--  handles this automatically – application code does not need
--  to write audit rows explicitly.
--
--  old_data / new_data store the full row as JSONB so any
--  field change is captured without altering this table.
-- =============================================================

CREATE TABLE audit_log (
    log_id          BIGSERIAL       PRIMARY KEY,
    table_name      VARCHAR(60)     NOT NULL,
    record_id       UUID            NOT NULL,       -- PK of the affected row
    operation       CHAR(6)         NOT NULL        -- 'INSERT','UPDATE','DELETE'
                        CHECK (operation IN ('INSERT','UPDATE','DELETE')),
    performed_by    UUID            REFERENCES clinician(clinician_id),
    performed_at    TIMESTAMPTZ     NOT NULL DEFAULT now(),
    old_data        JSONB,                          -- NULL on INSERT
    new_data        JSONB,                          -- NULL on DELETE
    ip_address      INET,                           -- set by application via SET LOCAL
    application     VARCHAR(80)                     -- e.g. 'EPR','HL7-Gateway','API'
);

CREATE INDEX idx_audit_table      ON audit_log(table_name);
CREATE INDEX idx_audit_record     ON audit_log(record_id);
CREATE INDEX idx_audit_clinician  ON audit_log(performed_by);
CREATE INDEX idx_audit_when       ON audit_log(performed_at);


-- =============================================================
--  SECTION 9 – AUDIT TRIGGER FUNCTION
--
--  The application is expected to call:
--      SET LOCAL app.current_clinician_id = '<uuid>';
--      SET LOCAL app.ip_address           = '<ip>';
--      SET LOCAL app.application_name     = 'EPR';
--  inside every transaction before DML, so the trigger can
--  pick up the actor context without altering table signatures.
-- =============================================================

CREATE OR REPLACE FUNCTION fn_audit_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_record_id     UUID;
    v_old_data      JSONB;
    v_new_data      JSONB;
    v_clinician_id  UUID;
    v_ip            INET;
    v_app           VARCHAR(80);
BEGIN
    -- Retrieve actor context set by the application layer
    BEGIN
        v_clinician_id := current_setting('app.current_clinician_id', true)::UUID;
    EXCEPTION WHEN OTHERS THEN
        v_clinician_id := NULL;
    END;

    BEGIN
        v_ip := current_setting('app.ip_address', true)::INET;
    EXCEPTION WHEN OTHERS THEN
        v_ip := NULL;
    END;

    v_app := current_setting('app.application_name', true);

    IF TG_OP = 'DELETE' THEN
        v_record_id := (row_to_json(OLD) ->> (TG_TABLE_NAME || '_id'))::UUID;
        v_old_data  := row_to_json(OLD)::JSONB;
        v_new_data  := NULL;
    ELSIF TG_OP = 'INSERT' THEN
        v_record_id := (row_to_json(NEW) ->> (TG_TABLE_NAME || '_id'))::UUID;
        v_old_data  := NULL;
        v_new_data  := row_to_json(NEW)::JSONB;
    ELSE  -- UPDATE
        v_record_id := (row_to_json(NEW) ->> (TG_TABLE_NAME || '_id'))::UUID;
        v_old_data  := row_to_json(OLD)::JSONB;
        v_new_data  := row_to_json(NEW)::JSONB;
    END IF;

    INSERT INTO audit_log (
        table_name, record_id, operation,
        performed_by, performed_at,
        old_data, new_data,
        ip_address, application
    ) VALUES (
        TG_TABLE_NAME, v_record_id, TG_OP,
        v_clinician_id, now(),
        v_old_data, v_new_data,
        v_ip, v_app
    );

    RETURN NULL;  -- AFTER trigger; return value ignored
END;
$$;


-- =============================================================
--  SECTION 10 – ATTACH AUDIT TRIGGER TO ALL CLINICAL TABLES
-- =============================================================

CREATE TRIGGER trg_audit_patient
    AFTER INSERT OR UPDATE OR DELETE ON patient
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_visit
    AFTER INSERT OR UPDATE OR DELETE ON visit
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_department
    AFTER INSERT OR UPDATE OR DELETE ON department
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_clinician
    AFTER INSERT OR UPDATE OR DELETE ON clinician
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_treatment
    AFTER INSERT OR UPDATE OR DELETE ON treatment
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_measurement
    AFTER INSERT OR UPDATE OR DELETE ON measurement
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_lab_result
    AFTER INSERT OR UPDATE OR DELETE ON lab_result
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER trg_audit_medical_image
    AFTER INSERT OR UPDATE OR DELETE ON medical_image
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();


-- =============================================================
--  SECTION 11 – updated_at TRIGGER
--  Automatically stamps updated_at on every UPDATE so
--  application code never needs to set it manually.
-- =============================================================

CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_updated_patient
    BEFORE UPDATE ON patient
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_visit
    BEFORE UPDATE ON visit
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_department
    BEFORE UPDATE ON department
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_clinician
    BEFORE UPDATE ON clinician
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_treatment
    BEFORE UPDATE ON treatment
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_measurement
    BEFORE UPDATE ON measurement
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_lab_result
    BEFORE UPDATE ON lab_result
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_updated_medical_image
    BEFORE UPDATE ON medical_image
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();


-- =============================================================
--  USAGE NOTES
--
--  Application transaction pattern:
--
--      BEGIN;
--        SET LOCAL app.current_clinician_id = 'xxxxxxxx-...';
--        SET LOCAL app.ip_address           = '10.0.1.42';
--        SET LOCAL app.application_name     = 'EPR';
--        -- your INSERT / UPDATE / DELETE statements
--      COMMIT;
--
--  The audit trigger captures old_data and new_data as JSONB,
--  so you can query changes like this:
--
--      SELECT performed_at, performed_by,
--             old_data->>'discharge_notes' AS before,
--             new_data->>'discharge_notes' AS after
--      FROM   audit_log
--      WHERE  table_name = 'visit'
--        AND  record_id  = '<visit_uuid>'
--      ORDER  BY performed_at;
--
--  DICOM integration notes:
--    dicom_sop_uid has a UNIQUE constraint – inserting the same
--    DICOM object twice will raise a conflict, which is the
--    correct behaviour (idempotent PACS ingest).
--    dicom_study_uid / dicom_series_uid are indexed so you can
--    efficiently retrieve all images belonging to a study or series.
-- =============================================================
