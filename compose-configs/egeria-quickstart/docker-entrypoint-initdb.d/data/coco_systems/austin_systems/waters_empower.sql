-- system-qualified-name: SoftwareServer::AUS-SYS-027::SN-CHR-AU-20180615
-- Waters Empower 3 - Austin.  The Austin chromatography data system: HPLC/UPLC sample sets, injections and signed-off
-- results for assay and impurities.  Its tables feed Laboratory Test Results (chromatographic results).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS waters_empower;
COMMENT ON SCHEMA waters_empower IS 'Waters Empower 3 (Austin QC laboratory): sample sets, injections and results with custom fields, as landed by the Empower Toolkit reporting export.';

CREATE TABLE IF NOT EXISTS waters_empower.sample_set (
  sample_set_id     integer NOT NULL,
  sample_set_name   varchar(60) NOT NULL,
  acquired_by       varchar(20) NOT NULL,
  acquisition_start timestamptz NOT NULL,
  system_name       varchar(40) NOT NULL,
  CONSTRAINT sample_set_pk PRIMARY KEY (sample_set_id)
);
COMMENT ON TABLE waters_empower.sample_set IS 'Acquired sample sets per instrument run.';

INSERT INTO waters_empower.sample_set (sample_set_id, sample_set_name, acquired_by, acquisition_start, system_name) VALUES
(7701, 'SS_20260702_ASS', 'ktran', '2026-07-02 07:30:00+00', 'US10-HPLC-04'),
(7702, 'SS_20260716_ASS', 'ktran', '2026-07-16 07:30:00+00', 'US10-HPLC-04'),
(7703, 'SS_20260724_ASS', 'ktran', '2026-07-24 07:30:00+00', 'US10-HPLC-04'),
(7704, 'SS_20260725_ASS', 'ktran', '2026-07-25 07:30:00+00', 'US10-HPLC-04'),
(7705, 'SS_20260809_ASS', 'ktran', '2026-08-09 07:30:00+00', 'US10-HPLC-04'),
(7706, 'SS_20260810_IMP', 'ktran', '2026-08-10 07:30:00+00', 'US10-HPLC-04'),
(7707, 'SS_20260821_ASS', 'ktran', '2026-08-21 07:30:00+00', 'US10-HPLC-04'),
(7708, 'SS_20260823_ASS', 'ktran', '2026-08-23 07:30:00+00', 'US10-HPLC-04'),
(7709, 'SS_20260824_IMP', 'ktran', '2026-08-24 07:30:00+00', 'US10-HPLC-04'),
(7710, 'SS_20260827_ASS', 'ktran', '2026-08-27 07:30:00+00', 'US10-HPLC-04'),
(7711, 'SS_20260906_ASS', 'ktran', '2026-09-06 07:30:00+00', 'US10-HPLC-04'),
(7712, 'SS_20260913_ASS', 'ktran', '2026-09-13 07:30:00+00', 'US10-HPLC-04'),
(7713, 'SS_20260914_IMP', 'ktran', '2026-09-14 07:30:00+00', 'US10-HPLC-04'),
(7714, 'SS_20260919_ASS', 'ktran', '2026-09-19 07:30:00+00', 'US10-HPLC-04'),
(7715, 'SS_20260924_ASS', 'ktran', '2026-09-24 07:30:00+00', 'US10-HPLC-04')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS waters_empower.injection (
  injection_id  integer NOT NULL,
  sample_set_id integer NOT NULL,
  sample_name   varchar(40) NOT NULL,
  label         varchar(10),
  vial          varchar(10),
  injection_no  integer NOT NULL,
  date_acquired timestamptz NOT NULL,
  CONSTRAINT injection_pk PRIMARY KEY (injection_id)
);
COMMENT ON TABLE waters_empower.injection IS 'Injections; sample name is the LabWare sample text ID.';

INSERT INTO waters_empower.injection (injection_id, sample_set_id, sample_name, label, vial, injection_no, date_acquired) VALUES
(450001, 7701, 'S26-026104', 'U1', '1:A,1', 1, '2026-07-02 09:10:00+00'),
(450002, 7702, 'S26-026110', 'U1', '1:A,1', 1, '2026-07-16 09:10:00+00'),
(450003, 7703, 'S26-026112', 'U1', '1:A,1', 1, '2026-07-24 09:10:00+00'),
(450004, 7704, 'S26-026133', 'U1', '1:A,1', 1, '2026-07-25 09:10:00+00'),
(450005, 7705, 'S26-026127', 'U1', '1:A,1', 1, '2026-08-09 09:10:00+00'),
(450006, 7706, 'S26-026127', 'U1', '1:A,1', 1, '2026-08-10 09:10:00+00'),
(450007, 7707, 'S26-026116', 'U1', '1:A,1', 1, '2026-08-21 09:10:00+00'),
(450008, 7708, 'S26-026128', 'U1', '1:A,1', 1, '2026-08-23 09:10:00+00'),
(450009, 7709, 'S26-026128', 'U1', '1:A,1', 1, '2026-08-24 09:10:00+00'),
(450010, 7710, 'S26-026118', 'U1', '1:A,1', 1, '2026-08-27 09:10:00+00'),
(450011, 7711, 'S26-026129', 'U1', '1:A,1', 1, '2026-09-06 09:10:00+00'),
(450012, 7712, 'S26-026130', 'U1', '1:A,1', 1, '2026-09-13 09:10:00+00'),
(450013, 7713, 'S26-026130', 'U1', '1:A,1', 1, '2026-09-14 09:10:00+00'),
(450014, 7714, 'S26-026134', 'U1', '1:A,1', 1, '2026-09-19 09:10:00+00'),
(450015, 7715, 'S26-026122', 'U1', '1:A,1', 1, '2026-09-24 09:10:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS waters_empower.result (
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
COMMENT ON TABLE waters_empower.result IS 'Processed results with custom fields for the reported value, specification and pass/fail.';

INSERT INTO waters_empower.result (result_id, injection_id, processing_method, cf_test_code, cf_reported_value, cf_units, cf_spec_min, cf_spec_max, cf_pass_fail, processed_by, date_processed, signoff_status) VALUES
(980001, 450001, 'PM_ASSAY', 'ASSAY', '99.2', '%', '98.0', '102.0', 'Pass', 'ktran', '2026-07-02 12:20:00+00', 'Approved'),
(980002, 450002, 'PM_ASSAY', 'ASSAY', '99.2', '%', '98.0', '102.0', 'Pass', 'ktran', '2026-07-16 06:30:00+00', 'Approved'),
(980003, 450003, 'PM_ASSAY', 'ASSAY', '100.5', '%', '98.0', '102.0', 'Pass', 'ktran', '2026-07-24 10:00:00+00', 'Approved'),
(980004, 450004, 'PM_ASSAY', 'ASSAY', '95.7', '%', '95.0', '105.0', 'Pass', 'ktran', '2026-07-25 20:30:00+00', 'Approved'),
(980005, 450005, 'PM_ASSAY', 'ASSAY', '97.0', '%', '95.0', '105.0', 'Pass', 'ktran', '2026-08-09 21:00:00+00', 'Approved'),
(980006, 450006, 'PM_IMPURITY_TOTAL', 'IMPURITY-TOTAL', '0.22', '%', NULL, '1.0', 'Pass', 'ktran', '2026-08-10 21:00:00+00', 'Approved'),
(980007, 450007, 'PM_ASSAY', 'ASSAY', '100.4', '%', '98.0', '102.0', 'Pass', 'ktran', '2026-08-21 09:40:00+00', 'Approved'),
(980008, 450008, 'PM_ASSAY', 'ASSAY', '97.3', '%', '95.0', '105.0', 'Pass', 'ktran', '2026-08-23 17:00:00+00', 'Approved'),
(980009, 450009, 'PM_IMPURITY_TOTAL', 'IMPURITY-TOTAL', '0.22', '%', NULL, '1.0', 'Pass', 'ktran', '2026-08-24 17:00:00+00', 'Approved'),
(980010, 450010, 'PM_ASSAY', 'ASSAY', '99.9', '%', '98.0', '102.0', 'Pass', 'ktran', '2026-08-27 12:10:00+00', 'Approved'),
(980011, 450011, 'PM_ASSAY', 'ASSAY', '98.1', '%', '95.0', '105.0', 'Pass', 'ktran', '2026-09-06 22:00:00+00', 'Approved'),
(980012, 450012, 'PM_ASSAY', 'ASSAY', '97.9', '%', '95.0', '105.0', 'Pass', 'ktran', '2026-09-13 21:00:00+00', 'Approved'),
(980013, 450013, 'PM_IMPURITY_TOTAL', 'IMPURITY-TOTAL', '0.36', '%', NULL, '1.0', 'Pass', 'ktran', '2026-09-14 21:00:00+00', 'Approved'),
(980014, 450014, 'PM_ASSAY', 'ASSAY', '96.6', '%', '95.0', '105.0', 'Pass', 'ktran', '2026-09-19 19:00:00+00', 'Approved'),
(980015, 450015, 'PM_ASSAY', 'ASSAY', '100.0', '%', '98.0', '102.0', 'Pass', 'ktran', '2026-09-24 06:50:00+00', 'Approved')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/waters_empower).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS waters_empower.lims_sample_request (
  sample_name    varchar(40) NOT NULL,
  lot_name       varchar(40) NOT NULL,
  material       varchar(20) NOT NULL,
  requested_on   timestamptz NOT NULL,
  request_status varchar(20) NOT NULL,
  CONSTRAINT lims_sample_request_pk PRIMARY KEY (sample_name)
);
COMMENT ON TABLE waters_empower.lims_sample_request IS 'Empower LIMS interface sample list: quarantined lots awaiting chromatographic testing, from Material Quarantine Dispositions.';

GRANT USAGE ON SCHEMA waters_empower TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA waters_empower TO egeria_user, airflow_user;
