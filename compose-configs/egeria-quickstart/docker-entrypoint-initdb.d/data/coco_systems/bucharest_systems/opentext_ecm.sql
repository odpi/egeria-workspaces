-- system-qualified-name: SoftwareServer::SYS-024::OpenText ECM
-- OpenText ECM - Bucharest.  OpenText Content Server (Extended ECM) used by EKG legal and quality to archive signed
-- batch record PDFs from the MES, supplier certificates, regulatory correspondence and contracts under records
-- management.  Its tables feed Electronic Batch Records (archived signed batch records), Supplier Material
-- Certificates (packaging certificates held only as archived PDFs) and Retention Period Assignments.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS opentext_ecm;
COMMENT ON SCHEMA opentext_ecm IS 'OpenText Content Server (EKG): DTree, KUAF, LLAttrData (category attributes) and the Records Management RSI and document cross-reference tables, lower-cased by the replication job.';

CREATE TABLE IF NOT EXISTS opentext_ecm.kuaf (
  id        integer NOT NULL,
  name      varchar(255) NOT NULL,
  firstname varchar(64),
  lastname  varchar(64),
  type      integer NOT NULL,
  CONSTRAINT kuaf_pk PRIMARY KEY (id)
);
COMMENT ON TABLE opentext_ecm.kuaf IS 'Users (type 0 = user).';

INSERT INTO opentext_ecm.kuaf (id, name, firstname, lastname, type) VALUES
(1000, 'Admin', NULL, NULL, 0),
(11207, 'apetre', 'Adina', 'Petre', 0),
(11214, 'noprea', 'Nicoleta', 'Oprea', 0),
(11231, 'renache', 'Raluca', 'Enache', 0),
(11240, 'ctudor', 'Ciprian', 'Tudor', 0),
(11255, 'svc_opcenter_sftp', NULL, NULL, 0)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opentext_ecm.dtree (
  dataid     bigint NOT NULL,
  parentid   bigint NOT NULL,
  name       varchar(248) NOT NULL,
  subtype    integer NOT NULL,
  createdate timestamptz NOT NULL,
  modifydate timestamptz NOT NULL,
  ownerid    bigint NOT NULL,
  mimetype   varchar(80),
  CONSTRAINT dtree_pk PRIMARY KEY (dataid)
);
COMMENT ON TABLE opentext_ecm.dtree IS 'Content Server nodes (subtype 0 folder, 144 document).';

INSERT INTO opentext_ecm.dtree (dataid, parentid, name, subtype, createdate, modifydate, ownerid, mimetype) VALUES
(2000101, -1, 'Enterprise', 0, '2019-03-04 10:00:00+00', '2025-06-10 09:00:00+00', 1000, NULL),
(2000210, 2000101, 'Calitate - Dosare de lot', 0, '2019-03-04 10:00:00+00', '2025-06-10 09:00:00+00', 1000, NULL),
(2000220, 2000101, 'Calitate - Certificate furnizori', 0, '2019-03-04 10:00:00+00', '2025-06-10 09:00:00+00', 1000, NULL),
(2000230, 2000101, 'Reglementare - Corespondență autorități', 0, '2019-03-04 10:00:00+00', '2025-06-10 09:00:00+00', 1000, NULL),
(2000240, 2000101, 'Juridic - Contracte', 0, '2019-03-04 10:00:00+00', '2025-06-10 09:00:00+00', 1000, NULL),
(2000250, 2000210, 'Migrare 2025 - dosare de lot scanate', 0, '2019-03-04 10:00:00+00', '2025-06-10 09:00:00+00', 1000, NULL),
(2240017, 2000210, 'EBR_EK26-0311_semnat.pdf', 144, '2026-07-23 16:40:00+00', '2026-07-23 16:40:00+00', 11255, 'application/pdf'),
(2240034, 2000210, 'EBR_EK26-0318_semnat.pdf', 144, '2026-08-06 16:40:00+00', '2026-08-06 16:40:00+00', 11255, 'application/pdf'),
(2240051, 2000210, 'EBR_EK26-0324_semnat.pdf', 144, '2026-08-20 16:40:00+00', '2026-08-20 16:40:00+00', 11255, 'application/pdf'),
(2240068, 2000210, 'EBR_EK26-0329_semnat.pdf', 144, '2026-09-04 16:40:00+00', '2026-09-04 16:40:00+00', 11255, 'application/pdf'),
(2240136, 2000210, 'EBR_SA26-0031_semnat.pdf', 144, '2026-07-16 16:40:00+00', '2026-07-16 16:40:00+00', 11255, 'application/pdf'),
(2240153, 2000210, 'EBR_SA26-0034_semnat.pdf', 144, '2026-08-06 16:40:00+00', '2026-08-06 16:40:00+00', 11255, 'application/pdf'),
(2240170, 2000210, 'EBR_SA26-0037_semnat.pdf', 144, '2026-08-27 16:40:00+00', '2026-08-27 16:40:00+00', 11255, 'application/pdf'),
(2240187, 2000210, 'EBR_SA26-0040_semnat.pdf', 144, '2026-09-17 16:40:00+00', '2026-09-17 16:40:00+00', 11255, 'application/pdf'),
(2238000, 2000250, 'Dosar_lot_EK25-0207_scanat.pdf', 144, '2025-06-10 09:30:00+00', '2025-06-10 09:30:00+00', 1000, 'application/pdf'),
(2238011, 2000250, 'Dosar_lot_EK25-0219_scanat.pdf', 144, '2025-06-10 09:31:00+00', '2025-06-10 09:31:00+00', 1000, 'application/pdf'),
(2238022, 2000250, 'Dosar_lot_EK25-0233_scanat.pdf', 144, '2025-06-10 09:32:00+00', '2025-06-10 09:32:00+00', 1000, 'application/pdf'),
(2250448, 2000220, 'SG-COC-2605-3391.pdf', 144, '2026-06-15 16:30:00+00', '2026-06-15 16:30:00+00', 11240, 'application/pdf'),
(2250469, 2000220, 'GXB-COC-26-0777.pdf', 144, '2026-07-01 11:50:00+00', '2026-07-01 11:50:00+00', 11240, 'application/pdf'),
(2250504, 2000220, 'SG-COC-2607-0412.pdf', 144, '2026-07-28 15:45:00+00', '2026-07-28 15:45:00+00', 11240, 'application/pdf'),
(2250574, 2000220, 'RPK-COC-2609-15.pdf', 144, '2026-09-26 11:20:00+00', '2026-09-26 11:20:00+00', 11240, 'application/pdf'),
(2261000, 2000230, 'ANMDMR_adresa_RPAS_oxitocina_2026.pdf', 144, '2026-06-26 12:00:00+00', '2026-06-26 12:00:00+00', 11207, 'application/pdf'),
(2261013, 2000230, 'ANMDMR_decizie_variatie_ondansetron_2026.pdf', 144, '2026-09-29 16:30:00+00', '2026-09-29 16:30:00+00', 11207, 'application/pdf'),
(2270000, 2000240, 'Contract_Carpatica_Logistic_Frig_2026.pdf', 144, '2026-01-15 10:00:00+00', '2026-01-15 10:00:00+00', 11207, 'application/pdf'),
(2270013, 2000240, 'Contract_Frigotehnica_Pantelimon_act_aditional_2026.pdf', 144, '2026-09-19 15:10:00+00', '2026-09-19 15:10:00+00', 11207, 'application/pdf')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opentext_ecm.catregionmap (
  catid    integer NOT NULL,
  catname  varchar(80),
  attrid   integer NOT NULL,
  attrname varchar(80) NOT NULL,
  CONSTRAINT catregionmap_pk PRIMARY KEY (catid, attrid)
);
COMMENT ON TABLE opentext_ecm.catregionmap IS 'Category attribute names (3001 Dosar de lot, 3002 Certificat furnizor, 3003 Corespondență, 3004 Contract).';

INSERT INTO opentext_ecm.catregionmap (catid, catname, attrid, attrname) VALUES
(3001, 'Dosar de lot', 2, 'Număr lot'),
(3001, 'Dosar de lot', 3, 'Tip document'),
(3001, 'Dosar de lot', 4, 'Sistem sursă'),
(3001, 'Dosar de lot', 5, 'Data certificării'),
(3002, 'Certificat furnizor', 2, 'Cod furnizor SAP'),
(3002, 'Certificat furnizor', 3, 'Cod material'),
(3002, 'Certificat furnizor', 4, 'Lot intern'),
(3002, 'Certificat furnizor', 5, 'Tip certificat'),
(3002, 'Certificat furnizor', 6, 'Data certificat'),
(3002, 'Certificat furnizor', 7, 'Conform'),
(3002, 'Certificat furnizor', 8, 'Număr certificat'),
(3003, 'Corespondență', 2, 'Autoritate'),
(3004, 'Contract', 2, 'Tip')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opentext_ecm.llattrdata (
  id       bigint NOT NULL,
  defid    integer NOT NULL,
  attrid   integer NOT NULL,
  entrynum integer NOT NULL,
  valstr   varchar(255),
  valdate  date,
  CONSTRAINT llattrdata_pk PRIMARY KEY (id, defid, attrid, entrynum)
);
COMMENT ON TABLE opentext_ecm.llattrdata IS 'Category attribute values per node (defid = category id).';

INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate) VALUES
(2240017, 3001, 2, 1, 'EK26-0311', NULL),
(2240017, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240017, 3001, 4, 1, 'OPCENTER', NULL),
(2240017, 3001, 5, 1, NULL, '2026-07-23'),
(2240034, 3001, 2, 1, 'EK26-0318', NULL),
(2240034, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240034, 3001, 4, 1, 'OPCENTER', NULL),
(2240034, 3001, 5, 1, NULL, '2026-08-06'),
(2240051, 3001, 2, 1, 'EK26-0324', NULL),
(2240051, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240051, 3001, 4, 1, 'OPCENTER', NULL),
(2240051, 3001, 5, 1, NULL, '2026-08-20'),
(2240068, 3001, 2, 1, 'EK26-0329', NULL),
(2240068, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240068, 3001, 4, 1, 'OPCENTER', NULL),
(2240068, 3001, 5, 1, NULL, '2026-09-04'),
(2240136, 3001, 2, 1, 'SA26-0031', NULL),
(2240136, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240136, 3001, 4, 1, 'OPCENTER', NULL),
(2240136, 3001, 5, 1, NULL, '2026-07-16'),
(2240153, 3001, 2, 1, 'SA26-0034', NULL),
(2240153, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240153, 3001, 4, 1, 'OPCENTER', NULL),
(2240153, 3001, 5, 1, NULL, '2026-08-06'),
(2240170, 3001, 2, 1, 'SA26-0037', NULL),
(2240170, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240170, 3001, 4, 1, 'OPCENTER', NULL),
(2240170, 3001, 5, 1, NULL, '2026-08-27'),
(2240187, 3001, 2, 1, 'SA26-0040', NULL),
(2240187, 3001, 3, 1, 'dosar de lot semnat', NULL),
(2240187, 3001, 4, 1, 'OPCENTER', NULL),
(2240187, 3001, 5, 1, NULL, '2026-09-17'),
(2238000, 3001, 2, 1, 'EK25-0207', NULL),
(2238000, 3001, 3, 1, 'dosar de lot scanat', NULL),
(2238000, 3001, 4, 1, 'MIGRARE', NULL),
(2238000, 3001, 5, 1, NULL, '2025-03-11'),
(2238011, 3001, 2, 1, 'EK25-0219', NULL),
(2238011, 3001, 3, 1, 'dosar de lot scanat', NULL),
(2238011, 3001, 4, 1, 'MIGRARE', NULL),
(2238011, 3001, 5, 1, NULL, '2025-04-02'),
(2238022, 3001, 2, 1, 'EK25-0233', NULL),
(2238022, 3001, 3, 1, 'dosar de lot scanat', NULL),
(2238022, 3001, 4, 1, 'MIGRARE', NULL),
(2238022, 3001, 5, 1, NULL, '2025-05-20'),
(2250448, 3002, 2, 1, '700170', NULL),
(2250448, 3002, 3, 1, 'AMB-30010', NULL),
(2250448, 3002, 4, 1, 'MP26-0064', NULL),
(2250448, 3002, 5, 1, 'COC', NULL),
(2250448, 3002, 6, 1, NULL, '2026-06-15'),
(2250448, 3002, 7, 1, 'DA', NULL),
(2250448, 3002, 8, 1, 'SG-COC-2605-3391', NULL),
(2250469, 3002, 2, 1, '700180', NULL),
(2250469, 3002, 3, 1, 'AMB-30030', NULL),
(2250469, 3002, 4, 1, 'MP26-0067', NULL),
(2250469, 3002, 5, 1, 'COC', NULL),
(2250469, 3002, 6, 1, NULL, '2026-07-01'),
(2250469, 3002, 7, 1, 'DA', NULL),
(2250469, 3002, 8, 1, 'GXB-COC-26-0777', NULL),
(2250504, 3002, 2, 1, '700170', NULL),
(2250504, 3002, 3, 1, 'AMB-30020', NULL),
(2250504, 3002, 4, 1, 'MP26-0072', NULL),
(2250504, 3002, 5, 1, 'COC', NULL),
(2250504, 3002, 6, 1, NULL, '2026-07-28'),
(2250504, 3002, 7, 1, 'DA', NULL),
(2250504, 3002, 8, 1, 'SG-COC-2607-0412', NULL),
(2250574, 3002, 2, 1, '700260', NULL),
(2250574, 3002, 3, 1, 'AMB-30050', NULL),
(2250574, 3002, 4, 1, 'MP26-0082', NULL),
(2250574, 3002, 5, 1, 'COC', NULL),
(2250574, 3002, 6, 1, NULL, '2026-09-26'),
(2250574, 3002, 7, 1, 'DA', NULL),
(2250574, 3002, 8, 1, 'RPK-COC-2609-15', NULL),
(2261000, 3003, 2, 1, 'ANMDMR', NULL),
(2261013, 3003, 2, 1, 'ANMDMR', NULL),
(2270000, 3004, 2, 1, 'contract', NULL),
(2270013, 3004, 2, 1, 'contract', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opentext_ecm.rm_rsi (
  rsi_id              integer NOT NULL,
  rsi_code            varchar(20) NOT NULL,
  title               varchar(120) NOT NULL,
  description         text NOT NULL,
  archive_after_years integer NOT NULL,
  destroy_after_years integer NOT NULL,
  trigger_event       varchar(40),
  CONSTRAINT rm_rsi_pk PRIMARY KEY (rsi_id)
);
COMMENT ON TABLE opentext_ecm.rm_rsi IS 'Records retention schedules (RSI).';

INSERT INTO opentext_ecm.rm_rsi (rsi_id, rsi_code, title, description, archive_after_years, destroy_after_years, trigger_event) VALUES
(11, 'RSI-GMP-BR', 'Documentație de lot (GMP)', 'EU GMP Partea I cap. 4.10: documentația de lot se păstrează cel puțin 1 an după expirarea lotului sau cel puțin 5 ani după certificarea de către Persoana Calificată, oricare este mai lung.', 2, 5, 'certificare'),
(12, 'RSI-GMP-COA', 'Certificate furnizor (GMP)', 'Certificatele furnizorilor se păstrează la fel ca documentația loturilor în care materialul a fost utilizat (EU GMP cap. 4).', 2, 6, 'recepție'),
(13, 'RSI-GEN-03', 'Documente generale', 'Program generic pentru documente fără clasificare, aplicat la migrare; 3 ani de la încărcare.', 1, 3, 'încărcare'),
(14, 'RSI-REG-MA', 'Corespondență autorități', 'Corespondența cu autoritățile competente se păstrează pe durata autorizației de punere pe piață plus 10 ani.', 5, 30, 'autorizație'),
(15, 'RSI-LEG-CTR', 'Contracte', 'Contractele se păstrează 10 ani după încetare (termen de prescripție, Codul civil art. 2517 și Legea 82/1991).', 3, 13, 'încetare contract')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opentext_ecm.rm_docxref (
  dataid            bigint NOT NULL,
  rsi_id            integer NOT NULL,
  rsi_assigned      timestamptz NOT NULL,
  assigned_by       integer NOT NULL,
  calc_archive_date date NOT NULL,
  calc_destroy_date date NOT NULL,
  CONSTRAINT rm_docxref_pk PRIMARY KEY (dataid)
);
COMMENT ON TABLE opentext_ecm.rm_docxref IS 'Records management classification of each document: the RSI assigned, when and by whom, and the calculated archive and destruction dates.';

INSERT INTO opentext_ecm.rm_docxref (dataid, rsi_id, rsi_assigned, assigned_by, calc_archive_date, calc_destroy_date) VALUES
(2240017, 11, '2026-07-23 16:42:00+00', 11255, '2028-07-23', '2031-07-23'),
(2240034, 11, '2026-08-06 16:42:00+00', 11255, '2028-08-06', '2031-08-06'),
(2240051, 11, '2026-08-20 16:42:00+00', 11255, '2028-08-20', '2031-08-20'),
(2240068, 11, '2026-09-04 16:42:00+00', 11255, '2028-09-04', '2031-09-04'),
(2240136, 11, '2026-07-16 16:42:00+00', 11255, '2028-07-16', '2031-07-16'),
(2240153, 11, '2026-08-06 16:42:00+00', 11255, '2028-08-06', '2031-08-06'),
(2240170, 11, '2026-08-27 16:42:00+00', 11255, '2028-08-27', '2031-08-27'),
(2240187, 11, '2026-09-17 16:42:00+00', 11255, '2028-09-17', '2031-09-17'),
(2238000, 13, '2025-06-10 09:30:00+00', 1000, '2026-06-10', '2028-06-10'),
(2238011, 13, '2025-06-10 09:31:00+00', 1000, '2026-06-10', '2028-06-10'),
(2238022, 13, '2025-06-10 09:32:00+00', 1000, '2026-06-10', '2028-06-10'),
(2250448, 12, '2026-06-15 16:35:00+00', 11240, '2028-06-15', '2032-06-15'),
(2250469, 12, '2026-07-01 11:55:00+00', 11240, '2028-07-01', '2032-07-01'),
(2250504, 12, '2026-07-28 15:50:00+00', 11240, '2028-07-28', '2032-07-28'),
(2250574, 12, '2026-09-26 11:25:00+00', 11240, '2028-09-26', '2032-09-26'),
(2261000, 14, '2026-06-26 13:00:00+00', 11207, '2031-06-26', '2056-06-26'),
(2261013, 14, '2026-09-29 17:30:00+00', 11207, '2031-09-29', '2056-09-29'),
(2270000, 15, '2026-01-16 10:00:00+00', 11207, '2029-01-15', '2039-01-15'),
(2270013, 15, '2026-09-20 15:10:00+00', 11207, '2029-09-19', '2039-09-19')
ON CONFLICT DO NOTHING;

-- Category 3005 Index dosar de lot: references indexed on the archived batch record from the data sharing hub
-- (subscription apply scripts buc_opentext_ecm__*), multi-valued (entrynum).
INSERT INTO opentext_ecm.catregionmap (catid, catname, attrid, attrname) VALUES
(3005, 'Index dosar de lot', 2, 'Lot materie primă'),
(3005, 'Index dosar de lot', 3, 'Echipament'),
(3005, 'Index dosar de lot', 4, 'Abatere'),
(3005, 'Index dosar de lot', 5, 'Certificat de analiză'),
(3005, 'Index dosar de lot', 6, 'Comandă tratament'),
(3005, 'Index dosar de lot', 7, 'Evaluare excursie temperatură'),
(3002, 'Certificat furnizor', 9, 'Denumire furnizor')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA opentext_ecm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA opentext_ecm TO egeria_user, airflow_user;
