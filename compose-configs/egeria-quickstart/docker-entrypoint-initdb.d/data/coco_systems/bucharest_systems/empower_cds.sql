-- system-qualified-name: SoftwareServer::SYS-027::Empower Chromatography
-- Empower Chromatography - Bucharest.  Waters Empower 3 chromatography data system of the EKG QC laboratory (HPLC
-- RO10-HPLC-02): sample sets, injections and processed results for finished-product assay and related substances.  Its
-- tables feed Laboratory Test Results.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS empower_cds;
COMMENT ON SCHEMA empower_cds IS 'Waters Empower 3 (EKG): sample set, injection and result as exported through the Empower Toolkit reporting view.';

CREATE TABLE IF NOT EXISTS empower_cds.sample_set (
  sample_set_id     integer NOT NULL,
  sample_set_name   varchar(60) NOT NULL,
  acquired_by       varchar(20) NOT NULL,
  acquisition_start timestamptz NOT NULL,
  system_name       varchar(40) NOT NULL,
  CONSTRAINT sample_set_pk PRIMARY KEY (sample_set_id)
);
COMMENT ON TABLE empower_cds.sample_set IS 'Sample sets acquired (acquired_by LABCC01 = the shared local account removed on 2026-08-31, Trackwise TWD-000481).';

INSERT INTO empower_cds.sample_set (sample_set_id, sample_set_name, acquired_by, acquisition_start, system_name) VALUES
(3301, 'EK26-0311_ASSAY_RS', 'LABCC01', '2026-07-09 19:00:00+00', 'RO10-HPLC-02'),
(3302, 'EK26-0318_ASSAY_RS', 'LABCC01', '2026-07-23 17:00:00+00', 'RO10-HPLC-02'),
(3303, 'EK26-0324_ASSAY_RS', 'LABCC01', '2026-08-06 18:00:00+00', 'RO10-HPLC-02'),
(3304, 'EK26-0329_ASSAY_RS', 'LABCC01', '2026-08-20 19:00:00+00', 'RO10-HPLC-02'),
(3305, 'EK26-0335_ASSAY_RS', 'imoldovan', '2026-09-03 19:00:00+00', 'RO10-HPLC-02'),
(3306, 'EK26-0341_ASSAY_RS', 'epopescu', '2026-09-17 18:00:00+00', 'RO10-HPLC-02')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS empower_cds.injection (
  injection_id  integer NOT NULL,
  sample_set_id integer NOT NULL,
  sample_name   varchar(40) NOT NULL,
  label         varchar(10),
  vial          varchar(10),
  injection_no  integer NOT NULL,
  date_acquired timestamptz NOT NULL,
  CONSTRAINT injection_pk PRIMARY KEY (injection_id)
);
COMMENT ON TABLE empower_cds.injection IS 'Injections (sample name = LIMS sample text ID).';

INSERT INTO empower_cds.injection (injection_id, sample_set_id, sample_name, label, vial, injection_no, date_acquired) VALUES
(91001, 3301, 'S26-26025', 'U', '1:A,3', 1, '2026-07-09 19:18:00+00'),
(91002, 3301, 'S26-26025', 'U', '1:A,4', 2, '2026-07-09 19:36:00+00'),
(91003, 3302, 'S26-26026', 'U', '1:A,3', 1, '2026-07-23 17:18:00+00'),
(91004, 3302, 'S26-26026', 'U', '1:A,4', 2, '2026-07-23 17:36:00+00'),
(91005, 3303, 'S26-26027', 'U', '1:A,3', 1, '2026-08-06 18:18:00+00'),
(91006, 3303, 'S26-26027', 'U', '1:A,4', 2, '2026-08-06 18:36:00+00'),
(91007, 3304, 'S26-26028', 'U', '1:A,3', 1, '2026-08-20 19:18:00+00'),
(91008, 3304, 'S26-26028', 'U', '1:A,4', 2, '2026-08-20 19:36:00+00'),
(91009, 3305, 'S26-26029', 'U', '1:A,3', 1, '2026-09-03 19:18:00+00'),
(91010, 3305, 'S26-26029', 'U', '1:A,4', 2, '2026-09-03 19:36:00+00'),
(91011, 3306, 'S26-26031', 'U', '1:A,3', 1, '2026-09-17 18:18:00+00'),
(91012, 3306, 'S26-26031', 'U', '1:A,4', 2, '2026-09-17 18:36:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS empower_cds.result (
  result_id         integer NOT NULL,
  injection_id      integer NOT NULL,
  processing_method varchar(60) NOT NULL,
  cf_test_code      varchar(40) NOT NULL,
  cf_reported_value varchar(20) NOT NULL,
  cf_units          varchar(20),
  cf_spec_min       varchar(20),
  cf_spec_max       varchar(20),
  cf_pass_fail      varchar(4) NOT NULL,
  processed_by      varchar(20) NOT NULL,
  date_processed    timestamptz NOT NULL,
  signoff_status    varchar(20) NOT NULL,
  CONSTRAINT result_pk PRIMARY KEY (result_id)
);
COMMENT ON TABLE empower_cds.result IS 'Processed results with custom fields for the reported value and specification; signoff Approved/Pending.';

INSERT INTO empower_cds.result (result_id, injection_id, processing_method, cf_test_code, cf_reported_value, cf_units, cf_spec_min, cf_spec_max, cf_pass_fail, processed_by, date_processed, signoff_status) VALUES
(440001, 91002, 'PF-1101_HPLC_DOZARE', 'HPLC_DOZARE', '99.7', '%', '95.0', '105.0', 'Pass', 'LABCC01', '2026-07-10 00:00:00+00', 'Approved'),
(440002, 91002, 'PF-1101_HPLC_IMPURITATI', 'HPLC_IMPURITATI', '0.36', '%', NULL, '1.0', 'Pass', 'LABCC01', '2026-07-10 00:00:00+00', 'Approved'),
(440003, 91004, 'PF-1102_HPLC_DOZARE', 'HPLC_DOZARE', '100.7', '%', '95.0', '105.0', 'Pass', 'LABCC01', '2026-07-23 22:00:00+00', 'Approved'),
(440004, 91004, 'PF-1102_HPLC_IMPURITATI', 'HPLC_IMPURITATI', '0.34', '%', NULL, '1.0', 'Pass', 'LABCC01', '2026-07-23 22:00:00+00', 'Approved'),
(440005, 91006, 'PF-1105_HPLC_DOZARE', 'HPLC_DOZARE', '99.7', '%', '95.0', '105.0', 'Pass', 'LABCC01', '2026-08-06 23:00:00+00', 'Approved'),
(440006, 91006, 'PF-1105_HPLC_IMPURITATI', 'HPLC_IMPURITATI', '0.25', '%', NULL, '1.0', 'Pass', 'LABCC01', '2026-08-06 23:00:00+00', 'Approved'),
(440007, 91008, 'PF-1101_HPLC_DOZARE', 'HPLC_DOZARE', '99.1', '%', '95.0', '105.0', 'Pass', 'LABCC01', '2026-08-21 00:00:00+00', 'Approved'),
(440008, 91008, 'PF-1101_HPLC_IMPURITATI', 'HPLC_IMPURITATI', '0.32', '%', NULL, '1.0', 'Pass', 'LABCC01', '2026-08-21 00:00:00+00', 'Approved'),
(440009, 91010, 'PF-1103_HPLC_DOZARE', 'HPLC_DOZARE', '100.7', '%', '95.0', '105.0', 'Pass', 'imoldovan', '2026-09-04 00:00:00+00', 'Approved'),
(440010, 91010, 'PF-1103_HPLC_IMPURITATI', 'HPLC_IMPURITATI', '0.41', '%', NULL, '1.0', 'Pass', 'imoldovan', '2026-09-04 00:00:00+00', 'Approved'),
(440011, 91012, 'PF-1104_HPLC_DOZARE', 'HPLC_DOZARE', '99.8', '%', '95.0', '105.0', 'Pass', 'epopescu', '2026-09-17 23:00:00+00', 'Approved'),
(440012, 91012, 'PF-1104_HPLC_IMPURITATI', 'HPLC_IMPURITATI', '0.20', '%', NULL, '1.0', 'Pass', 'epopescu', '2026-09-17 23:00:00+00', 'Pending')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA empower_cds TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA empower_cds TO egeria_user, airflow_user;
