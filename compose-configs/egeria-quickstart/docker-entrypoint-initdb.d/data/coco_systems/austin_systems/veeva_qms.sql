-- system-qualified-name: SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901
-- Veeva Vault QMS - Austin.  The Austin quality management vault: deviations, investigations, CAPA actions, the safety
-- intake register and batch dispositions taken where a deviation is linked.  Its tables feed Deviations And CAPAs,
-- Consolidated Safety Reports (reports first received outside ServiceNow) and Batch Certification Decisions.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS veeva_qms;
COMMENT ON SCHEMA veeva_qms IS 'Veeva Vault QMS (Austin): Vault objects as landed by the Vault Direct Data API (lower-case API names).';

CREATE TABLE IF NOT EXISTS veeva_qms.user__sys (
  id              varchar(20) NOT NULL,
  username__sys   varchar(120) NOT NULL,
  first_name__sys varchar(80),
  last_name__sys  varchar(80),
  status__v       varchar(20) NOT NULL,
  CONSTRAINT user__sys_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.user__sys IS 'Vault users (QMS); username is the Entra UPN.';

INSERT INTO veeva_qms.user__sys (id, username__sys, first_name__sys, last_name__sys, status__v) VALUES
('V0U00000001000', 'mwhitfield@austinpharma.com', 'Marcus', 'Whitfield', 'active__v'),
('V0U00000001001', 'praman@austinpharma.com', 'Priya', 'Raman', 'active__v'),
('V0U00000001002', 'dokafor@austinpharma.com', 'Daniel', 'Okafor', 'active__v'),
('V0U00000001003', 'jmorales@austinpharma.com', 'Jason', 'Morales', 'active__v'),
('V0U00000001004', 'npetrov@austinpharma.com', 'Nina', 'Petrov', 'active__v'),
('V0U00000001005', 'epark@austinpharma.com', 'Ethan', 'Park', 'active__v'),
('V0U00000001006', 'imoreno@austinpharma.com', 'Isabel', 'Moreno', 'active__v'),
('V0U00000001007', 'rcastillo@austinpharma.com', 'Robert', 'Castillo', 'active__v')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.product__v (
  id              varchar(20) NOT NULL,
  name__v         varchar(120) NOT NULL,
  product_code__c varchar(20) NOT NULL,
  status__v       varchar(20) NOT NULL,
  CONSTRAINT product__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.product__v IS 'Product records (product_code__c = company product code).';

INSERT INTO veeva_qms.product__v (id, name__v, product_code__c, status__v) VALUES
('00P00000000200', 'Cozaar 100mg film-coated tablets', '3000', 'active__v'),
('00P00000000201', 'Plavix 75mg film-coated tablets', '2050', 'active__v'),
('00P00000000202', 'Cisplatin 50mg/50mL injection', '9000', 'active__v'),
('00P00000000203', 'Carboplatin 450mg/45mL injection', 'AU-4410', 'active__v'),
('00P00000000204', 'Oxaliplatin 100mg/20mL injection', 'AU-4520', 'active__v'),
('00P00000000205', 'Methotrexate 250mg/10mL injection', 'AU-4630', 'active__v'),
('00P00000000206', 'Dendrivax autologous dendritic cell suspension', 'AU-7710', 'active__v')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.quality_event__qdm (
  id                  varchar(20) NOT NULL,
  name__v             varchar(40) NOT NULL,
  object_type__v      varchar(40) NOT NULL,
  title__v            varchar(100) NOT NULL,
  description__c      text,
  state__v            varchar(40) NOT NULL,
  severity__c         varchar(20),
  source__c           varchar(40),
  batch_number__c     varchar(40),
  product__c          varchar(20),
  signal_reference__c varchar(40),
  created_date__v     timestamptz NOT NULL,
  CONSTRAINT quality_event__qdm_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.quality_event__qdm IS 'Quality events (deviation object type).';

INSERT INTO veeva_qms.quality_event__qdm (id, name__v, object_type__v, title__v, description__c, state__v, severity__c, source__c, batch_number__c, product__c, signal_reference__c, created_date__v) VALUES
('0QE00000003100', 'DEV-26-0197', 'deviation__c', 'Grade B viable air count above alert limit during vial filling', 'Grade B viable air count above alert limit during vial filling', 'closed_state__v', 'minor__c', 'manufacturing_execution__c', 'A26-4410-0052', '00P00000000203', NULL, '2026-07-21 11:40:00+00'),
('0QE00000003101', 'DEV-26-0203', 'deviation__c', 'Internal audit: aseptic gowning requalification tracked on paper, not linked to line access', 'Internal audit: aseptic gowning requalification tracked on paper, not linked to line access', 'open_state__c', 'minor__c', 'audit__c', NULL, NULL, NULL, '2026-07-29 09:15:00+00'),
('0QE00000003102', 'DEV-26-0212', 'deviation__c', 'One commissioned pack failed vision verification and was not aggregated; reconciliation difference o', 'One commissioned pack failed vision verification and was not aggregated; reconciliation difference of one pack', 'closed_state__v', 'minor__c', 'manufacturing_execution__c', 'A26-2050-0087', '00P00000000201', NULL, '2026-08-19 15:10:00+00'),
('0QE00000003103', 'DEV-26-0219', 'deviation__c', 'Safety signal referred from drug safety: cluster of hypersensitivity reactions with carboplatin', 'Safety signal referred from drug safety: cluster of hypersensitivity reactions with carboplatin', 'investigation_state__c', 'major__c', 'safety_signal__c', NULL, '00P00000000203', 'SIG-26-004', '2026-08-28 16:00:00+00'),
('0QE00000003104', 'DEV-26-0226', 'deviation__c', 'Mannitol lot RM26-0109 loss on drying out of specification at incoming testing', 'Mannitol lot RM26-0109 loss on drying out of specification at incoming testing', 'closed_state__v', 'minor__c', 'other__c', NULL, NULL, NULL, '2026-09-09 10:30:00+00'),
('0QE00000003105', 'DEV-26-0231', 'deviation__c', 'Check-weigher recorded fill weight below lower limit (49.95 g) during filling', 'Check-weigher recorded fill weight below lower limit (49.95 g) during filling', 'closed_state__v', 'minor__c', 'manufacturing_execution__c', 'A26-9000-0019', '00P00000000202', NULL, '2026-09-02 06:10:00+00'),
('0QE00000003106', 'DEV-26-0238', 'deviation__c', 'Main compression force above proven acceptable range (18.6 kN) during compression', 'Main compression force above proven acceptable range (18.6 kN) during compression', 'investigation_state__c', 'major__c', 'manufacturing_execution__c', 'A26-3000-0142', '00P00000000200', NULL, '2026-09-09 03:20:00+00'),
('0QE00000003107', 'DEV-26-0244', 'deviation__c', 'CO2 incubator US10-INC-02 used for culture after its calibration fell due on 2026-09-08', 'CO2 incubator US10-INC-02 used for culture after its calibration fell due on 2026-09-08', 'disposition_state__c', 'major__c', 'manufacturing_execution__c', 'A26-7710-P018', '00P00000000206', NULL, '2026-09-16 08:05:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.investigation__qdm (
  id                   varchar(20) NOT NULL,
  name__v              varchar(40) NOT NULL,
  quality_event__c     varchar(20) NOT NULL,
  investigator__c      varchar(20) NOT NULL,
  completed_date__c    date,
  root_cause__c        text,
  impact_assessment__c text,
  disposition__c       varchar(40),
  state__v             varchar(40) NOT NULL,
  CONSTRAINT investigation__qdm_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.investigation__qdm IS 'Investigations of quality events.';

INSERT INTO veeva_qms.investigation__qdm (id, name__v, quality_event__c, investigator__c, completed_date__c, root_cause__c, impact_assessment__c, disposition__c, state__v) VALUES
('0IN00000000500', 'INV-26-0197', '0QE00000003100', 'V0U00000001000', '2026-08-04', 'Door interlock on the isolator transfer hatch held open during a component transfer', 'Isolator integrity maintained; grade A results within limits', 'no_impact__c', 'complete_state__c'),
('0IN00000000501', 'INV-26-0212', '0QE00000003102', 'V0U00000001001', '2026-08-21', 'Vision camera misread due to label skew on one bottle; pack removed and destroyed', 'No impact on released packs; reconciliation explained', 'no_impact__c', 'complete_state__c'),
('0IN00000000502', 'INV-26-0226', '0QE00000003104', 'V0U00000001002', '2026-09-11', 'Supplier drying step shortened on their line (confirmed by supplier)', 'Lot never issued to production', 'reject__c', 'complete_state__c'),
('0IN00000000503', 'INV-26-0231', '0QE00000003105', 'V0U00000001001', '2026-09-10', 'Check-weigher feedback loop lag after a nozzle change; rejected vials removed automatically', 'Automatic rejection worked; all released vials within fill limits', 'release_with_justification__c', 'complete_state__c'),
('0IN00000000504', 'INV-26-0244', '0QE00000003107', 'V0U00000001000', '2026-09-24', 'Calibration work order not scheduled because the PM was set to manual release', 'As-found calibration within tolerance; culture conditions unaffected', 'release_with_justification__c', 'complete_state__c'),
('0IN00000000590', 'INV-26-0238', '0QE00000003106', 'V0U00000001001', NULL, NULL, NULL, NULL, 'in_progress_state__c')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.capa_action__qdm (
  id               varchar(20) NOT NULL,
  name__v          varchar(40) NOT NULL,
  quality_event__c varchar(20) NOT NULL,
  action_type__c   varchar(20) NOT NULL,
  description__c   text,
  owner__c         varchar(20) NOT NULL,
  due_date__c      date NOT NULL,
  state__v         varchar(40) NOT NULL,
  CONSTRAINT capa_action__qdm_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.capa_action__qdm IS 'CAPA actions.';

INSERT INTO veeva_qms.capa_action__qdm (id, name__v, quality_event__c, action_type__c, description__c, owner__c, due_date__c, state__v) VALUES
('0CA00000000700', 'CAPA-26-0101', '0QE00000003100', 'corrective__c', 'Retrain operators on transfer hatch procedure SOP-FIL-014', 'V0U00000001003', '2026-08-31', 'effectiveness_verified_state__c'),
('0CA00000000701', 'CAPA-26-0104', '0QE00000003101', 'preventive__c', 'Link Cornerstone aseptic qualification status to isolator badge access', 'V0U00000001004', '2026-11-30', 'open_state__c'),
('0CA00000000702', 'CAPA-26-0109', '0QE00000003104', 'corrective__c', 'Supplier corrective action request to Roquette America for drying step control', 'V0U00000001005', '2026-10-15', 'open_state__c'),
('0CA00000000703', 'CAPA-26-0112', '0QE00000003105', 'corrective__c', 'Retune check-weigher feedback after nozzle changes and add to changeover checklist', 'V0U00000001004', '2026-09-20', 'complete_state__c'),
('0CA00000000704', 'CAPA-26-0113', '0QE00000003105', 'preventive__c', 'Add low-fill trend alarm to the filling line telemetry', 'V0U00000001004', '2026-10-31', 'open_state__c'),
('0CA00000000705', 'CAPA-26-0118', '0QE00000003107', 'corrective__c', 'Calibrate US10-INC-02 and assess other assets with manually released PMs', 'V0U00000001004', '2026-09-19', 'complete_state__c'),
('0CA00000000706', 'CAPA-26-0119', '0QE00000003107', 'preventive__c', 'Block MES resource use when Maximo calibration due date has passed', 'V0U00000001003', '2026-12-15', 'open_state__c')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.safety_intake__c (
  id                       varchar(20) NOT NULL,
  name__v                  varchar(40) NOT NULL,
  received_datetime__c     timestamptz NOT NULL,
  source_type__c           varchar(40) NOT NULL,
  source_reference__c      varchar(80),
  patient_pseudonym__c     varchar(40),
  product__c               varchar(20) NOT NULL,
  batch_number__c          varchar(40),
  trial_reference__c       varchar(40),
  event_description__c     text NOT NULL,
  safety_case_reference__c varchar(40),
  state__v                 varchar(40) NOT NULL,
  CONSTRAINT safety_intake__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.safety_intake__c IS 'Safety intake register for reports first received by the quality unit (clinician, literature, medical information).';

INSERT INTO veeva_qms.safety_intake__c (id, name__v, received_datetime__c, source_type__c, source_reference__c, patient_pseudonym__c, product__c, batch_number__c, trial_reference__c, event_description__c, safety_case_reference__c, state__v) VALUES
('0SI00000000040', 'SI-000044', '2026-07-21 10:00:00+00', 'literature__c', 'J Oncol Pharm Pract 2026;32(5):1101-4', NULL, '00P00000000202', NULL, NULL, 'Published case report of cisplatin-associated high-frequency hearing loss in an adult patient', 'SC-26-0112', 'registered_state__c'),
('0SI00000000041', 'SI-000045', '2026-08-03 14:48:00+00', 'clinician__c', 'ARR-000031', 'PP-FA1AF588F5B4', '00P00000000206', 'A26-7710-P015', NULL, 'Grade 2 cytokine release syndrome 36 hours after Dendrivax infusion', 'SC-26-0118', 'registered_state__c'),
('0SI00000000042', 'SI-000047', '2026-09-02 13:05:00+00', 'clinician__c', 'HOLD-300117', 'PP-CCD4B098EAFF', '00P00000000206', 'A26-7710-P016', NULL, 'Injection-site erythema and fatigue reported to the order desk', NULL, 'registered_state__c'),
('0SI00000000043', 'SI-000048', '2026-09-19 17:22:00+00', 'clinician__c', 'ARR-000034', 'PP-08BA47CBA05B', '00P00000000206', 'A26-7710-P017', NULL, 'Infusion chills and rigors, self-limiting', NULL, 'registered_state__c'),
('0SI00000000044', 'SI-000049', '2026-09-24 12:40:00+00', 'other__c', 'MI-26-0388', NULL, '00P00000000205', NULL, NULL, 'Medical information call: hospital pharmacist reports mucositis in a patient on high-dose methotrexate', NULL, 'registered_state__c')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.batch_disposition__c (
  id                    varchar(20) NOT NULL,
  name__v               varchar(40) NOT NULL,
  batch_number__c       varchar(40) NOT NULL,
  market__c             varchar(8) NOT NULL,
  decision__c           varchar(20) NOT NULL,
  decided_by__c         varchar(20) NOT NULL,
  decision_date__c      date NOT NULL,
  released_quantity__c  integer,
  record_complete__c    boolean NOT NULL,
  quality_event__c      varchar(20),
  notes__c              text,
  storage_conditions__c text,
  CONSTRAINT batch_disposition__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.batch_disposition__c IS 'Batch disposition decisions taken in QMS because a deviation is linked to the batch.';

INSERT INTO veeva_qms.batch_disposition__c (id, name__v, batch_number__c, market__c, decision__c, decided_by__c, decision_date__c, released_quantity__c, record_complete__c, quality_event__c, notes__c, storage_conditions__c) VALUES
('0BD00000000060', 'BD-A26-4410-0052-US', 'A26-4410-0052', 'US', 'certified__c', 'V0U00000001001', '2026-08-05', 3180, TRUE, '0QE00000003100', 'Released after deviation closure; EM excursion assessed as no impact', NULL),
('0BD00000000061', 'BD-A26-2050-0087-US', 'A26-2050-0087', 'US', 'certified__c', 'V0U00000001001', '2026-08-24', 89400, TRUE, '0QE00000003102', 'Reconciliation difference explained', NULL),
('0BD00000000062', 'BD-A26-9000-0019-US', 'A26-9000-0019', 'US', 'certified__c', 'V0U00000001000', '2026-09-12', 1500, TRUE, '0QE00000003105', 'Released with justification: low-fill vials automatically rejected', 'Store at 20-25 C; do not refrigerate'),
('0BD00000000063', 'BD-A26-9000-0019-CA', 'A26-9000-0019', 'CA', 'certified__c', 'V0U00000001000', '2026-09-12', 950, TRUE, '0QE00000003105', 'Released with justification for Health Canada DIN 02534120', 'Store at 20-25 C; do not refrigerate'),
('0BD00000000064', 'BD-A26-3000-0142-US', 'A26-3000-0142', 'US', 'held__c', 'V0U00000001001', '2026-09-15', NULL, FALSE, '0QE00000003106', 'Held pending compression force investigation and dissolution results', NULL),
('0BD00000000065', 'BD-A26-3000-0142-CA', 'A26-3000-0142', 'CA', 'held__c', 'V0U00000001001', '2026-09-15', NULL, FALSE, '0QE00000003106', 'Held pending compression force investigation and dissolution results', NULL),
('0BD00000000066', 'BD-A26-7710-P018-US', 'A26-7710-P018', 'US', 'held__c', 'V0U00000001000', '2026-09-26', NULL, FALSE, '0QE00000003107', 'Deviation dispositioned; awaiting 14-day sterility result', NULL)
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/veeva_qms).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS veeva_qms.product_market__c (
  id                      varchar(20) NOT NULL,
  product__c              varchar(20) NOT NULL,
  market__c               varchar(8) NOT NULL,
  authorisation_number__c varchar(40) NOT NULL,
  authorised_from__c      date NOT NULL,
  authorised_to__c        date,
  CONSTRAINT product_market__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.product_market__c IS 'Markets each product is authorised in (release is only certified for these), from Product Master Data.';

CREATE TABLE IF NOT EXISTS veeva_qms.mes_exception__c (
  id                   varchar(20) NOT NULL,
  name__v              varchar(80) NOT NULL,
  batch_number__c      varchar(40) NOT NULL,
  step_number__c       integer NOT NULL,
  exception_type__c    varchar(20) NOT NULL,
  detail__c            text NOT NULL,
  occurred_datetime__c timestamptz,
  CONSTRAINT mes_exception__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.mes_exception__c IS 'Batch execution exceptions awaiting a decision to raise a deviation, from Batch Execution Records.';

CREATE TABLE IF NOT EXISTS veeva_qms.external_safety_report__c (
  id                   varchar(20) NOT NULL,
  name__v              varchar(40) NOT NULL,
  reported_date__c     date NOT NULL,
  patient_pseudonym__c varchar(40) NOT NULL,
  clinician__c         varchar(40) NOT NULL,
  product__c           varchar(20),
  batch_number__c      varchar(40),
  event_description__c text NOT NULL,
  reported_severity__c varchar(20),
  CONSTRAINT external_safety_report__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.external_safety_report__c IS 'Clinician reaction reports first received by other Austin systems, for quality triage, from Clinician Adverse Reaction Reports.';

CREATE TABLE IF NOT EXISTS veeva_qms.batch_record_review__c (
  id                   varchar(20) NOT NULL,
  name__v              varchar(40) NOT NULL,
  product__c           varchar(20),
  patient_pseudonym__c varchar(40),
  batch_start__c       timestamptz NOT NULL,
  batch_end__c         timestamptz,
  quantity__c          integer,
  record_complete__c   boolean NOT NULL,
  ebr_status__c        varchar(20) NOT NULL,
  CONSTRAINT batch_record_review__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.batch_record_review__c IS 'Batch records available for disposition review, from Electronic Batch Records.';

CREATE TABLE IF NOT EXISTS veeva_qms.complaint__qdm (
  id                          varchar(20) NOT NULL,
  name__v                     varchar(40) NOT NULL,
  received_datetime__c        timestamptz NOT NULL,
  reporter_type__c            varchar(100) NOT NULL,
  product__c                  varchar(20),
  batch_number__c             varchar(40),
  serial_number__c            varchar(40),
  description__c              text NOT NULL,
  csm_status__c               varchar(20) NOT NULL,
  safety_content__c           boolean,
  safety_assessed_by__c       varchar(40),
  safety_assessed_datetime__c timestamptz,
  safety_case_reference__c    varchar(40),
  CONSTRAINT complaint__qdm_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.complaint__qdm IS 'Product complaints for quality investigation, with the customer service safety assessment, from Product Complaints.';

CREATE TABLE IF NOT EXISTS veeva_qms.signal_referral__c (
  id                    varchar(20) NOT NULL,
  name__v               varchar(40) NOT NULL,
  detected_date__c      date NOT NULL,
  product__c            varchar(20),
  adverse_event_code__c varchar(20) NOT NULL,
  case_count__c         integer NOT NULL,
  description__c        text NOT NULL,
  signal_status__c      varchar(20) NOT NULL,
  referral_type__c      varchar(20),
  CONSTRAINT signal_referral__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.signal_referral__c IS 'Safety signals on Austin-made products referred to quality, from Safety Signals.';

GRANT USAGE ON SCHEMA veeva_qms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA veeva_qms TO egeria_user, airflow_user;
