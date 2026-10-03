-- system-qualified-name: SoftwareServer::SYS-002::Veeva Vault QMS
-- Veeva Vault QMS - Bucharest.  Veeva Vault QMS for EKG quality assurance: deviations raised from manufacturing, the
-- laboratory, cold chain and safety, their investigations and CAPAs, and the QP decisions on batches that carry a
-- deviation.  Its tables feed Deviations And CAPAs and Batch Certification Decisions.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS veeva_qms;
COMMENT ON SCHEMA veeva_qms IS 'Veeva Vault QMS (EKG): Vault objects as landed by the Vault Direct Data API loader (one table per object, __v/__c/__qdm field names, picklist values as API names).';

CREATE TABLE IF NOT EXISTS veeva_qms.user__sys (
  id                varchar(20) NOT NULL,
  username__sys     varchar(120) NOT NULL,
  first_name__sys   varchar(80),
  last_name__sys    varchar(80),
  federated_id__sys varchar(60),
  status__v         varchar(20) NOT NULL,
  CONSTRAINT user__sys_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.user__sys IS 'Vault users (username = work e-mail; federated id = AD login used for SAML SSO).';

INSERT INTO veeva_qms.user__sys (id, username__sys, first_name__sys, last_name__sys, federated_id__sys, status__v) VALUES
('VUS0000000000100', 'ciprian.tudor@ekgpharma.ro', 'Ciprian', 'Tudor', 'ctudor', 'active__v'),
('VUS0000000000101', 'elena.popescu@ekgpharma.ro', 'Elena', 'Popescu', 'epopescu', 'active__v'),
('VUS0000000000102', 'florin.stoica@ekgpharma.ro', 'Florin', 'Stoica', 'fstoica', 'active__v'),
('VUS0000000000103', 'gabriela.toma@ekgpharma.ro', 'Gabriela', 'Toma', 'gtoma', 'active__v'),
('VUS0000000000104', 'marian.bucur@ekgpharma.ro', 'Marian', 'Bucur', 'mbucur', 'active__v'),
('VUS0000000000105', 'mihai.constantin@ekgpharma.ro', 'Mihai', 'Constantin', 'mconstantin', 'active__v'),
('VUS0000000000106', 'nicoleta.oprea@ekgpharma.ro', 'Nicoleta', 'Oprea', 'noprea', 'active__v'),
('VUS0000000000107', 'raluca.enache@ekgpharma.ro', 'Raluca', 'Enache', 'renache', 'active__v'),
('VUS0000000000108', 'radu.stoian@ekgpharma.ro', 'Radu', 'Stoian', 'rstoian', 'active__v')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS veeva_qms.product__v (
  id              varchar(20) NOT NULL,
  name__v         varchar(120) NOT NULL,
  product_code__c varchar(20) NOT NULL,
  status__v       varchar(20) NOT NULL,
  CONSTRAINT product__v_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.product__v IS 'Products (product_code__c = SAP material number).';

INSERT INTO veeva_qms.product__v (id, name__v, product_code__c, status__v) VALUES
('VPR0000000000010', 'Oxitocină EKG 5 UI/ml soluție injectabilă', 'PF-1101', 'active__v'),
('VPR0000000000011', 'Ceftriaxonă EKG 1 g pulbere pentru soluție injectabilă/perfuzabilă', 'PF-1102', 'active__v'),
('VPR0000000000012', 'Metoclopramid EKG 10 mg/2 ml soluție injectabilă', 'PF-1103', 'active__v'),
('VPR0000000000013', 'Ondansetron EKG 4 mg/2 ml soluție injectabilă', 'PF-1104', 'active__v'),
('VPR0000000000014', 'Octreotidă EKG 0,1 mg/ml soluție injectabilă', 'PF-1105', 'active__v'),
('VPR0000000000015', 'Ser autolog EKG 20% picături oftalmice (pacient nominal)', 'PF-9101', 'active__v')
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
COMMENT ON TABLE veeva_qms.quality_event__qdm IS 'Quality events of type deviation (MES in-process deviations arrive over the REST interface; LIMS OOS results; cold chain excursions; safety signals referred from pharmacovigilance).';

INSERT INTO veeva_qms.quality_event__qdm (id, name__v, object_type__v, title__v, description__c, state__v, severity__c, source__c, batch_number__c, product__c, signal_reference__c, created_date__v) VALUES
('VQE0000000002310', 'DEV-RO-000231', 'deviation__c', 'Oprire linie umplere fiole', 'Oprire linie de umplere RO10-AMP-01 timp de 47 min în timpul umplerii; purjarea cu azot a fost întreruptă.', 'closed_state__c', 'minor__c', 'manufacturing_execution__c', 'EK26-0329', 'VPR0000000000010', NULL, '2026-08-18 14:05:00+00'),
('VQE0000000002313', 'DEV-RO-000236', 'deviation__c', 'Autoclavă cu etalonare expirată', 'Autoclava RO10-AUT-02 utilizată la 2026-09-01 după data scadentă a etalonării (2026-08-28); valorile F0 au fost înregistrate de o sondă neetalonată. Semnalat de alerta Maximo.', 'investigation_state__c', 'major__c', 'manufacturing_execution__c', 'EK26-0335', 'VPR0000000000012', NULL, '2026-09-03 09:20:00+00'),
('VQE0000000002316', 'DEV-RO-000238', 'deviation__c', 'OOS dozare octreotidă lot MP26-0077', 'Rezultat în afara specificației la dozarea acetatului de octreotidă, lot MP26-0077 (96,1%; limită 98,0-102,0%). Furnizor neaprobat.', 'closed_state__c', 'major__c', 'laboratory__c', NULL, 'VPR0000000000014', NULL, '2026-09-10 16:40:00+00'),
('VQE0000000002319', 'DEV-RO-000240', 'deviation__c', 'Alarmă temperatură centrifugă', 'Alarmă temperatură centrifugă RO10-CEN-01: 9,2 °C timp de 6 min (limită 4 ± 2 °C) în timpul separării serului.', 'disposition_state__c', 'minor__c', 'manufacturing_execution__c', 'SA26-0040', 'VPR0000000000015', NULL, '2026-09-16 11:30:00+00'),
('VQE0000000002322', 'DEV-RO-000242', 'deviation__c', 'Excursie temperatură EXP-26-0418', 'Excursie de temperatură în transport, expediția EXP-26-0418 către Chișinău: max 9,4 °C timp de 50 min la punctul de trecere Albița.', 'investigation_state__c', 'minor__c', 'cold_chain__c', 'EK26-0329', 'VPR0000000000010', NULL, '2026-09-16 13:15:00+00'),
('VQE0000000002325', 'DEV-RO-000244', 'deviation__c', 'Semnal QT ondansetron', 'Semnal de siguranță referit de farmacovigilență: cazuri de prelungire QT la administrare IV rapidă de ondansetron; evaluare impact asupra RCP și a loturilor în curs.', 'open_state__c', 'major__c', 'safety_signal__c', NULL, 'VPR0000000000013', 'SIG-EKG-26-003', '2026-09-26 10:00:00+00')
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
('VIN0000000000700', 'INV-RO-000231', 'VQE0000000002310', 'VUS0000000000107', '2026-08-28', 'Senzor de presiune azot defect pe linia de umplere; alarma a oprit linia conform proiectării.', 'Fiolele umplute în intervalul fără purjare au fost identificate și distruse; restul lotului neafectat.', 'release_with_justification__c', 'complete_state__c'),
('VIN0000000000701', 'INV-RO-000238', 'VQE0000000002316', 'VUS0000000000101', '2026-09-12', 'Lot achiziționat de la un broker neaprobat (Balkan Pharma Trading) în timpul penuriei Bachem; substanță degradată.', 'Lotul nu a fost eliberat pentru producție; niciun lot de produs finit afectat.', 'reject__c', 'complete_state__c'),
('VIN0000000000702', 'INV-RO-000240', 'VQE0000000002319', 'VUS0000000000107', '2026-09-17', 'Ușa centrifugei deschisă prematur de operator; temperatura revenită în 6 min.', 'Expunere scurtă sub 10 °C; stabilitatea serului neafectată conform datelor de validare.', 'no_impact__c', 'complete_state__c'),
('VIN0000000000703', 'INV-RO-000236', 'VQE0000000002313', 'VUS0000000000107', NULL, NULL, NULL, NULL, 'in_progress_state__c')
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
COMMENT ON TABLE veeva_qms.capa_action__qdm IS 'Corrective and preventive actions.';

INSERT INTO veeva_qms.capa_action__qdm (id, name__v, quality_event__c, action_type__c, description__c, owner__c, due_date__c, state__v) VALUES
('VCA0000000001180', 'CAPA-RO-000118', 'VQE0000000002310', 'corrective__c', 'Înlocuire senzor presiune azot și adăugare în planul de etalonare Maximo.', 'VUS0000000000104', '2026-09-15', 'complete_state__c'),
('VCA0000000001181', 'CAPA-RO-000119', 'VQE0000000002310', 'preventive__c', 'Revizuire SOP-PRD-014 pentru reluarea umplerii după oprire.', 'VUS0000000000102', '2026-10-15', 'open_state__c'),
('VCA0000000001182', 'CAPA-RO-000121', 'VQE0000000002313', 'corrective__c', 'Interblocare MES: refuzarea utilizării echipamentelor cu etalonare expirată citită din Maximo.', 'VUS0000000000105', '2026-11-30', 'open_state__c'),
('VCA0000000001183', 'CAPA-RO-000122', 'VQE0000000002313', 'corrective__c', 'Reetalonare sonde autoclavă RO10-AUT-02 și recalificare.', 'VUS0000000000108', '2026-10-09', 'open_state__c'),
('VCA0000000001184', 'CAPA-RO-000123', 'VQE0000000002316', 'preventive__c', 'Blocare în SAP a achizițiilor de la furnizori neaprobați (grup de conturi ZRAW).', 'VUS0000000000100', '2026-09-30', 'verified_state__c')
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
COMMENT ON TABLE veeva_qms.batch_disposition__c IS 'QP disposition per batch and market for batches with an open or closed deviation (the MES release then references it).';

INSERT INTO veeva_qms.batch_disposition__c (id, name__v, batch_number__c, market__c, decision__c, decided_by__c, decision_date__c, released_quantity__c, record_complete__c, quality_event__c, notes__c, storage_conditions__c) VALUES
('VBD0000000000400', 'BD-EK26-0329-RO', 'EK26-0329', 'RO', 'certified__c', 'VUS0000000000106', '2026-09-04', 17600, TRUE, 'VQE0000000002310', 'Oprire linie umplere 47 min; purjare azot reluată; fiolele din intervalul afectat (812 buc.) distruse. Eliberare cu justificare.', 'A se păstra la frigider (2-8 °C). A nu se congela. A se păstra fiola în cutie.'),
('VBD0000000000401', 'BD-EK26-0329-MD', 'EK26-0329', 'MD', 'certified__c', 'VUS0000000000106', '2026-09-04', 5400, TRUE, 'VQE0000000002310', 'Idem RO; etichetare AMDM verificată.', 'A se păstra la frigider (2-8 °C). A nu se congela. A se păstra fiola în cutie.'),
('VBD0000000000402', 'BD-EK26-0335-RO', 'EK26-0335', 'RO', 'deferred__c', 'VUS0000000000106', '2026-09-25', NULL, TRUE, 'VQE0000000002313', 'Certificare amânată: sterilizare în autoclava RO10-AUT-02 cu etalonarea expirată la 2026-08-28; investigație în curs.', 'A nu se păstra la temperaturi peste 25 °C. A se proteja de lumină.')
ON CONFLICT DO NOTHING;

-- Custom Vault objects filled from the data sharing hub (subscription apply scripts buc_veeva_qms__*).
CREATE TABLE IF NOT EXISTS veeva_qms.batch__c (
  id                       varchar(20) NOT NULL,
  name__v                  varchar(40) NOT NULL,
  product__c               varchar(20),
  start_date__c            timestamptz,
  end_date__c              timestamptz,
  quantity__c              integer,
  record_complete__c       boolean,
  certification_status__c  varchar(40),
  modified_date__v         timestamptz NOT NULL,
  CONSTRAINT batch__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.batch__c IS 'Batch (custom object): the electronic batch record header of each batch with a quality event, reviewed before the QP disposition (batch_disposition__c); id = BAT- + batch number.';

CREATE TABLE IF NOT EXISTS veeva_qms.safety_signal__c (
  id                       varchar(20) NOT NULL,
  name__v                  varchar(40) NOT NULL,
  product__c               varchar(20) NOT NULL,
  detected_date__c         date,
  event_term__c            varchar(20),
  case_count__c            integer,
  description__c           text,
  signal_status__c         varchar(40),
  referral__c              varchar(40),
  modified_date__v         timestamptz NOT NULL,
  CONSTRAINT safety_signal__c_pk PRIMARY KEY (id)
);
COMMENT ON TABLE veeva_qms.safety_signal__c IS 'Safety signal (custom object): signals referred to quality, from which a deviation of source safety signal is opened (quality_event__qdm.signal_reference__c).';

GRANT USAGE ON SCHEMA veeva_qms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA veeva_qms TO egeria_user, airflow_user;
