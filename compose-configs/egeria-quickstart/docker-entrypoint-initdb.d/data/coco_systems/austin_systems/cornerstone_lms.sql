-- system-qualified-name: SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110
-- Cornerstone OnDemand LMS - Austin.  GMP training compliance for the Austin site: competencies required per position,
-- learning objects, transcripts, assessments and certifications.  Its tables feed Role Competency Requirements,
-- Training Completions and Worker Qualifications.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS cornerstone_lms;
COMMENT ON SCHEMA cornerstone_lms IS 'Cornerstone OnDemand (Austin portal): users, learning objects, competencies, position requirements, transcripts, test attempts and certifications as landed by the Cornerstone data feed.';

CREATE TABLE IF NOT EXISTS cornerstone_lms.users (
  user_id        varchar(20) NOT NULL,
  user_name      varchar(60) NOT NULL,
  first_name     varchar(80),
  last_name      varchar(80),
  ou_position_id varchar(40) NOT NULL,
  user_status    varchar(20) NOT NULL,
  last_hire_date date,
  CONSTRAINT users_pk PRIMARY KEY (user_id)
);
COMMENT ON TABLE cornerstone_lms.users IS 'Learners fed from Workday (user_id = Workday employee ID; position OU = Workday job profile).';

INSERT INTO cornerstone_lms.users (user_id, user_name, first_name, last_name, ou_position_id, user_status, last_hire_date) VALUES
('100101', 'rhernandez', 'Rebecca', 'Hernandez', 'JP-SITE-HEAD', 'Active', '2014-03-03'),
('100112', 'mwhitfield', 'Marcus', 'Whitfield', 'JP-QA-DIR', 'Active', '2016-06-13'),
('100118', 'praman', 'Priya', 'Raman', 'JP-QA-BDS', 'Active', '2019-01-07'),
('100122', 'bfoster', 'Brian', 'Foster', 'JP-MFG-OP2', 'Inactive', '2021-04-19'),
('100124', 'dokafor', 'Daniel', 'Okafor', 'JP-QC-MGR', 'Active', '2017-09-11'),
('100131', 'sdelgado', 'Sofia', 'Delgado', 'JP-QC-ANL2', 'Active', '2020-08-24'),
('100137', 'ktran', 'Kevin', 'Tran', 'JP-QC-CHROM', 'Active', '2026-02-09'),
('100142', 'jmorales', 'Jason', 'Morales', 'JP-MFG-SUP', 'Active', '2018-05-14'),
('100149', 'abrooks', 'Aaliyah', 'Brooks', 'JP-MFG-OP3', 'Active', '2019-10-07'),
('100153', 'tnguyen', 'Tyler', 'Nguyen', 'JP-MFG-OP3', 'Active', '2022-03-21'),
('100158', 'glindqvist', 'Grace', 'Lindqvist', 'JP-CT-SPEC', 'Active', '2023-01-09'),
('100162', 'ohaddad', 'Omar', 'Haddad', 'JP-WH-LEAD', 'Active', '2018-11-05'),
('100167', 'hkowalski', 'Hannah', 'Kowalski', 'JP-FIN-CTRL', 'Active', '2017-04-03'),
('100171', 'lcarranza', 'Luis', 'Carranza', 'JP-FIN-SRACC', 'Active', '2020-07-13'),
('100176', 'moneill', 'Megan', 'O''Neill', 'JP-FIN-AP', 'Active', '2021-09-20'),
('100180', 'epark', 'Ethan', 'Park', 'JP-PROC-MGR', 'Active', '2019-05-06'),
('100184', 'cbennett', 'Chloe', 'Bennett', 'JP-HR-BP', 'Active', '2020-11-02'),
('100189', 'sadeyemi', 'Samuel', 'Adeyemi', 'JP-LOG-DG', 'Active', '2021-02-15'),
('100193', 'npetrov', 'Nina', 'Petrov', 'JP-ENG-CAL', 'Active', '2019-08-19'),
('100197', 'rcastillo', 'Robert', 'Castillo', 'JP-CQ-SPEC', 'Active', '2022-06-06'),
('100201', 'imoreno', 'Isabel', 'Moreno', 'JP-PV-ASSOC', 'Active', '2026-03-02'),
('100205', 'mjohnson', 'Mia', 'Johnson', 'JP-QC-ANL1', 'Active', '2026-09-08'),
('C00015', 'dshaw.ext', 'Derek', 'Shaw', 'JP-VAL-CONS', 'Active', '2026-06-01')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.competency (
  competency_id           varchar(40) NOT NULL,
  title                   varchar(120) NOT NULL,
  description             text,
  refresh_interval_months integer NOT NULL,
  regulatory_flag         char(1) NOT NULL,
  CONSTRAINT competency_pk PRIMARY KEY (competency_id)
);
COMMENT ON TABLE cornerstone_lms.competency IS 'Competency library.';

INSERT INTO cornerstone_lms.competency (competency_id, title, description, refresh_interval_months, regulatory_flag) VALUES
('CMP-GMP-CORE', 'GMP fundamentals', 'Current good manufacturing practice (21 CFR 210/211), documentation and data integrity', 12, 'Y'),
('CMP-ASEPTIC', 'Aseptic gowning and cleanroom behaviour', 'Grade A/B gowning qualification, aseptic technique and media-fill participation', 6, 'Y'),
('CMP-CYTO', 'Cytotoxic handling', 'Safe handling of hazardous drugs (USP <800>), spill response and closed-system transfer', 12, 'Y'),
('CMP-DG-SHIP', 'Hazardous materials shipping', 'Hazmat employee training (49 CFR 172.704) and IATA DGR for Class 6.1 and dry ice consignments', 24, 'Y'),
('CMP-HPLC', 'Chromatography data system use', 'Empower 3 acquisition, processing and audit trail review', 24, 'N'),
('CMP-BATCH-DISP', 'Batch record review and disposition', 'Review of executed batch records, deviation linkage and release decision', 12, 'Y'),
('CMP-CAL', 'Calibration and metrology', 'Calibration of GMP instruments, tolerances and out-of-tolerance handling', 24, 'N'),
('CMP-SOX-JE', 'Journal entry controls', 'Manual journal preparation, support and approval under SOX 404', 12, 'Y'),
('CMP-AE-INTAKE', 'Adverse event recognition and reporting', 'Recognising and forwarding adverse events within one business day (21 CFR 314.80)', 12, 'Y'),
('CMP-FORKLIFT', 'Powered industrial truck operation', 'Forklift operation and evaluation (OSHA 1910.178)', 36, 'Y'),
('CMP-CELL-PROC', 'Aseptic cell processing', 'Autologous cell processing, chain of identity and cryopreservation', 12, 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.training (
  lo_id        uuid NOT NULL,
  lo_course_no varchar(40) NOT NULL,
  lo_title     varchar(200) NOT NULL,
  lo_type      varchar(40) NOT NULL,
  lo_version   integer NOT NULL,
  lo_active    boolean NOT NULL,
  has_test     boolean NOT NULL,
  CONSTRAINT training_pk PRIMARY KEY (lo_id)
);
COMMENT ON TABLE cornerstone_lms.training IS 'Learning objects (courses, curricula, tests).';

INSERT INTO cornerstone_lms.training (lo_id, lo_course_no, lo_title, lo_type, lo_version, lo_active, has_test) VALUES
('be203aa0-98ed-c635-2d12-139c36fcd20c', 'GMP-101', 'GMP fundamentals (annual/refresher)', 'Online Course', 3, TRUE, TRUE),
('746e31c7-2480-157f-d560-f4f8d65ef2dc', 'ASP-201', 'Aseptic gowning and cleanroom behaviour (annual/refresher)', 'Instructor Led', 3, TRUE, FALSE),
('78e3fcc6-1266-7f1a-cd86-1dea96598fc5', 'CYT-110', 'Cytotoxic handling (annual/refresher)', 'Online Course', 3, TRUE, TRUE),
('5497bcdb-36dd-702c-5a95-f40cf01bffb0', 'DGR-300', 'Hazardous materials shipping', 'Online Course', 3, TRUE, TRUE),
('95d34109-5f02-ee49-8120-bae8ab39eaa6', 'EMP-210', 'Chromatography data system use', 'Online Course', 3, TRUE, FALSE),
('ce775bb0-4a4b-f009-087a-e345d5c245b8', 'BRD-400', 'Batch record review and disposition (annual/refresher)', 'Online Course', 3, TRUE, TRUE),
('f31d7d1f-4b06-ffc1-be7f-28cc60348373', 'CAL-150', 'Calibration and metrology', 'Online Course', 3, TRUE, FALSE),
('a3298955-6a7f-67ca-bd1e-f7d07aaf1da8', 'SOX-120', 'Journal entry controls (annual/refresher)', 'Online Course', 3, TRUE, TRUE),
('e903b4e2-cd09-3ffc-89e3-6bd0b93aaf4c', 'AER-105', 'Adverse event recognition and reporting (annual/refresher)', 'Online Course', 3, TRUE, TRUE),
('f3923f1c-f6f0-4e32-3486-42c2d85913dd', 'PIT-100', 'Powered industrial truck operation', 'Instructor Led', 3, TRUE, FALSE),
('d79d8b96-2edc-a3b4-5573-7726ac302f41', 'CEL-220', 'Aseptic cell processing (annual/refresher)', 'Instructor Led', 3, TRUE, FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.lo_competency (
  lo_id         uuid NOT NULL,
  competency_id varchar(40) NOT NULL,
  CONSTRAINT lo_competency_pk PRIMARY KEY (lo_id, competency_id)
);
COMMENT ON TABLE cornerstone_lms.lo_competency IS 'Competency each learning object evidences.';

INSERT INTO cornerstone_lms.lo_competency (lo_id, competency_id) VALUES
('be203aa0-98ed-c635-2d12-139c36fcd20c', 'CMP-GMP-CORE'),
('746e31c7-2480-157f-d560-f4f8d65ef2dc', 'CMP-ASEPTIC'),
('78e3fcc6-1266-7f1a-cd86-1dea96598fc5', 'CMP-CYTO'),
('5497bcdb-36dd-702c-5a95-f40cf01bffb0', 'CMP-DG-SHIP'),
('95d34109-5f02-ee49-8120-bae8ab39eaa6', 'CMP-HPLC'),
('ce775bb0-4a4b-f009-087a-e345d5c245b8', 'CMP-BATCH-DISP'),
('f31d7d1f-4b06-ffc1-be7f-28cc60348373', 'CMP-CAL'),
('a3298955-6a7f-67ca-bd1e-f7d07aaf1da8', 'CMP-SOX-JE'),
('e903b4e2-cd09-3ffc-89e3-6bd0b93aaf4c', 'CMP-AE-INTAKE'),
('f3923f1c-f6f0-4e32-3486-42c2d85913dd', 'CMP-FORKLIFT'),
('d79d8b96-2edc-a3b4-5573-7726ac302f41', 'CMP-CELL-PROC')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.ou_competency_requirement (
  ou_id          varchar(40) NOT NULL,
  competency_id  varchar(40) NOT NULL,
  effective_date date NOT NULL,
  required       char(1) NOT NULL,
  CONSTRAINT ou_competency_requirement_pk PRIMARY KEY (ou_id, competency_id)
);
COMMENT ON TABLE cornerstone_lms.ou_competency_requirement IS 'Competencies required by position OU (the role-based curriculum).';

INSERT INTO cornerstone_lms.ou_competency_requirement (ou_id, competency_id, effective_date, required) VALUES
('JP-QA-DIR', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-QA-DIR', 'CMP-BATCH-DISP', '2020-01-13', 'Y'),
('JP-QA-BDS', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-QA-BDS', 'CMP-BATCH-DISP', '2020-01-13', 'Y'),
('JP-QC-MGR', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-QC-MGR', 'CMP-CYTO', '2020-01-13', 'Y'),
('JP-QC-ANL2', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-QC-ANL2', 'CMP-HPLC', '2020-01-13', 'Y'),
('JP-QC-ANL1', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-QC-CHROM', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-QC-CHROM', 'CMP-HPLC', '2020-01-13', 'Y'),
('JP-MFG-SUP', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-MFG-SUP', 'CMP-CYTO', '2020-01-13', 'Y'),
('JP-MFG-OP3', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-MFG-OP3', 'CMP-CYTO', '2020-01-13', 'Y'),
('JP-MFG-OP3', 'CMP-ASEPTIC', '2020-01-13', 'Y'),
('JP-MFG-OP2', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-CT-SPEC', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-CT-SPEC', 'CMP-ASEPTIC', '2020-01-13', 'Y'),
('JP-CT-SPEC', 'CMP-CELL-PROC', '2021-09-01', 'Y'),
('JP-WH-LEAD', 'CMP-GMP-CORE', '2020-01-13', 'Y'),
('JP-WH-LEAD', 'CMP-FORKLIFT', '2020-01-13', 'Y'),
('JP-LOG-DG', 'CMP-DG-SHIP', '2020-01-13', 'Y'),
('JP-ENG-CAL', 'CMP-CAL', '2020-01-13', 'Y'),
('JP-CQ-SPEC', 'CMP-AE-INTAKE', '2023-05-15', 'Y'),
('JP-PV-ASSOC', 'CMP-AE-INTAKE', '2023-05-15', 'Y'),
('JP-FIN-CTRL', 'CMP-SOX-JE', '2024-01-01', 'Y'),
('JP-FIN-SRACC', 'CMP-SOX-JE', '2024-01-01', 'Y'),
('JP-VAL-CONS', 'CMP-GMP-CORE', '2020-01-13', 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.transcript (
  reg_num           varchar(20) NOT NULL,
  user_id           varchar(20) NOT NULL,
  lo_id             uuid NOT NULL,
  transcript_status varchar(20) NOT NULL,
  assigned_dt       date NOT NULL,
  due_dt            date,
  completion_dt     date,
  expiration_dt     date,
  session_start_dt  date,
  CONSTRAINT transcript_pk PRIMARY KEY (reg_num)
);
COMMENT ON TABLE cornerstone_lms.transcript IS 'Transcript records: completions, open refresher registrations and scheduled sessions.';

INSERT INTO cornerstone_lms.transcript (reg_num, user_id, lo_id, transcript_status, assigned_dt, due_dt, completion_dt, expiration_dt, session_start_dt) VALUES
('REG-70011', '100112', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-03-14', '2026-03-29', '2026-03-24', '2027-03-24', NULL),
('REG-70022', '100112', 'ce775bb0-4a4b-f009-087a-e345d5c245b8', 'Completed', '2026-06-28', '2026-07-13', '2026-07-08', '2027-07-08', NULL),
('REG-70033', '100118', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-06-05', '2026-06-20', '2026-06-15', '2027-06-15', NULL),
('REG-70044', '100118', 'ce775bb0-4a4b-f009-087a-e345d5c245b8', 'Completed', '2026-05-01', '2026-05-16', '2026-05-11', '2027-05-11', NULL),
('REG-70055', '100122', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-04-16', '2026-05-01', '2026-04-26', '2027-04-26', NULL),
('REG-70066', '100124', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-06-06', '2026-06-21', '2026-06-16', '2027-06-16', NULL),
('REG-70077', '100124', '78e3fcc6-1266-7f1a-cd86-1dea96598fc5', 'Completed', '2026-02-21', '2026-03-08', '2026-03-03', '2027-03-03', NULL),
('REG-70088', '100131', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-04-05', '2026-04-20', '2026-04-15', '2027-04-15', NULL),
('REG-70099', '100131', '95d34109-5f02-ee49-8120-bae8ab39eaa6', 'Completed', '2026-05-09', '2026-05-24', '2026-05-19', '2028-05-19', NULL),
('REG-70110', '100137', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-02-06', '2026-02-21', '2026-02-16', '2027-02-16', NULL),
('REG-70121', '100137', '95d34109-5f02-ee49-8120-bae8ab39eaa6', 'Completed', '2026-02-04', '2026-02-19', '2026-02-14', '2028-02-14', NULL),
('REG-70132', '100142', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-03-09', '2026-03-24', '2026-03-19', '2027-03-19', NULL),
('REG-70143', '100142', '78e3fcc6-1266-7f1a-cd86-1dea96598fc5', 'Completed', '2026-03-20', '2026-04-04', '2026-03-30', '2027-03-30', NULL),
('REG-70154', '100149', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-05-15', '2026-05-30', '2026-05-25', '2027-05-25', NULL),
('REG-70165', '100149', '78e3fcc6-1266-7f1a-cd86-1dea96598fc5', 'Completed', '2026-06-18', '2026-07-03', '2026-06-28', '2027-06-28', NULL),
('REG-70176', '100149', '746e31c7-2480-157f-d560-f4f8d65ef2dc', 'Completed', '2026-03-10', '2026-03-25', '2026-03-20', '2026-09-20', NULL),
('REG-70177', '100149', '746e31c7-2480-157f-d560-f4f8d65ef2dc', 'Past Due', '2026-08-06', '2026-09-20', NULL, NULL, '2026-09-28'),
('REG-70188', '100153', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-01-26', '2026-02-10', '2026-02-05', '2027-02-05', NULL),
('REG-70199', '100153', '78e3fcc6-1266-7f1a-cd86-1dea96598fc5', 'Completed', '2026-01-25', '2026-02-09', '2026-02-04', '2027-02-04', NULL),
('REG-70210', '100153', '746e31c7-2480-157f-d560-f4f8d65ef2dc', 'Completed', '2026-04-16', '2026-05-01', '2026-04-26', '2026-10-26', NULL),
('REG-70211', '100153', '746e31c7-2480-157f-d560-f4f8d65ef2dc', 'Registered', '2026-09-11', '2026-10-26', NULL, NULL, '2026-10-14'),
('REG-70222', '100158', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-05-26', '2026-06-10', '2026-06-05', '2027-06-05', NULL),
('REG-70233', '100158', '746e31c7-2480-157f-d560-f4f8d65ef2dc', 'Completed', '2026-05-06', '2026-05-21', '2026-05-16', '2026-11-16', NULL),
('REG-70234', '100158', '746e31c7-2480-157f-d560-f4f8d65ef2dc', 'Registered', '2026-10-02', '2026-11-16', NULL, NULL, '2026-11-04'),
('REG-70245', '100158', 'd79d8b96-2edc-a3b4-5573-7726ac302f41', 'Completed', '2026-01-05', '2026-01-20', '2026-01-15', '2027-01-15', NULL),
('REG-70256', '100162', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-03-13', '2026-03-28', '2026-03-23', '2027-03-23', NULL),
('REG-70267', '100162', 'f3923f1c-f6f0-4e32-3486-42c2d85913dd', 'Completed', '2023-10-20', '2023-11-04', '2023-10-30', '2026-10-30', NULL),
('REG-70268', '100162', 'f3923f1c-f6f0-4e32-3486-42c2d85913dd', 'Registered', '2026-09-15', '2026-10-30', NULL, NULL, '2026-10-18'),
('REG-70279', '100167', 'a3298955-6a7f-67ca-bd1e-f7d07aaf1da8', 'Completed', '2026-07-05', '2026-07-20', '2026-07-15', '2027-07-15', NULL),
('REG-70290', '100171', 'a3298955-6a7f-67ca-bd1e-f7d07aaf1da8', 'Completed', '2026-06-07', '2026-06-22', '2026-06-17', '2027-06-17', NULL),
('REG-70301', '100189', '5497bcdb-36dd-702c-5a95-f40cf01bffb0', 'Completed', '2026-03-24', '2026-04-08', '2026-04-03', '2028-04-03', NULL),
('REG-70312', '100193', 'f31d7d1f-4b06-ffc1-be7f-28cc60348373', 'Completed', '2024-09-28', '2024-10-13', '2024-10-08', '2026-10-08', NULL),
('REG-70313', '100193', 'f31d7d1f-4b06-ffc1-be7f-28cc60348373', 'Registered', '2026-08-24', '2026-10-08', NULL, NULL, '2026-09-26'),
('REG-70324', '100197', 'e903b4e2-cd09-3ffc-89e3-6bd0b93aaf4c', 'Completed', '2026-07-02', '2026-07-17', '2026-07-12', '2027-07-12', NULL),
('REG-70335', '100201', 'e903b4e2-cd09-3ffc-89e3-6bd0b93aaf4c', 'Completed', '2026-02-24', '2026-03-11', '2026-03-06', '2027-03-06', NULL),
('REG-70346', '100205', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-09-05', '2026-09-20', '2026-09-15', '2027-09-15', NULL),
('REG-70357', 'C00015', 'be203aa0-98ed-c635-2d12-139c36fcd20c', 'Completed', '2026-05-29', '2026-06-13', '2026-06-08', '2027-06-08', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.transcript_test (
  reg_num       varchar(20) NOT NULL,
  attempt_dt    date NOT NULL,
  score         numeric(5,1) NOT NULL,
  passing_score numeric(5,1) NOT NULL,
  passed        char(1) NOT NULL,
  CONSTRAINT transcript_test_pk PRIMARY KEY (reg_num, attempt_dt)
);
COMMENT ON TABLE cornerstone_lms.transcript_test IS 'Test attempts on transcript records.';

INSERT INTO cornerstone_lms.transcript_test (reg_num, attempt_dt, score, passing_score, passed) VALUES
('REG-70011', '2026-03-24', 86.0, 80.0, 'Y'),
('REG-70022', '2026-07-08', 98.0, 80.0, 'Y'),
('REG-70033', '2026-06-15', 96.0, 80.0, 'Y'),
('REG-70044', '2026-05-11', 82.0, 80.0, 'Y'),
('REG-70055', '2026-04-26', 88.0, 80.0, 'Y'),
('REG-70066', '2026-06-16', 85.0, 80.0, 'Y'),
('REG-70077', '2026-03-03', 83.0, 80.0, 'Y'),
('REG-70088', '2026-04-15', 88.0, 80.0, 'Y'),
('REG-70110', '2026-02-16', 87.0, 80.0, 'Y'),
('REG-70132', '2026-03-19', 96.0, 80.0, 'Y'),
('REG-70143', '2026-03-30', 98.0, 80.0, 'Y'),
('REG-70154', '2026-05-25', 93.0, 80.0, 'Y'),
('REG-70165', '2026-06-28', 84.0, 80.0, 'Y'),
('REG-70188', '2026-02-05', 89.0, 80.0, 'Y'),
('REG-70199', '2026-02-02', 72.0, 80.0, 'N'),
('REG-70199', '2026-02-04', 93.0, 80.0, 'Y'),
('REG-70222', '2026-06-05', 87.0, 80.0, 'Y'),
('REG-70256', '2026-03-23', 83.0, 80.0, 'Y'),
('REG-70279', '2026-07-15', 97.0, 80.0, 'Y'),
('REG-70290', '2026-06-17', 96.0, 80.0, 'Y'),
('REG-70301', '2026-04-03', 94.0, 80.0, 'Y'),
('REG-70324', '2026-07-12', 97.0, 80.0, 'Y'),
('REG-70335', '2026-03-06', 98.0, 80.0, 'Y'),
('REG-70346', '2026-09-15', 95.0, 80.0, 'Y'),
('REG-70357', '2026-06-08', 83.0, 80.0, 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS cornerstone_lms.certification_user (
  cert_user_id         varchar(20) NOT NULL,
  user_id              varchar(20) NOT NULL,
  competency_id        varchar(40) NOT NULL,
  certification_number varchar(40) NOT NULL,
  cert_status          varchar(20) NOT NULL,
  acquired_dt          date NOT NULL,
  expiration_dt        date NOT NULL,
  evidence_reg_num     varchar(20) NOT NULL,
  position_ou_id       varchar(40) NOT NULL,
  CONSTRAINT certification_user_pk PRIMARY KEY (cert_user_id)
);
COMMENT ON TABLE cornerstone_lms.certification_user IS 'Certifications held (one per worker and competency), with the transcript that evidences them.';

INSERT INTO cornerstone_lms.certification_user (cert_user_id, user_id, competency_id, certification_number, cert_status, acquired_dt, expiration_dt, evidence_reg_num, position_ou_id) VALUES
('CU-70011', '100112', 'CMP-GMP-CORE', 'CERT-GMP-101-260011', 'Active', '2026-03-24', '2027-03-24', 'REG-70011', 'JP-QA-DIR'),
('CU-70022', '100112', 'CMP-BATCH-DISP', 'CERT-BRD-400-260022', 'Active', '2026-07-08', '2027-07-08', 'REG-70022', 'JP-QA-DIR'),
('CU-70033', '100118', 'CMP-GMP-CORE', 'CERT-GMP-101-260033', 'Active', '2026-06-15', '2027-06-15', 'REG-70033', 'JP-QA-BDS'),
('CU-70044', '100118', 'CMP-BATCH-DISP', 'CERT-BRD-400-260044', 'Active', '2026-05-11', '2027-05-11', 'REG-70044', 'JP-QA-BDS'),
('CU-70055', '100122', 'CMP-GMP-CORE', 'CERT-GMP-101-260055', 'Active', '2026-04-26', '2027-04-26', 'REG-70055', 'JP-MFG-OP2'),
('CU-70066', '100124', 'CMP-GMP-CORE', 'CERT-GMP-101-260066', 'Active', '2026-06-16', '2027-06-16', 'REG-70066', 'JP-QC-MGR'),
('CU-70077', '100124', 'CMP-CYTO', 'CERT-CYT-110-260077', 'Active', '2026-03-03', '2027-03-03', 'REG-70077', 'JP-QC-MGR'),
('CU-70088', '100131', 'CMP-GMP-CORE', 'CERT-GMP-101-260088', 'Active', '2026-04-15', '2027-04-15', 'REG-70088', 'JP-QC-ANL2'),
('CU-70099', '100131', 'CMP-HPLC', 'CERT-EMP-210-260099', 'Active', '2026-05-19', '2028-05-19', 'REG-70099', 'JP-QC-ANL2'),
('CU-70110', '100137', 'CMP-GMP-CORE', 'CERT-GMP-101-260110', 'Active', '2026-02-16', '2027-02-16', 'REG-70110', 'JP-QC-CHROM'),
('CU-70121', '100137', 'CMP-HPLC', 'CERT-EMP-210-260121', 'Active', '2026-02-14', '2028-02-14', 'REG-70121', 'JP-QC-CHROM'),
('CU-70132', '100142', 'CMP-GMP-CORE', 'CERT-GMP-101-260132', 'Active', '2026-03-19', '2027-03-19', 'REG-70132', 'JP-MFG-SUP'),
('CU-70143', '100142', 'CMP-CYTO', 'CERT-CYT-110-260143', 'Active', '2026-03-30', '2027-03-30', 'REG-70143', 'JP-MFG-SUP'),
('CU-70154', '100149', 'CMP-GMP-CORE', 'CERT-GMP-101-260154', 'Active', '2026-05-25', '2027-05-25', 'REG-70154', 'JP-MFG-OP3'),
('CU-70165', '100149', 'CMP-CYTO', 'CERT-CYT-110-260165', 'Active', '2026-06-28', '2027-06-28', 'REG-70165', 'JP-MFG-OP3'),
('CU-70176', '100149', 'CMP-ASEPTIC', 'CERT-ASP-201-260176', 'Expired', '2026-03-20', '2026-09-20', 'REG-70176', 'JP-MFG-OP3'),
('CU-70188', '100153', 'CMP-GMP-CORE', 'CERT-GMP-101-260188', 'Active', '2026-02-05', '2027-02-05', 'REG-70188', 'JP-MFG-OP3'),
('CU-70199', '100153', 'CMP-CYTO', 'CERT-CYT-110-260199', 'Active', '2026-02-04', '2027-02-04', 'REG-70199', 'JP-MFG-OP3'),
('CU-70210', '100153', 'CMP-ASEPTIC', 'CERT-ASP-201-260210', 'Expiring', '2026-04-26', '2026-10-26', 'REG-70210', 'JP-MFG-OP3'),
('CU-70222', '100158', 'CMP-GMP-CORE', 'CERT-GMP-101-260222', 'Active', '2026-06-05', '2027-06-05', 'REG-70222', 'JP-CT-SPEC'),
('CU-70233', '100158', 'CMP-ASEPTIC', 'CERT-ASP-201-260233', 'Expiring', '2026-05-16', '2026-11-16', 'REG-70233', 'JP-CT-SPEC'),
('CU-70245', '100158', 'CMP-CELL-PROC', 'CERT-CEL-220-260245', 'Active', '2026-01-15', '2027-01-15', 'REG-70245', 'JP-CT-SPEC'),
('CU-70256', '100162', 'CMP-GMP-CORE', 'CERT-GMP-101-260256', 'Active', '2026-03-23', '2027-03-23', 'REG-70256', 'JP-WH-LEAD'),
('CU-70267', '100162', 'CMP-FORKLIFT', 'CERT-PIT-100-230267', 'Expiring', '2023-10-30', '2026-10-30', 'REG-70267', 'JP-WH-LEAD'),
('CU-70279', '100167', 'CMP-SOX-JE', 'CERT-SOX-120-260279', 'Active', '2026-07-15', '2027-07-15', 'REG-70279', 'JP-FIN-CTRL'),
('CU-70290', '100171', 'CMP-SOX-JE', 'CERT-SOX-120-260290', 'Active', '2026-06-17', '2027-06-17', 'REG-70290', 'JP-FIN-SRACC'),
('CU-70301', '100189', 'CMP-DG-SHIP', 'CERT-DGR-300-260301', 'Active', '2026-04-03', '2028-04-03', 'REG-70301', 'JP-LOG-DG'),
('CU-70312', '100193', 'CMP-CAL', 'CERT-CAL-150-240312', 'Expiring', '2024-10-08', '2026-10-08', 'REG-70312', 'JP-ENG-CAL'),
('CU-70324', '100197', 'CMP-AE-INTAKE', 'CERT-AER-105-260324', 'Active', '2026-07-12', '2027-07-12', 'REG-70324', 'JP-CQ-SPEC'),
('CU-70335', '100201', 'CMP-AE-INTAKE', 'CERT-AER-105-260335', 'Active', '2026-03-06', '2027-03-06', 'REG-70335', 'JP-PV-ASSOC'),
('CU-70346', '100205', 'CMP-GMP-CORE', 'CERT-GMP-101-260346', 'Active', '2026-09-15', '2027-09-15', 'REG-70346', 'JP-QC-ANL1'),
('CU-70357', 'C00015', 'CMP-GMP-CORE', 'CERT-GMP-101-260357', 'Active', '2026-06-08', '2027-06-08', 'REG-70357', 'JP-VAL-CONS')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/cornerstone_lms).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS cornerstone_lms.compliance_alert (
  alert_id      varchar(40) NOT NULL,
  user_id       varchar(20) NOT NULL,
  competency_id varchar(40) NOT NULL,
  expiration_dt date NOT NULL,
  raised_dt     timestamptz NOT NULL,
  alert_type    varchar(20) NOT NULL,
  due_dt        date NOT NULL,
  CONSTRAINT compliance_alert_pk PRIMARY KEY (alert_id)
);
COMMENT ON TABLE cornerstone_lms.compliance_alert IS 'Qualification expiry warnings received for learners; the administrator assigns the refresher from here.';

GRANT USAGE ON SCHEMA cornerstone_lms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA cornerstone_lms TO egeria_user, airflow_user;
