-- system-qualified-name: SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301
-- Veeva Vault EBR - Austin.  The Austin electronic batch record vault: each batch's record assembled from MES,
-- SCADA/Kafka telemetry, LIMS and QMS sections, and the market release once certified.  Its tables feed Electronic
-- Batch Records and Batch Certification Decisions (batches with no linked deviation).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS veeva_ebr;
COMMENT ON SCHEMA veeva_ebr IS 'Veeva Vault EBR (Austin): batch, batch record section and batch release objects as landed by the Vault Direct Data API.';

CREATE TABLE IF NOT EXISTS veeva_ebr.user__sys (
  id              varchar(20) NOT NULL,
  username__sys   varchar(120) NOT NULL,
  first_name__sys varchar(80),
  last_name__sys  varchar(80),
  status__v       varchar(20) NOT NULL,
  CONSTRAINT user__sys_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.user__sys IS 'Vault users (EBR); username is the Entra UPN.';

INSERT INTO veeva_ebr.user__sys (id, username__sys, first_name__sys, last_name__sys, status__v) VALUES
('V0U00000001000', 'mwhitfield@austinpharma.com', 'Marcus', 'Whitfield', 'active__v'),
('V0U00000001001', 'praman@austinpharma.com', 'Priya', 'Raman', 'active__v'),
('V0U00000001002', 'dokafor@austinpharma.com', 'Daniel', 'Okafor', 'active__v'),
('V0U00000001003', 'jmorales@austinpharma.com', 'Jason', 'Morales', 'active__v'),
('V0U00000001004', 'npetrov@austinpharma.com', 'Nina', 'Petrov', 'active__v'),
('V0U00000001005', 'epark@austinpharma.com', 'Ethan', 'Park', 'active__v'),
('V0U00000001006', 'imoreno@austinpharma.com', 'Isabel', 'Moreno', 'active__v'),
('V0U00000001007', 'rcastillo@austinpharma.com', 'Robert', 'Castillo', 'active__v')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_ebr.product__v (
  id              varchar(20) NOT NULL,
  name__v         varchar(120) NOT NULL,
  product_code__c varchar(20) NOT NULL,
  status__v       varchar(20) NOT NULL,
  CONSTRAINT product__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.product__v IS 'Product records (product_code__c = company product code).';

INSERT INTO veeva_ebr.product__v (id, name__v, product_code__c, status__v) VALUES
('00P00000000200', 'Cozaar 100mg film-coated tablets', '3000', 'active__v'),
('00P00000000201', 'Plavix 75mg film-coated tablets', '2050', 'active__v'),
('00P00000000202', 'Cisplatin 50mg/50mL injection', '9000', 'active__v'),
('00P00000000203', 'Carboplatin 450mg/45mL injection', 'AU-4410', 'active__v'),
('00P00000000204', 'Oxaliplatin 100mg/20mL injection', 'AU-4520', 'active__v'),
('00P00000000205', 'Methotrexate 250mg/10mL injection', 'AU-4630', 'active__v'),
('00P00000000206', 'Dendrivax autologous dendritic cell suspension', 'AU-7710', 'active__v')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_ebr.batch__v (
  id                   varchar(20) NOT NULL,
  name__v              varchar(40) NOT NULL,
  product__c           varchar(20) NOT NULL,
  patient_pseudonym__c varchar(40),
  start_datetime__c    timestamptz NOT NULL,
  end_datetime__c      timestamptz,
  quantity__c          integer,
  status__v            varchar(40) NOT NULL,
  record_complete__c   boolean NOT NULL,
  CONSTRAINT batch__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.batch__v IS 'Batches; patient pseudonym is set for patient-specific batches.';

INSERT INTO veeva_ebr.batch__v (id, name__v, product__c, patient_pseudonym__c, start_datetime__c, end_datetime__c, quantity__c, status__v, record_complete__c) VALUES
('0BT00000000800', 'A26-3000-0141', '00P00000000200', NULL, '2026-08-03 06:00:00+00', '2026-08-05 18:00:00+00', 120000, 'certified__c', TRUE),
('0BT00000000801', 'A26-2050-0087', '00P00000000201', NULL, '2026-08-17 06:00:00+00', '2026-08-19 14:00:00+00', 90000, 'certified__c', TRUE),
('0BT00000000802', 'A26-9000-0019', '00P00000000202', NULL, '2026-09-01 07:00:00+00', '2026-09-02 19:00:00+00', 2500, 'certified__c', TRUE),
('0BT00000000803', 'A26-3000-0142', '00P00000000200', NULL, '2026-09-07 06:00:00+00', '2026-09-09 18:00:00+00', 120000, 'under_review__c', FALSE),
('0BT00000000804', 'A26-2050-0088', '00P00000000201', NULL, '2026-09-28 06:00:00+00', NULL, 90000, 'in_execution__c', FALSE),
('0BT00000000805', 'A26-4410-0052', '00P00000000203', NULL, '2026-07-20 07:00:00+00', '2026-07-21 17:30:00+00', 3200, 'certified__c', TRUE),
('0BT00000000806', 'A26-4630-0017', '00P00000000205', NULL, '2026-09-14 07:00:00+00', '2026-09-15 16:00:00+00', 4000, 'certified__c', TRUE),
('0BT00000000807', 'A26-7710-P015', '00P00000000206', 'PP-FA1AF588F5B4', '2026-07-13 07:00:00+00', '2026-07-24 16:00:00+00', 1, 'certified__c', TRUE),
('0BT00000000808', 'A26-7710-P016', '00P00000000206', 'PP-CCD4B098EAFF', '2026-08-10 07:00:00+00', '2026-08-21 15:30:00+00', 1, 'certified__c', TRUE),
('0BT00000000809', 'A26-7710-P017', '00P00000000206', 'PP-08BA47CBA05B', '2026-09-01 07:00:00+00', '2026-09-12 14:00:00+00', 1, 'certified__c', TRUE),
('0BT00000000810', 'A26-7710-P018', '00P00000000206', 'PP-06CCD43B6C3E', '2026-09-15 07:00:00+00', '2026-09-26 15:00:00+00', 1, 'under_review__c', FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_ebr.batch_record_section__c (
  id                   varchar(20) NOT NULL,
  batch__c             varchar(20) NOT NULL,
  section_reference__c varchar(60) NOT NULL,
  section_type__c      varchar(40) NOT NULL,
  source_system__c     varchar(20) NOT NULL,
  received_datetime__c timestamptz NOT NULL,
  CONSTRAINT batch_record_section__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.batch_record_section__c IS 'Sections of the batch record received from contributing systems.';

INSERT INTO veeva_ebr.batch_record_section__c (id, batch__c, section_reference__c, section_type__c, source_system__c, received_datetime__c) VALUES
('0BS00000009001', '0BT00000000800', 'OPC-A26-3000-0141-EXEC', 'execution__c', 'OPCENTER', '2026-08-05 18:30:00+00'),
('0BS00000009002', '0BT00000000800', 'FAC-A26-3000-0141-PP', 'process_parameters__c', 'FACTORYTALK', '2026-08-05 19:00:00+00'),
('0BS00000009003', '0BT00000000800', 'AUS-COA-26-0141', 'laboratory_results__c', 'LABWARE', '2026-08-11 02:20:00+00'),
('0BS00000009004', '0BT00000000800', 'SIG-MWHITFIELD-0141', 'signature_authority__c', 'VAULT_EBR', '2026-08-17 10:00:00+00'),
('0BS00000009011', '0BT00000000801', 'OPC-A26-2050-0087-EXEC', 'execution__c', 'OPCENTER', '2026-08-19 14:30:00+00'),
('0BS00000009012', '0BT00000000801', 'FAC-A26-2050-0087-PP', 'process_parameters__c', 'FACTORYTALK', '2026-08-19 15:00:00+00'),
('0BS00000009013', '0BT00000000801', 'AUS-COA-26-0087', 'laboratory_results__c', 'LABWARE', '2026-08-24 22:20:00+00'),
('0BS00000009014', '0BT00000000801', 'DEV-26-0212', 'deviation_disposition__c', 'VAULT_QMS', '2026-08-21 17:00:00+00'),
('0BS00000009015', '0BT00000000801', 'SIG-PRAMAN-0087', 'signature_authority__c', 'VAULT_EBR', '2026-08-24 10:00:00+00'),
('0BS00000009021', '0BT00000000802', 'OPC-A26-9000-0019-EXEC', 'execution__c', 'OPCENTER', '2026-09-02 19:30:00+00'),
('0BS00000009022', '0BT00000000802', 'KAF-A26-9000-0019-PP', 'process_parameters__c', 'KAFKA', '2026-09-02 20:00:00+00'),
('0BS00000009023', '0BT00000000802', 'AUS-COA-26-0019', 'laboratory_results__c', 'LABWARE', '2026-09-10 02:20:00+00'),
('0BS00000009024', '0BT00000000802', 'DEV-26-0231', 'deviation_disposition__c', 'VAULT_QMS', '2026-09-10 17:00:00+00'),
('0BS00000009025', '0BT00000000802', 'SIG-MWHITFIELD-0019', 'signature_authority__c', 'VAULT_EBR', '2026-09-12 10:00:00+00'),
('0BS00000009031', '0BT00000000803', 'OPC-A26-3000-0142-EXEC', 'execution__c', 'OPCENTER', '2026-09-09 18:30:00+00'),
('0BS00000009032', '0BT00000000803', 'FAC-A26-3000-0142-PP', 'process_parameters__c', 'FACTORYTALK', '2026-09-09 19:00:00+00'),
('0BS00000009041', '0BT00000000804', 'OPC-A26-2050-0088-EXEC-PARTIAL', 'execution__c', 'OPCENTER', '2026-09-29 18:00:00+00'),
('0BS00000009051', '0BT00000000805', 'OPC-A26-4410-0052-EXEC', 'execution__c', 'OPCENTER', '2026-07-21 18:00:00+00'),
('0BS00000009052', '0BT00000000805', 'KAF-A26-4410-0052-PP', 'process_parameters__c', 'KAFKA', '2026-07-21 18:30:00+00'),
('0BS00000009053', '0BT00000000805', 'AUS-COA-26-0052', 'laboratory_results__c', 'LABWARE', '2026-07-29 00:50:00+00'),
('0BS00000009054', '0BT00000000805', 'DEV-26-0197', 'deviation_disposition__c', 'VAULT_QMS', '2026-08-04 17:00:00+00'),
('0BS00000009055', '0BT00000000805', 'SIG-PRAMAN-0052', 'signature_authority__c', 'VAULT_EBR', '2026-08-05 10:00:00+00'),
('0BS00000009061', '0BT00000000806', 'OPC-A26-4630-0017-EXEC', 'execution__c', 'OPCENTER', '2026-09-15 16:30:00+00'),
('0BS00000009062', '0BT00000000806', 'KAF-A26-4630-0017-PP', 'process_parameters__c', 'KAFKA', '2026-09-15 17:00:00+00'),
('0BS00000009063', '0BT00000000806', 'AUS-COA-26-0017', 'laboratory_results__c', 'LABWARE', '2026-09-22 23:20:00+00'),
('0BS00000009064', '0BT00000000806', 'SIG-PRAMAN-0017', 'signature_authority__c', 'VAULT_EBR', '2026-09-23 10:00:00+00'),
('0BS00000009071', '0BT00000000807', 'OPC-A26-7710-P015-EXEC', 'execution__c', 'OPCENTER', '2026-07-24 16:30:00+00'),
('0BS00000009072', '0BT00000000807', 'KAF-A26-7710-P015-PP', 'process_parameters__c', 'KAFKA', '2026-07-24 17:00:00+00'),
('0BS00000009073', '0BT00000000807', 'AUS-COA-26-P015', 'laboratory_results__c', 'LABWARE', '2026-08-07 23:20:00+00'),
('0BS00000009074', '0BT00000000807', 'EXC-P015-NONE', 'excursion_disposition__c', 'VAULT_QMS', '2026-07-28 09:00:00+00'),
('0BS00000009075', '0BT00000000807', 'SIG-PRAMAN-P015', 'signature_authority__c', 'VAULT_EBR', '2026-07-28 10:00:00+00'),
('0BS00000009081', '0BT00000000808', 'OPC-A26-7710-P016-EXEC', 'execution__c', 'OPCENTER', '2026-08-21 16:00:00+00'),
('0BS00000009082', '0BT00000000808', 'KAF-A26-7710-P016-PP', 'process_parameters__c', 'KAFKA', '2026-08-21 16:30:00+00'),
('0BS00000009083', '0BT00000000808', 'AUS-COA-26-P016', 'laboratory_results__c', 'LABWARE', '2026-09-04 22:50:00+00'),
('0BS00000009084', '0BT00000000808', 'EXC-P016-NONE', 'excursion_disposition__c', 'VAULT_QMS', '2026-08-25 08:30:00+00'),
('0BS00000009085', '0BT00000000808', 'SIG-MWHITFIELD-P016', 'signature_authority__c', 'VAULT_EBR', '2026-08-25 10:00:00+00'),
('0BS00000009091', '0BT00000000809', 'OPC-A26-7710-P017-EXEC', 'execution__c', 'OPCENTER', '2026-09-12 14:30:00+00'),
('0BS00000009092', '0BT00000000809', 'KAF-A26-7710-P017-PP', 'process_parameters__c', 'KAFKA', '2026-09-12 15:00:00+00'),
('0BS00000009093', '0BT00000000809', 'AUS-COA-26-P017', 'laboratory_results__c', 'LABWARE', '2026-09-26 21:20:00+00'),
('0BS00000009094', '0BT00000000809', 'EXC-P017-NONE', 'excursion_disposition__c', 'VAULT_QMS', '2026-09-15 07:30:00+00'),
('0BS00000009095', '0BT00000000809', 'SIG-MWHITFIELD-P017', 'signature_authority__c', 'VAULT_EBR', '2026-09-15 10:00:00+00'),
('0BS00000009101', '0BT00000000810', 'OPC-A26-7710-P018-EXEC', 'execution__c', 'OPCENTER', '2026-09-26 15:30:00+00'),
('0BS00000009102', '0BT00000000810', 'KAF-A26-7710-P018-PP', 'process_parameters__c', 'KAFKA', '2026-09-26 16:00:00+00'),
('0BS00000009103', '0BT00000000810', 'DEV-26-0244', 'deviation_disposition__c', 'VAULT_QMS', '2026-09-24 17:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_ebr.batch_release__c (
  id                    varchar(20) NOT NULL,
  batch__c              varchar(20) NOT NULL,
  market__c             varchar(8) NOT NULL,
  released_quantity__c  integer NOT NULL,
  certification_date__c date NOT NULL,
  certified_by__c       varchar(20) NOT NULL,
  decision__c           varchar(20) NOT NULL,
  notes__c              text,
  storage_conditions__c text,
  CONSTRAINT batch_release__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.batch_release__c IS 'Market release authorisations of certified batches.';

INSERT INTO veeva_ebr.batch_release__c (id, batch__c, market__c, released_quantity__c, certification_date__c, certified_by__c, decision__c, notes__c, storage_conditions__c) VALUES
('0BR00000000100', '0BT00000000800', 'US', 73656, '2026-08-17', 'V0U00000001000', 'certified__c', NULL, 'Store at 20-25 C'),
('0BR00000000101', '0BT00000000800', 'CA', 45144, '2026-08-17', 'V0U00000001000', 'certified__c', NULL, 'Store at 20-25 C'),
('0BR00000000102', '0BT00000000801', 'US', 89400, '2026-08-24', 'V0U00000001001', 'certified__c', 'Deviation dispositioned in QMS before release', 'Store at 20-25 C'),
('0BR00000000103', '0BT00000000802', 'US', 1500, '2026-09-12', 'V0U00000001000', 'certified__c', 'Deviation dispositioned in QMS before release', 'Store at 15-25 C; protect from light; do not refrigerate'),
('0BR00000000104', '0BT00000000802', 'CA', 950, '2026-09-12', 'V0U00000001000', 'certified__c', 'Deviation dispositioned in QMS before release', 'Store at 15-25 C; protect from light; do not refrigerate'),
('0BR00000000105', '0BT00000000805', 'US', 3180, '2026-08-05', 'V0U00000001001', 'certified__c', 'Deviation dispositioned in QMS before release', 'Store at 20-25 C; protect from light'),
('0BR00000000106', '0BT00000000806', 'US', 3960, '2026-09-23', 'V0U00000001001', 'certified__c', NULL, 'Store at 20-25 C; protect from light'),
('0BR00000000107', '0BT00000000807', 'US', 1, '2026-07-28', 'V0U00000001001', 'certified__c', NULL, 'Ship in LN2 vapour-phase dry shipper at or below -150 C; chain of identity seal intact'),
('0BR00000000108', '0BT00000000808', 'US', 1, '2026-08-25', 'V0U00000001000', 'certified__c', NULL, 'Ship in LN2 vapour-phase dry shipper at or below -150 C; chain of identity seal intact'),
('0BR00000000109', '0BT00000000809', 'US', 1, '2026-09-15', 'V0U00000001000', 'certified__c', NULL, 'Ship in LN2 vapour-phase dry shipper at or below -150 C; chain of identity seal intact')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/veeva_ebr).
-- No extract reads them.

ALTER TABLE veeva_ebr.product__v ADD COLUMN IF NOT EXISTS storage_min_temp__c double precision;
ALTER TABLE veeva_ebr.product__v ADD COLUMN IF NOT EXISTS storage_max_temp__c double precision;
ALTER TABLE veeva_ebr.product__v ADD COLUMN IF NOT EXISTS hazard_code__c varchar(20);
ALTER TABLE veeva_ebr.product__v ADD COLUMN IF NOT EXISTS shelf_life_days__c integer;
COMMENT ON COLUMN veeva_ebr.product__v.storage_min_temp__c IS 'Minimum storage temperature (C), from Product Master Data.';
COMMENT ON COLUMN veeva_ebr.product__v.storage_max_temp__c IS 'Maximum storage temperature (C), from Product Master Data.';
COMMENT ON COLUMN veeva_ebr.product__v.shelf_life_days__c IS 'Shelf life in days, from Product Master Data.';

CREATE TABLE IF NOT EXISTS veeva_ebr.product_market__c (
  id                      varchar(20) NOT NULL,
  product__c              varchar(20) NOT NULL,
  market__c               varchar(8) NOT NULL,
  authorisation_number__c varchar(40) NOT NULL,
  authorised_from__c      date NOT NULL,
  authorised_to__c        date,
  CONSTRAINT product_market__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.product_market__c IS 'Markets each product is authorised in (release is only certified for these), from Product Master Data.';

CREATE TABLE IF NOT EXISTS veeva_ebr.execution_step__c (
  id                    varchar(20) NOT NULL,
  name__v               varchar(60) NOT NULL,
  batch__c              varchar(20) NOT NULL,
  step_number__c        integer NOT NULL,
  step_code__c          varchar(40) NOT NULL,
  start_datetime__c     timestamptz NOT NULL,
  end_datetime__c       timestamptz NOT NULL,
  performer_pseudonym__c varchar(40) NOT NULL,
  signature__c          varchar(200) NOT NULL,
  step_status__c        varchar(100) NOT NULL,
  CONSTRAINT execution_step__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.execution_step__c IS 'Executed steps of each batch with their electronic signatures, from Batch Execution Records.';

CREATE TABLE IF NOT EXISTS veeva_ebr.material_consumption__c (
  id               varchar(20) NOT NULL,
  batch__c         varchar(20) NOT NULL,
  step_number__c   integer NOT NULL,
  lot__c           varchar(40) NOT NULL,
  material_code__c varchar(20) NOT NULL,
  quantity__c      double precision NOT NULL,
  unit__c          varchar(20) NOT NULL,
  CONSTRAINT material_consumption__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.material_consumption__c IS 'Raw material lots consumed at each step, from Batch Execution Records.';

CREATE TABLE IF NOT EXISTS veeva_ebr.equipment_use__c (
  id                      varchar(20) NOT NULL,
  batch__c                varchar(20) NOT NULL,
  step_number__c          integer NOT NULL,
  equipment__c            varchar(40) NOT NULL,
  qualification_status__c varchar(20) NOT NULL,
  calibration_due__c      date NOT NULL,
  CONSTRAINT equipment_use__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.equipment_use__c IS 'Equipment used at each step with its status at use, from Batch Execution Records.';

CREATE TABLE IF NOT EXISTS veeva_ebr.batch_deviation__c (
  id                         varchar(20) NOT NULL,
  name__v                    varchar(40) NOT NULL,
  batch__c                   varchar(20) NOT NULL,
  raised_datetime__c         timestamptz NOT NULL,
  source__c                  varchar(100) NOT NULL,
  severity__c                varchar(20) NOT NULL,
  description__c             text NOT NULL,
  state__c                   varchar(20) NOT NULL,
  disposition__c             varchar(40),
  investigation_completed__c date,
  impact__c                  text,
  CONSTRAINT batch_deviation__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.batch_deviation__c IS 'QMS deviations linked to a batch, with the investigation disposition, from Deviations And CAPAs.';

CREATE TABLE IF NOT EXISTS veeva_ebr.qc_sample__c (
  id                    varchar(20) NOT NULL,
  name__v               varchar(40) NOT NULL,
  batch__c              varchar(20) NOT NULL,
  sample_type__c        varchar(20) NOT NULL,
  collected_datetime__c timestamptz NOT NULL,
  status__c             varchar(20) NOT NULL,
  CONSTRAINT qc_sample__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.qc_sample__c IS 'LIMS samples of the batch (in-process and finished product), from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS veeva_ebr.qc_result__c (
  id                    varchar(20) NOT NULL,
  name__v               varchar(40) NOT NULL,
  qc_sample__c          varchar(20) NOT NULL,
  test__c               varchar(40) NOT NULL,
  result_value__c       varchar(60) NOT NULL,
  unit__c               varchar(20),
  specification_min__c  varchar(60),
  specification_max__c  varchar(60),
  conforms__c           boolean NOT NULL,
  completed_datetime__c timestamptz NOT NULL,
  analyst__c            varchar(40) NOT NULL,
  CONSTRAINT qc_result__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.qc_result__c IS 'Laboratory results on the batch samples, from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS veeva_ebr.certificate_of_analysis__c (
  id                  varchar(20) NOT NULL,
  name__v             varchar(40) NOT NULL,
  batch__c            varchar(20) NOT NULL,
  certificate_date__c date NOT NULL,
  conforms__c         boolean NOT NULL,
  approved_by__c      varchar(40) NOT NULL,
  CONSTRAINT certificate_of_analysis__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.certificate_of_analysis__c IS 'Finished batch certificates of analysis issued by the laboratory, from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS veeva_ebr.planned_batch__c (
  id                    varchar(20) NOT NULL,
  name__v               varchar(40) NOT NULL,
  order_reference__c    varchar(40) NOT NULL,
  patient_pseudonym__c  varchar(40) NOT NULL,
  product_code__c       varchar(20) NOT NULL,
  slot_start__c         timestamptz NOT NULL,
  slot_end__c           timestamptz NOT NULL,
  patient_parameters__c text,
  slot_status__c        varchar(20) NOT NULL,
  CONSTRAINT planned_batch__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.planned_batch__c IS 'Scheduled patient-specific batches; the batch record is opened from here when the slot starts.  From Personalised Manufacturing Schedule.';

CREATE TABLE IF NOT EXISTS veeva_ebr.patient_material_receipt__c (
  id                   varchar(20) NOT NULL,
  name__v              varchar(40) NOT NULL,
  patient_pseudonym__c varchar(40) NOT NULL,
  received_datetime__c timestamptz NOT NULL,
  arrival_condition__c text NOT NULL,
  viable_hours__c      integer NOT NULL,
  CONSTRAINT patient_material_receipt__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.patient_material_receipt__c IS 'Receipt of the patient starting material for a scheduled batch, from Personalised Manufacturing Schedule.';

CREATE TABLE IF NOT EXISTS veeva_ebr.process_parameter__c (
  id                  varchar(20) NOT NULL,
  batch__c            varchar(20) NOT NULL,
  equipment__c        varchar(40) NOT NULL,
  parameter__c        varchar(40) NOT NULL,
  reading_datetime__c timestamptz NOT NULL,
  reading_value__c    double precision NOT NULL,
  unit__c             varchar(20) NOT NULL,
  range_min__c        double precision,
  range_max__c        double precision,
  CONSTRAINT process_parameter__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.process_parameter__c IS 'Process parameter readings taken during the batch, from Process Parameter Time Series.';

CREATE TABLE IF NOT EXISTS veeva_ebr.excursion_assessment__c (
  id                     varchar(20) NOT NULL,
  name__v                varchar(40) NOT NULL,
  batch__c               varchar(20) NOT NULL,
  shipment__c            varchar(40) NOT NULL,
  product_code__c        varchar(20) NOT NULL,
  assessed_by__c         varchar(40) NOT NULL,
  assessed_datetime__c   timestamptz NOT NULL,
  stability_reference__c varchar(40) NOT NULL,
  disposition__c         varchar(20) NOT NULL,
  notes__c               text,
  CONSTRAINT excursion_assessment__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.excursion_assessment__c IS 'Temperature excursion dispositions for shipments of the batch, from Temperature Excursion Assessments.';

CREATE TABLE IF NOT EXISTS veeva_ebr.signature_qualification__c (
  id                  varchar(20) NOT NULL,
  worker_pseudonym__c varchar(40) NOT NULL,
  competency__c       varchar(40) NOT NULL,
  competency_name__c  varchar(120) NOT NULL,
  qualified_from__c   date NOT NULL,
  qualified_to__c     date NOT NULL,
  status__c           varchar(20) NOT NULL,
  training_record__c  varchar(40) NOT NULL,
  certificate__c      varchar(40),
  role__c             varchar(40) NOT NULL,
  CONSTRAINT signature_qualification__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_ebr.signature_qualification__c IS 'Worker qualifications checked by the signature authority rule (by worker pseudonym), from Worker Qualifications.';

GRANT USAGE ON SCHEMA veeva_ebr TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA veeva_ebr TO egeria_user, airflow_user;
