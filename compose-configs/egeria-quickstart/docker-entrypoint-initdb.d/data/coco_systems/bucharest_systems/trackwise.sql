-- system-qualified-name: SoftwareServer::SYS-005::Trackwise Digital
-- Trackwise Digital - Bucharest.  Sparta TrackWise Digital (on Salesforce) used by EKG regulatory affairs for GMP
-- compliance tracking: inspection and audit observations, supplier deviations, their investigations and CAPAs, plus
-- read-only copies of CAPAs closed in Veeva QMS.  Its tables feed Deviations And CAPAs (Trackwise-originated records
-- only).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS trackwise;
COMMENT ON SCHEMA trackwise IS 'Trackwise Digital (EKG): managed-package objects (namespace cmpl123qms__) as landed by the Salesforce replication tool: sfid keys, lower-case API names.';

CREATE TABLE IF NOT EXISTS trackwise.users (
  sfid                 varchar(18) NOT NULL,
  username             varchar(120) NOT NULL,
  firstname            varchar(80),
  lastname             varchar(80),
  federationidentifier varchar(60),
  isactive             boolean NOT NULL,
  CONSTRAINT users_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE trackwise.users IS 'Salesforce users (federation identifier = AD login used for SSO).';

INSERT INTO trackwise.users (sfid, username, firstname, lastname, federationidentifier, isactive) VALUES
('005000000004100AAA', 'adina.petre@ekgpharma.ro.tw', 'Adina', 'Petre', 'apetre', TRUE),
('005000000004101AAA', 'ciprian.tudor@ekgpharma.ro.tw', 'Ciprian', 'Tudor', 'ctudor', TRUE),
('005000000004102AAA', 'marian.bucur@ekgpharma.ro.tw', 'Marian', 'Bucur', 'mbucur', TRUE),
('005000000004103AAA', 'mihai.constantin@ekgpharma.ro.tw', 'Mihai', 'Constantin', 'mconstantin', TRUE),
('005000000004104AAA', 'nicoleta.oprea@ekgpharma.ro.tw', 'Nicoleta', 'Oprea', 'noprea', TRUE),
('005000000004105AAA', 'raluca.enache@ekgpharma.ro.tw', 'Raluca', 'Enache', 'renache', TRUE),
('005000000004106AAA', 'sorin.matei@ekgpharma.ro.tw', 'Sorin', 'Matei', 'smatei', TRUE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS trackwise.cmpl123qms__quality_event__c (
  sfid                            varchar(18) NOT NULL,
  name                            varchar(80) NOT NULL,
  createddate                     timestamptz NOT NULL,
  cmpl123qms__category__c         varchar(40) NOT NULL,
  cmpl123qms__batch_number__c     varchar(40),
  cmpl123qms__product_code__c     varchar(20),
  cmpl123qms__description__c      text,
  cmpl123qms__severity__c         varchar(20),
  cmpl123qms__status__c           varchar(20) NOT NULL,
  cmpl123qms__origin_system__c    varchar(40) NOT NULL,
  cmpl123qms__origin_reference__c varchar(40),
  isdeleted                       boolean NOT NULL,
  CONSTRAINT cmpl123qms__quality_event__c_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE trackwise.cmpl123qms__quality_event__c IS 'Quality events.  origin_system = Veeva QMS marks read-only copies received with closed CAPAs over the QMS interface.';

INSERT INTO trackwise.cmpl123qms__quality_event__c (sfid, name, createddate, cmpl123qms__category__c, cmpl123qms__batch_number__c, cmpl123qms__product_code__c, cmpl123qms__description__c, cmpl123qms__severity__c, cmpl123qms__status__c, cmpl123qms__origin_system__c, cmpl123qms__origin_reference__c, isdeleted) VALUES
('a0Q000000048100AAA', 'TWD-000481', '2026-06-24 10:00:00+00', 'Regulatory Inspection', NULL, NULL, 'Observație inspecție ANMDMR: cont partajat pe stația Empower din laboratorul CC (integritatea datelor).', 'Major', 'Closed', 'Trackwise', NULL, FALSE),
('a0Q000000048105AAA', 'TWD-000486', '2026-07-30 14:20:00+00', 'Supplier', NULL, 'PF-1103', 'Cutii Cartonaj Ilfov cu zona variabilă (lot/expirare) tipărită deplasat; lot de cutii respins la recepție.', 'Minor', 'Closed', 'Trackwise', NULL, FALSE),
('a0Q000000048110AAA', 'TWD-000490', '2026-09-08 09:30:00+00', 'Internal Audit', NULL, NULL, 'Audit intern: dosarele de lot migrate în OpenText în 2025 au primit programul generic de retenție RSI-GEN-03 în loc de RSI-GMP-BR.', 'Major', 'Open', 'Trackwise', NULL, FALSE),
('a0Q000000048115AAA', 'TWD-000493', '2026-09-01 08:00:00+00', 'Deviation', 'EK26-0329', 'PF-1101', 'Copie închidere CAPA din Veeva QMS pentru DEV-RO-000231.', 'Minor', 'Closed', 'Veeva QMS', 'DEV-RO-000231', FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS trackwise.cmpl123qms__investigation__c (
  sfid                             varchar(18) NOT NULL,
  name                             varchar(80) NOT NULL,
  cmpl123qms__quality_event__c     varchar(18) NOT NULL,
  cmpl123qms__investigator__c      varchar(18) NOT NULL,
  cmpl123qms__completed_date__c    date,
  cmpl123qms__root_cause__c        text,
  cmpl123qms__impact_assessment__c text,
  cmpl123qms__disposition__c       varchar(40),
  cmpl123qms__status__c            varchar(20) NOT NULL,
  isdeleted                        boolean NOT NULL,
  CONSTRAINT cmpl123qms__investigation__c_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE trackwise.cmpl123qms__investigation__c IS 'Investigations.';

INSERT INTO trackwise.cmpl123qms__investigation__c (sfid, name, cmpl123qms__quality_event__c, cmpl123qms__investigator__c, cmpl123qms__completed_date__c, cmpl123qms__root_cause__c, cmpl123qms__impact_assessment__c, cmpl123qms__disposition__c, cmpl123qms__status__c, isdeleted) VALUES
('a0R000000009100AAA', 'INV-TWD-000481', 'a0Q000000048100AAA', '005000000004104AAA', '2026-07-15', 'Stație Empower configurată la instalare cu un cont local comun; nicio procedură de revizuire a conturilor.', 'Revizuire audit trail 2025-2026: nicio modificare neautorizată a rezultatelor identificată.', 'No Impact', 'Complete', FALSE),
('a0R000000009101AAA', 'INV-TWD-000486', 'a0Q000000048105AAA', '005000000004105AAA', '2026-08-07', 'Șablon de tipar nevalidat la furnizor după schimbarea mașinii de tipar.', 'Nicio cutie greșită nu a ajuns în producție.', 'Reject', 'Complete', FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS trackwise.cmpl123qms__capa__c (
  sfid                         varchar(18) NOT NULL,
  name                         varchar(80) NOT NULL,
  cmpl123qms__quality_event__c varchar(18) NOT NULL,
  cmpl123qms__type__c          varchar(20) NOT NULL,
  cmpl123qms__description__c   text,
  ownerid                      varchar(18) NOT NULL,
  cmpl123qms__due_date__c      date NOT NULL,
  cmpl123qms__status__c        varchar(30) NOT NULL,
  isdeleted                    boolean NOT NULL,
  CONSTRAINT cmpl123qms__capa__c_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE trackwise.cmpl123qms__capa__c IS 'CAPA actions.';

INSERT INTO trackwise.cmpl123qms__capa__c (sfid, name, cmpl123qms__quality_event__c, cmpl123qms__type__c, cmpl123qms__description__c, ownerid, cmpl123qms__due_date__c, cmpl123qms__status__c, isdeleted) VALUES
('a0S000000037700AAA', 'TWC-000377', 'a0Q000000048100AAA', 'Corrective', 'Conturi individuale Empower legate de Active Directory; dezactivarea contului local comun.', '005000000004103AAA', '2026-08-31', 'Closed - Effective', FALSE),
('a0S000000037701AAA', 'TWC-000378', 'a0Q000000048100AAA', 'Preventive', 'Revizuire trimestrială a conturilor în sistemele GxP.', '005000000004106AAA', '2026-12-31', 'Open', FALSE),
('a0S000000037702AAA', 'TWC-000381', 'a0Q000000048105AAA', 'Corrective', 'Audit la furnizor și re-aprobarea șablonului de tipar.', '005000000004101AAA', '2026-09-30', 'Closed - Effective', FALSE),
('a0S000000037703AAA', 'TWC-000384', 'a0Q000000048110AAA', 'Corrective', 'Reclasificarea dosarelor de lot migrate în programul RSI-GMP-BR.', '005000000004100AAA', '2026-11-30', 'Open', FALSE),
('a0S000000037704AAA', 'TWC-000386', 'a0Q000000048115AAA', 'Corrective', 'Copie din Veeva QMS: CAPA-RO-000118 (înlocuire senzor presiune azot).', '005000000004102AAA', '2026-09-15', 'Closed - Effective', FALSE)
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA trackwise TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA trackwise TO egeria_user, airflow_user;
