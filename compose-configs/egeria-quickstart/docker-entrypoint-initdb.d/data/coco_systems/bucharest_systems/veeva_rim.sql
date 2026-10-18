-- system-qualified-name: SoftwareServer::SYS-021::Veeva Vault RIM
-- Veeva Vault RIM - Bucharest.  Veeva Vault RIM for EKG regulatory affairs: marketing authorisations (registrations)
-- per product and market with their conditions and commitments, and the safety submissions to ANMDMR, BDA, AMDM and
-- EudraVigilance with their acknowledgements.  Its tables feed Market Authorisations and Regulatory Safety
-- Submissions.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS veeva_rim;
COMMENT ON SCHEMA veeva_rim IS 'Veeva Vault RIM (EKG): Vault objects as landed by the Vault Direct Data API loader.';

CREATE TABLE IF NOT EXISTS veeva_rim.product__v (
  id              varchar(20) NOT NULL,
  name__v         varchar(120) NOT NULL,
  product_code__c varchar(20) NOT NULL,
  CONSTRAINT product__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.product__v IS 'Registered products (the named-patient serum has no marketing authorisation).';

INSERT INTO veeva_rim.product__v (id, name__v, product_code__c) VALUES
('VPR00000001', 'Oxitocină EKG 5 UI/ml soluție injectabilă', 'PF-1101'),
('VPR00000002', 'Ceftriaxonă EKG 1 g pulbere pentru soluție injectabilă/perfuzabilă', 'PF-1102'),
('VPR00000003', 'Metoclopramid EKG 10 mg/2 ml soluție injectabilă', 'PF-1103'),
('VPR00000004', 'Ondansetron EKG 4 mg/2 ml soluție injectabilă', 'PF-1104'),
('VPR00000005', 'Octreotidă EKG 0,1 mg/ml soluție injectabilă', 'PF-1105')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_rim.country__v (
  id              varchar(20) NOT NULL,
  name__v         varchar(80) NOT NULL,
  abbreviation__c varchar(2) NOT NULL,
  CONSTRAINT country__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.country__v IS 'Countries.';

INSERT INTO veeva_rim.country__v (id, name__v, abbreviation__c) VALUES
('VCT00000001', 'România', 'RO'),
('VCT00000002', 'Bulgaria', 'BG'),
('VCT00000003', 'Republica Moldova', 'MD')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_rim.registration__v (
  id                     varchar(20) NOT NULL,
  name__v                varchar(40) NOT NULL,
  product__v             varchar(20) NOT NULL,
  country__v             varchar(20) NOT NULL,
  health_authority__c    varchar(20) NOT NULL,
  registration_status__v varchar(30) NOT NULL,
  approval_date__v       date NOT NULL,
  expiration_date__v     date,
  related_signal__c      varchar(40),
  CONSTRAINT registration__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.registration__v IS 'Registrations (marketing authorisations) per product and country.';

INSERT INTO veeva_rim.registration__v (id, name__v, product__v, country__v, health_authority__c, registration_status__v, approval_date__v, expiration_date__v, related_signal__c) VALUES
('VRG00000001', '11873/2019/01', 'VPR00000001', 'VCT00000001', 'ANMDMR', 'approved__v', '2019-04-17', NULL, NULL),
('VRG00000002', '12544/2019/01', 'VPR00000002', 'VCT00000001', 'ANMDMR', 'approved__v', '2019-11-05', NULL, NULL),
('VRG00000003', '13208/2020/01', 'VPR00000003', 'VCT00000001', 'ANMDMR', 'approved__v', '2020-06-22', NULL, NULL),
('VRG00000004', '14790/2022/01', 'VPR00000004', 'VCT00000001', 'ANMDMR', 'approved__v', '2022-09-14', '2027-09-14', 'SIG-EKG-26-003'),
('VRG00000005', '15632/2024/01', 'VPR00000005', 'VCT00000001', 'ANMDMR', 'approved__v', '2024-03-28', '2029-03-28', NULL),
('VRG00000006', '20230417', 'VPR00000002', 'VCT00000002', 'BDA', 'approved__v', '2023-04-17', '2028-04-17', NULL),
('VRG00000007', 'MD-25418', 'VPR00000001', 'VCT00000003', 'AMDM', 'renewal_pending__c', '2021-10-11', '2026-10-11', NULL),
('VRG00000008', 'MD-26077', 'VPR00000003', 'VCT00000003', 'AMDM', 'approved__v', '2022-02-03', '2027-02-03', NULL),
('VRG00000009', '11873/2019/02', 'VPR00000001', 'VCT00000001', 'ANMDMR', 'withdrawn__v', '2019-04-17', '2025-12-31', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_rim.commitment__v (
  id                   varchar(20) NOT NULL,
  registration__v      varchar(20) NOT NULL,
  commitment_number__c integer NOT NULL,
  commitment_type__c   varchar(40) NOT NULL,
  description__v       text NOT NULL,
  start_date__c        date NOT NULL,
  CONSTRAINT commitment__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.commitment__v IS 'Conditions and commitments attached to registrations.';

INSERT INTO veeva_rim.commitment__v (id, registration__v, commitment_number__c, commitment_type__c, description__v, start_date__c) VALUES
('VCM00000001', 'VRG00000001', 1, 'pharmacovigilance__c', 'Depunere RPAS conform listei EURD (oxitocină)', '2019-04-17'),
('VCM00000002', 'VRG00000002', 1, 'quality__c', 'Studiu de stabilitate în curs pe trei loturi industriale; raportare anuală', '2019-11-05'),
('VCM00000003', 'VRG00000003', 1, 'labelling__c', 'RCP: durata maximă a tratamentului 5 zile (restricție metoclopramid)', '2020-06-22'),
('VCM00000004', 'VRG00000004', 1, 'pharmacovigilance__c', 'Monitorizare suplimentară a cazurilor de prelungire QT', '2022-09-14'),
('VCM00000005', 'VRG00000004', 2, 'labelling__c', 'Actualizare RCP pct. 4.4 privind administrarea IV rapidă (semnal SIG-EKG-26-003), în curs', '2026-09-29'),
('VCM00000006', 'VRG00000005', 1, 'specific_obligation__c', 'Raport final studiu de bioechivalență post-autorizare', '2024-03-28'),
('VCM00000007', 'VRG00000006', 1, 'labelling__c', 'Ambalaj bilingv BG/RO aprobat de BDA', '2023-04-17'),
('VCM00000008', 'VRG00000007', 1, 'renewal__c', 'Cerere de reînnoire depusă la AMDM; autorizația expiră 2026-10-11', '2026-07-08'),
('VCM00000009', 'VRG00000008', 1, 'labelling__c', 'Etichetă autocolantă în limba română cu nr. AMDM', '2022-02-03')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_rim.submission__v (
  id                         varchar(20) NOT NULL,
  name__v                    varchar(40) NOT NULL,
  product__v                 varchar(20) NOT NULL,
  country__v                 varchar(20) NOT NULL,
  health_authority__c        varchar(20) NOT NULL,
  submission_type__v         varchar(40) NOT NULL,
  planned_submission_date__v date NOT NULL,
  actual_submission_date__v  timestamptz,
  submission_format__c       varchar(20) NOT NULL,
  safety_case_reference__c   varchar(40),
  safety_related__c          boolean NOT NULL,
  CONSTRAINT submission__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.submission__v IS 'Submissions to health authorities (safety_related__c marks PSURs, expedited reports and safety variations).';

INSERT INTO veeva_rim.submission__v (id, name__v, product__v, country__v, health_authority__c, submission_type__v, planned_submission_date__v, actual_submission_date__v, submission_format__c, safety_case_reference__c, safety_related__c) VALUES
('VSB00000001', 'SUB-26-0012', 'VPR00000001', 'VCT00000001', 'ANMDMR', 'psur__v', '2026-06-30', '2026-06-24 10:15:00+00', 'cesp__c', NULL, TRUE),
('VSB00000002', 'SUB-26-0015', 'VPR00000003', 'VCT00000001', 'ANMDMR', 'psur__v', '2026-07-31', '2026-07-29 14:05:00+00', 'cesp__c', NULL, TRUE),
('VSB00000003', 'SUB-26-0016', 'VPR00000003', 'VCT00000003', 'AMDM', 'psur__v', '2026-08-15', '2026-08-20 09:30:00+00', 'paper__c', NULL, TRUE),
('VSB00000004', 'SUB-26-0017', 'VPR00000005', 'VCT00000001', 'EMA-EV', 'expedited__c', '2026-08-14', '2026-08-12 16:40:00+00', 'e2b_r3__c', 'EKG-ICSR-26-0104', TRUE),
('VSB00000005', 'SUB-26-0019', 'VPR00000002', 'VCT00000002', 'BDA', 'psur__v', '2026-09-01', '2026-08-27 11:20:00+00', 'cesp__c', NULL, TRUE),
('VSB00000006', 'SUB-26-0021', 'VPR00000004', 'VCT00000001', 'ANMDMR', 'safety_variation__c', '2026-10-26', '2026-09-29 15:50:00+00', 'ectd__v', 'EKG-ICSR-26-0117', TRUE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_rim.submission_acknowledgement__c (
  id                           varchar(20) NOT NULL,
  submission__v                varchar(20) NOT NULL,
  acknowledgement_reference__c varchar(60) NOT NULL,
  received_date__c             timestamptz NOT NULL,
  ack_status__c                varchar(20) NOT NULL,
  CONSTRAINT submission_acknowledgement__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.submission_acknowledgement__c IS 'Gateway / portal acknowledgements received for submissions.';

INSERT INTO veeva_rim.submission_acknowledgement__c (id, submission__v, acknowledgement_reference__c, received_date__c, ack_status__c) VALUES
('VAK00000001', 'VSB00000001', 'CESP-RO-2026-118822', '2026-06-24 10:22:00+00', 'delivered__c'),
('VAK00000002', 'VSB00000002', 'CESP-RO-2026-121907', '2026-07-29 14:11:00+00', 'delivered__c'),
('VAK00000003', 'VSB00000003', 'AMDM-INTR-2026-4471', '2026-09-02 12:00:00+00', 'received__c'),
('VAK00000004', 'VSB00000004', 'EV-ACK-2026-7730412', '2026-08-12 16:58:00+00', 'accepted__c'),
('VAK00000005', 'VSB00000005', 'CESP-BG-2026-044193', '2026-08-27 11:24:00+00', 'delivered__c')
ON CONFLICT DO NOTHING;

-- Custom Vault objects filled from the data sharing hub (subscription apply scripts buc_veeva_rim__*).
CREATE TABLE IF NOT EXISTS veeva_rim.safety_case__c (
  id                       varchar(20) NOT NULL,
  name__v                  varchar(40) NOT NULL,
  product__v               varchar(20) NOT NULL,
  report_reference__c      varchar(40),
  received_date__c         timestamptz,
  seriousness__c           varchar(20),
  expectedness__c          varchar(20),
  causality__c             varchar(20),
  reporting_due_date__c    date,
  case_status__c           varchar(20),
  modified_date__v         timestamptz NOT NULL,
  CONSTRAINT safety_case__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.safety_case__c IS 'Safety case (custom object): individual case safety reports to be submitted (submission__v.safety_case_reference__c), with the reporting due date.';

CREATE TABLE IF NOT EXISTS veeva_rim.safety_signal__c (
  id                       varchar(20) NOT NULL,
  name__v                  varchar(40) NOT NULL,
  product__v               varchar(20) NOT NULL,
  detected_date__c         date,
  event_term__c            varchar(20),
  case_count__c            integer,
  description__c           text,
  signal_status__c         varchar(40),
  referral__c              varchar(40),
  modified_date__v         timestamptz NOT NULL,
  CONSTRAINT safety_signal__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_rim.safety_signal__c IS 'Safety signal (custom object): signals referred to the authorisation register, which may lead to a label variation (registration__v.related_signal__c).';

GRANT USAGE ON SCHEMA veeva_rim TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA veeva_rim TO egeria_user, airflow_user;
