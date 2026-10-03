-- system-qualified-name: SoftwareServer::SYS-019::Warehouse Management System (WMS)
-- Warehouse Management System (WMS) - Bucharest.  EKG's in-house warehouse system (Python/PostgreSQL, built by EKG
-- IT): receipts of SAP purchase orders, receipt inspection, quarantine, lot-level stock by warehouse zone, movements
-- including issues to production batches, and despatches with their ADR dangerous goods paperwork.  Its tables feed
-- Goods Receipts, Material Quarantine Dispositions (quarantine records), Goods Inventory Stock and Dangerous Goods
-- Consignment Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS ekg_wms;
COMMENT ON SCHEMA ekg_wms IS 'WMS intern EKG (depozit): homegrown schema with Romanian names; dates in some tables are text in Bucharest local time (DD.MM.YYYY HH24:MI), units are the WMS base units (mg, g, ml, buc).';

CREATE TABLE IF NOT EXISTS ekg_wms.articole (
  cod_art    varchar(20) NOT NULL,
  denumire   varchar(120) NOT NULL,
  um_baza    varchar(5) NOT NULL,
  um_sap     varchar(3) NOT NULL,
  factor_sap integer NOT NULL,
  stoc_min   integer,
  stoc_max   integer,
  CONSTRAINT articole_pk PRIMARY KEY (cod_art)
);
COMMENT ON TABLE ekg_wms.articole IS 'Articole: articles copied from the SAP material master, with the WMS base unit and the SAP-to-WMS factor.';

INSERT INTO ekg_wms.articole (cod_art, denumire, um_baza, um_sap, factor_sap, stoc_min, stoc_max) VALUES
('MP-10010', 'Oxitocină (substanță activă)', 'mg', 'G', 1000, 2500, 20000),
('MP-10020', 'Ceftriaxonă sodică sterilă', 'g', 'KG', 1000, 5000, 120000),
('MP-10030', 'Clorhidrat de metoclopramid', 'g', 'KG', 1000, 15000, 160000),
('MP-10040', 'Clorhidrat de ondansetron dihidrat', 'g', 'KG', 1000, 10000, 140000),
('MP-10050', 'Acetat de octreotidă', 'mg', 'G', 1000, 2000, 18000),
('MP-20010', 'Clorură de sodiu Ph. Eur.', 'g', 'KG', 1000, 20000, 180000),
('MP-40010', 'Soluție salină sterilă 0,9%', 'ml', 'L', 1000, 20000, 360000),
('AMB-30010', 'Fiolă sticlă tip I 1 ml', 'buc', 'ST', 1, 16000, 180000),
('AMB-30020', 'Fiolă sticlă tip I 2 ml', 'buc', 'ST', 1, 4000, 120000),
('AMB-30030', 'Flacon sticlă tip I 15 ml cu dop bromobutil', 'buc', 'ST', 1, 12000, 160000),
('AMB-30050', 'Flacon picurător PE 5 ml steril', 'buc', 'ST', 1, 20000, 200000),
('PF-1101', 'Oxitocină EKG 5 UI/ml soluție injectabilă', 'buc', 'ST', 1, 16000, 180000),
('PF-1102', 'Ceftriaxonă EKG 1 g pulbere pentru soluție injectabilă/perfuzabilă', 'buc', 'ST', 1, 4000, 120000),
('PF-1103', 'Metoclopramid EKG 10 mg/2 ml soluție injectabilă', 'buc', 'ST', 1, 8000, 140000),
('PF-1104', 'Ondansetron EKG 4 mg/2 ml soluție injectabilă', 'buc', 'ST', 1, 4000, 120000),
('PF-1105', 'Octreotidă EKG 0,1 mg/ml soluție injectabilă', 'buc', 'ST', 1, 8000, 140000),
('PF-9101', 'Ser autolog EKG 20% picături oftalmice (pacient nominal)', 'buc', 'ST', 1, NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.depozite (
  cod_dep  varchar(5) NOT NULL,
  denumire varchar(80) NOT NULL,
  temp_min numeric(5,1),
  temp_max numeric(5,1),
  CONSTRAINT depozite_pk PRIMARY KEY (cod_dep)
);
COMMENT ON TABLE ekg_wms.depozite IS 'Warehouse zones of the Bucharest site.';

INSERT INTO ekg_wms.depozite (cod_dep, denumire, temp_min, temp_max) VALUES
('D01', 'Materii prime și ambalaje', 15, 25),
('D02', 'Zonă carantină', 2, 25),
('D03', 'Produse finite', 15, 25),
('D04', 'Cameră frigorifică 2-8 °C', 2, 8),
('D05', 'Congelator -40 °C', -45, -18)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.receptii (
  nr_rec        varchar(20) NOT NULL,
  sap_doc_mat   varchar(10) NOT NULL,
  nr_comanda    varchar(10) NOT NULL,
  cod_furnizor  varchar(10) NOT NULL,
  cod_art       varchar(20) NOT NULL,
  lot_intern    varchar(20) NOT NULL,
  lot_furnizor  varchar(40),
  data_rec      varchar(16) NOT NULL,
  cant          integer NOT NULL,
  um            varchar(5) NOT NULL,
  depozit       varchar(5) NOT NULL,
  nr_certificat varchar(40),
  operator      varchar(20) NOT NULL,
  CONSTRAINT receptii_pk PRIMARY KEY (nr_rec)
);
COMMENT ON TABLE ekg_wms.receptii IS 'Recepții: goods received against SAP purchase orders (sap_doc_mat = the SAP goods receipt material document sent back by SAP); data_rec is text in local time.';

INSERT INTO ekg_wms.receptii (nr_rec, sap_doc_mat, nr_comanda, cod_furnizor, cod_art, lot_intern, lot_furnizor, data_rec, cant, um, depozit, nr_certificat, operator) VALUES
('REC-26-0061', '5000041207', '4500002611', '700110', 'MP-10010', 'MP26-0061', 'HPPL-OXY-2604-11', '10.06.2026 13:40', 5000, 'mg', 'D02', 'HPPL/COA/OXY/2604-11', 'dilie'),
('REC-26-0063', '5000041219', '4500002614', '700150', 'MP-20010', 'MP26-0063', 'CC-NACL-26-1187', '12.06.2026 12:15', 200000, 'g', 'D02', 'CC-BA-26-1187', 'dilie'),
('REC-26-0064', '5000041231', '4500002617', '700170', 'AMB-30010', 'MP26-0064', 'SG-A1-2605-3391', '15.06.2026 16:30', 60000, 'buc', 'D02', 'SG-COC-2605-3391', 'ctudor'),
('REC-26-0066', '5000041288', '4500002630', '700120', 'MP-10020', 'MP26-0066', 'ACSD-CTX-6621', '29.06.2026 14:20', 40000, 'g', 'D02', 'ACSD-COA-6621', 'dilie'),
('REC-26-0067', '5000041296', '4500002633', '700180', 'AMB-30030', 'MP26-0067', 'GXB-V15-26-0777', '01.07.2026 11:50', 32000, 'buc', 'D02', 'GXB-COC-26-0777', 'dilie'),
('REC-26-0069', '5000041342', '4500002641', '700140', 'MP-10050', 'MP26-0069', 'BAC-OCT-4012877', '13.07.2026 17:10', 2000, 'mg', 'D02', 'BAC-COA-4012877', 'ctudor'),
('REC-26-0071', '5000041388', '4500002652', '700130', 'MP-10030', 'MP26-0071', 'IPCA-MCP-2606088', '27.07.2026 13:05', 5000, 'g', 'D02', 'IPCA-COA-2606088', 'dilie'),
('REC-26-0072', '5000041395', '4500002655', '700170', 'AMB-30020', 'MP26-0072', 'SG-A2-2607-0412', '28.07.2026 15:45', 60000, 'buc', 'D02', 'SG-COC-2607-0412', 'dilie'),
('REC-26-0074', '5000041447', '4500002668', '700110', 'MP-10010', 'MP26-0074', 'HPPL-OXY-2607-03', '10.08.2026 14:35', 5000, 'mg', 'D02', 'HPPL/COA/OXY/2607-03', 'ctudor'),
('REC-26-0075', '5000041489', '4500002674', '700130', 'MP-10040', 'MP26-0075', 'IPCA-OND-2607114', '24.08.2026 12:55', 1000, 'g', 'D02', 'IPCA-COA-2607114', 'dilie'),
('REC-26-0077', '5000041530', '4500002683', '700240', 'MP-10050', 'MP26-0077', 'BPT-OCT-260811', '07.09.2026 18:20', 2000, 'mg', 'D02', 'BPT-COA-260811', 'dilie'),
('REC-26-0079', '5000041562', '4500002689', '700160', 'MP-40010', 'MP26-0079', 'MRK-NS-26H1904', '14.09.2026 13:30', 100000, 'ml', 'D02', 'MRK-COA-26H1904', 'ctudor'),
('REC-26-0081', '5000041601', '4500002697', '700120', 'MP-10020', 'MP26-0081', 'ACSD-CTX-6694', '21.09.2026 14:00', 40000, 'g', 'D02', 'ACSD-COA-6694', 'dilie'),
('REC-26-0082', '5000041622', '4500002699', '700260', 'AMB-30050', 'MP26-0082', 'RPK-PD5-2609-15', '24.09.2026 12:20', 3000, 'buc', 'D02', 'RPK-COC-2609-15', 'dilie')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.inspectii_receptie (
  nr_rec     varchar(20) NOT NULL,
  data_insp  date NOT NULL,
  inspector  varchar(20) NOT NULL,
  rezultat   varchar(20) NOT NULL,
  observatii text,
  CONSTRAINT inspectii_receptie_pk PRIMARY KEY (nr_rec, data_insp)
);
COMMENT ON TABLE ekg_wms.inspectii_receptie IS 'Inspecții la recepție: visual and documentary check of each receipt (ACCEPTAT, ACCEPTAT CU OBS, IN ASTEPTARE, RESPINS).';

INSERT INTO ekg_wms.inspectii_receptie (nr_rec, data_insp, inspector, rezultat, observatii) VALUES
('REC-26-0061', '2026-06-10', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0063', '2026-06-12', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0064', '2026-06-15', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0066', '2026-06-29', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0067', '2026-07-01', 'dilie', 'ACCEPTAT CU OBS', '2 paleți cu folie stretch deteriorată; cutiile interioare intacte.'),
('REC-26-0069', '2026-07-13', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0071', '2026-07-27', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0072', '2026-07-28', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0074', '2026-08-10', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0075', '2026-08-24', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0077', '2026-09-07', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0079', '2026-09-14', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0081', '2026-09-21', 'dilie', 'ACCEPTAT', NULL),
('REC-26-0082', '2026-09-24', 'dilie', 'IN ASTEPTARE', 'Certificatul de conformitate lipsește la livrare; solicitat furnizorului.'),
('REC-26-0082', '2026-09-26', 'ctudor', 'ACCEPTAT', 'Certificat RPK-COC-2609-15 primit prin e-mail și atașat.')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.carantina (
  lot_intern   varchar(20) NOT NULL,
  nr_rec       varchar(20) NOT NULL,
  data_intrare varchar(19) NOT NULL,
  depozit      varchar(5) NOT NULL,
  cant         integer NOT NULL,
  nr_proba     varchar(20),
  stare        char(1) NOT NULL,
  data_decizie varchar(19),
  CONSTRAINT carantina_pk PRIMARY KEY (lot_intern)
);
COMMENT ON TABLE ekg_wms.carantina IS 'Carantină: lots held pending the laboratory (stare C carantină, E eliberat, R respins); nr_proba = LIMS sample; dates are local-time text (YYYY-MM-DD HH24:MI:SS).';

INSERT INTO ekg_wms.carantina (lot_intern, nr_rec, data_intrare, depozit, cant, nr_proba, stare, data_decizie) VALUES
('MP26-0061', 'REC-26-0061', '2026-06-10 13:40:00', 'D02', 5000, 'S26-26001', 'E', '2026-06-19 17:20:00'),
('MP26-0063', 'REC-26-0063', '2026-06-12 12:15:00', 'D02', 200000, 'S26-26003', 'E', '2026-06-16 14:10:00'),
('MP26-0064', 'REC-26-0064', '2026-06-15 16:30:00', 'D02', 60000, 'S26-26005', 'E', '2026-06-17 13:05:00'),
('MP26-0066', 'REC-26-0066', '2026-06-29 14:20:00', 'D02', 40000, 'S26-26006', 'E', '2026-07-09 18:45:00'),
('MP26-0067', 'REC-26-0067', '2026-07-01 11:50:00', 'D02', 32000, 'S26-26008', 'E', '2026-07-03 12:30:00'),
('MP26-0069', 'REC-26-0069', '2026-07-13 17:10:00', 'D02', 2000, 'S26-26009', 'E', '2026-07-23 19:00:00'),
('MP26-0071', 'REC-26-0071', '2026-07-27 13:05:00', 'D02', 5000, 'S26-26011', 'E', '2026-08-05 15:30:00'),
('MP26-0072', 'REC-26-0072', '2026-07-28 15:45:00', 'D02', 60000, 'S26-26013', 'E', '2026-07-30 11:40:00'),
('MP26-0074', 'REC-26-0074', '2026-08-10 14:35:00', 'D02', 5000, 'S26-26014', 'E', '2026-08-20 16:15:00'),
('MP26-0075', 'REC-26-0075', '2026-08-24 12:55:00', 'D02', 1000, 'S26-26016', 'E', '2026-09-02 13:20:00'),
('MP26-0077', 'REC-26-0077', '2026-09-07 18:20:00', 'D02', 2000, 'S26-26018', 'R', '2026-09-12 15:10:00'),
('MP26-0079', 'REC-26-0079', '2026-09-14 13:30:00', 'D02', 100000, 'S26-26020', 'E', '2026-09-18 12:45:00'),
('MP26-0081', 'REC-26-0081', '2026-09-21 14:00:00', 'D02', 40000, 'S26-26022', 'C', NULL),
('MP26-0082', 'REC-26-0082', '2026-09-24 12:20:00', 'D02', 3000, 'S26-26024', 'C', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.stoc (
  cod_art    varchar(20) NOT NULL,
  depozit    varchar(5) NOT NULL,
  lot        varchar(20) NOT NULL,
  cant       integer NOT NULL,
  actualizat timestamp NOT NULL,
  CONSTRAINT stoc_pk PRIMARY KEY (cod_art, depozit, lot)
);
COMMENT ON TABLE ekg_wms.stoc IS 'Stoc: current stock by article, zone and lot (nightly recalculation, local time).';

INSERT INTO ekg_wms.stoc (cod_art, depozit, lot, cant, actualizat) VALUES
('AMB-30010', 'D01', 'MP26-0064', 2500, '2026-09-30 06:00:00'),
('AMB-30020', 'D01', 'MP26-0072', 8600, '2026-09-30 06:00:00'),
('AMB-30030', 'D01', 'MP26-0067', 1200, '2026-09-30 06:00:00'),
('AMB-30050', 'D01', 'MP25-0215', 1700, '2026-09-30 06:00:00'),
('AMB-30050', 'D02', 'MP26-0082', 3000, '2026-09-30 06:00:00'),
('MP-10010', 'D04', 'MP26-0061', 4560, '2026-09-30 06:00:00'),
('MP-10010', 'D04', 'MP26-0074', 5000, '2026-09-30 06:00:00'),
('MP-10020', 'D01', 'MP26-0066', 9400, '2026-09-30 06:00:00'),
('MP-10020', 'D02', 'MP26-0081', 40000, '2026-09-30 06:00:00'),
('MP-10030', 'D01', 'MP26-0071', 4690, '2026-09-30 06:00:00'),
('MP-10040', 'D01', 'MP26-0075', 920, '2026-09-30 06:00:00'),
('MP-10050', 'D02', 'MP26-0077', 2000, '2026-09-30 06:00:00'),
('MP-10050', 'D04', 'MP26-0069', 1180, '2026-09-30 06:00:00'),
('MP-20010', 'D01', 'MP26-0063', 198700, '2026-09-30 06:00:00'),
('MP-40010', 'D01', 'MP25-0212', 99200, '2026-09-30 06:00:00'),
('MP-40010', 'D01', 'MP26-0079', 99800, '2026-09-30 06:00:00'),
('PF-1101', 'D04', 'EK26-0311', 12000, '2026-09-30 06:00:00'),
('PF-1101', 'D04', 'EK26-0329', 24600, '2026-09-30 06:00:00'),
('PF-1102', 'D03', 'EK26-0318', 15000, '2026-09-30 06:00:00'),
('PF-1103', 'D02', 'EK26-0335', 30000, '2026-09-30 06:00:00'),
('PF-1104', 'D02', 'EK26-0341', 20000, '2026-09-30 06:00:00'),
('PF-1105', 'D04', 'EK26-0324', 5600, '2026-09-30 06:00:00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.miscari (
  id_misc      varchar(12) NOT NULL,
  tip          varchar(12) NOT NULL,
  cod_art      varchar(20) NOT NULL,
  lot          varchar(20),
  cant         integer NOT NULL,
  data_misc    varchar(16) NOT NULL,
  depozit      varchar(5) NOT NULL,
  depozit_dest varchar(5),
  ref_doc      varchar(20),
  operator     varchar(20) NOT NULL,
  CONSTRAINT miscari_pk PRIMARY KEY (id_misc)
);
COMMENT ON TABLE ekg_wms.miscari IS 'Mișcări: stock movements (INTRARE receipt, TRANSFER between zones, CONSUM issue to a production batch = ref_doc, INTRARE_PF finished goods from production, LIVRARE despatch = ref_doc); data_misc is local-time text.';

INSERT INTO ekg_wms.miscari (id_misc, tip, cod_art, lot, cant, data_misc, depozit, depozit_dest, ref_doc, operator) VALUES
('M26007', 'INTRARE', 'MP-10010', 'MP26-0061', 5000, '10.06.2026 14:10', 'D02', NULL, '5000041207', 'dilie'),
('M26014', 'TRANSFER', 'MP-10010', 'MP26-0061', 5000, '19.06.2026 18:20', 'D02', 'D04', 'UD-SAP', 'dilie'),
('M26021', 'INTRARE', 'MP-20010', 'MP26-0063', 200000, '12.06.2026 12:45', 'D02', NULL, '5000041219', 'dilie'),
('M26028', 'TRANSFER', 'MP-20010', 'MP26-0063', 200000, '16.06.2026 15:10', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26035', 'INTRARE', 'AMB-30010', 'MP26-0064', 60000, '15.06.2026 17:00', 'D02', NULL, '5000041231', 'dilie'),
('M26042', 'TRANSFER', 'AMB-30010', 'MP26-0064', 60000, '17.06.2026 14:05', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26049', 'INTRARE', 'MP-10020', 'MP26-0066', 40000, '29.06.2026 14:50', 'D02', NULL, '5000041288', 'dilie'),
('M26056', 'TRANSFER', 'MP-10020', 'MP26-0066', 40000, '09.07.2026 19:45', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26063', 'INTRARE', 'AMB-30030', 'MP26-0067', 32000, '01.07.2026 12:20', 'D02', NULL, '5000041296', 'dilie'),
('M26070', 'TRANSFER', 'AMB-30030', 'MP26-0067', 32000, '03.07.2026 13:30', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26077', 'INTRARE', 'MP-10050', 'MP26-0069', 2000, '13.07.2026 17:40', 'D02', NULL, '5000041342', 'dilie'),
('M26084', 'TRANSFER', 'MP-10050', 'MP26-0069', 2000, '23.07.2026 20:00', 'D02', 'D04', 'UD-SAP', 'dilie'),
('M26091', 'INTRARE', 'MP-10030', 'MP26-0071', 5000, '27.07.2026 13:35', 'D02', NULL, '5000041388', 'dilie'),
('M26098', 'TRANSFER', 'MP-10030', 'MP26-0071', 5000, '05.08.2026 16:30', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26105', 'INTRARE', 'AMB-30020', 'MP26-0072', 60000, '28.07.2026 16:15', 'D02', NULL, '5000041395', 'dilie'),
('M26112', 'TRANSFER', 'AMB-30020', 'MP26-0072', 60000, '30.07.2026 12:40', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26119', 'INTRARE', 'MP-10010', 'MP26-0074', 5000, '10.08.2026 15:05', 'D02', NULL, '5000041447', 'dilie'),
('M26126', 'TRANSFER', 'MP-10010', 'MP26-0074', 5000, '20.08.2026 17:15', 'D02', 'D04', 'UD-SAP', 'dilie'),
('M26133', 'INTRARE', 'MP-10040', 'MP26-0075', 1000, '24.08.2026 13:25', 'D02', NULL, '5000041489', 'dilie'),
('M26140', 'TRANSFER', 'MP-10040', 'MP26-0075', 1000, '02.09.2026 14:20', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26147', 'INTRARE', 'MP-10050', 'MP26-0077', 2000, '07.09.2026 18:50', 'D02', NULL, '5000041530', 'dilie'),
('M26154', 'INTRARE', 'MP-40010', 'MP26-0079', 100000, '14.09.2026 14:00', 'D02', NULL, '5000041562', 'dilie'),
('M26161', 'TRANSFER', 'MP-40010', 'MP26-0079', 100000, '18.09.2026 13:45', 'D02', 'D01', 'UD-SAP', 'dilie'),
('M26168', 'INTRARE', 'MP-10020', 'MP26-0081', 40000, '21.09.2026 14:30', 'D02', NULL, '5000041601', 'dilie'),
('M26175', 'INTRARE', 'AMB-30050', 'MP26-0082', 3000, '24.09.2026 12:50', 'D02', NULL, '5000041622', 'dilie'),
('M26182', 'CONSUM', 'MP-10010', 'MP26-0061', 220, '06.07.2026 07:00', 'D04', NULL, 'EK26-0311', 'dilie'),
('M26189', 'CONSUM', 'MP-20010', 'MP26-0063', 220, '06.07.2026 07:00', 'D01', NULL, 'EK26-0311', 'dilie'),
('M26196', 'CONSUM', 'AMB-30010', 'MP26-0064', 24600, '06.07.2026 07:00', 'D01', NULL, 'EK26-0311', 'dilie'),
('M26203', 'CONSUM', 'MP-10020', 'MP26-0066', 15300, '20.07.2026 07:00', 'D01', NULL, 'EK26-0318', 'dilie'),
('M26210', 'CONSUM', 'AMB-30030', 'MP26-0067', 15400, '20.07.2026 07:00', 'D01', NULL, 'EK26-0318', 'dilie'),
('M26217', 'CONSUM', 'MP-10050', 'MP26-0069', 820, '03.08.2026 07:00', 'D04', NULL, 'EK26-0324', 'dilie'),
('M26224', 'CONSUM', 'AMB-30010', 'MP26-0064', 8300, '03.08.2026 07:00', 'D01', NULL, 'EK26-0324', 'dilie'),
('M26231', 'CONSUM', 'MP-10010', 'MP26-0061', 220, '17.08.2026 07:00', 'D04', NULL, 'EK26-0329', 'dilie'),
('M26238', 'CONSUM', 'MP-20010', 'MP26-0063', 220, '17.08.2026 07:00', 'D01', NULL, 'EK26-0329', 'dilie'),
('M26245', 'CONSUM', 'AMB-30010', 'MP26-0064', 24600, '17.08.2026 07:00', 'D01', NULL, 'EK26-0329', 'dilie'),
('M26252', 'CONSUM', 'MP-10030', 'MP26-0071', 310, '31.08.2026 07:00', 'D01', NULL, 'EK26-0335', 'dilie'),
('M26259', 'CONSUM', 'MP-20010', 'MP26-0063', 500, '31.08.2026 07:00', 'D01', NULL, 'EK26-0335', 'dilie'),
('M26266', 'CONSUM', 'AMB-30020', 'MP26-0072', 30800, '31.08.2026 07:00', 'D01', NULL, 'EK26-0335', 'dilie'),
('M26273', 'CONSUM', 'MP-10040', 'MP26-0075', 80, '14.09.2026 07:00', 'D01', NULL, 'EK26-0341', 'dilie'),
('M26280', 'CONSUM', 'MP-20010', 'MP26-0063', 360, '14.09.2026 07:00', 'D01', NULL, 'EK26-0341', 'dilie'),
('M26287', 'CONSUM', 'AMB-30020', 'MP26-0072', 20600, '14.09.2026 07:00', 'D01', NULL, 'EK26-0341', 'dilie'),
('M26294', 'CONSUM', 'MP-10020', 'MP26-0066', 15300, '28.09.2026 07:00', 'D01', NULL, 'EK26-0347', 'dilie'),
('M26301', 'CONSUM', 'AMB-30030', 'MP26-0067', 15400, '28.09.2026 07:00', 'D01', NULL, 'EK26-0347', 'dilie'),
('M26308', 'CONSUM', 'MP-40010', 'MP25-0212', 200, '14.07.2026 13:00', 'D01', NULL, 'SA26-0031', 'dilie'),
('M26315', 'CONSUM', 'AMB-30050', 'MP25-0215', 60, '14.07.2026 13:00', 'D01', NULL, 'SA26-0031', 'dilie'),
('M26322', 'CONSUM', 'MP-40010', 'MP25-0212', 200, '04.08.2026 14:00', 'D01', NULL, 'SA26-0034', 'dilie'),
('M26329', 'CONSUM', 'AMB-30050', 'MP25-0215', 60, '04.08.2026 14:00', 'D01', NULL, 'SA26-0034', 'dilie'),
('M26336', 'CONSUM', 'MP-40010', 'MP25-0212', 200, '26.08.2026 08:00', 'D01', NULL, 'SA26-0037', 'dilie'),
('M26343', 'CONSUM', 'AMB-30050', 'MP25-0215', 60, '26.08.2026 08:00', 'D01', NULL, 'SA26-0037', 'dilie'),
('M26350', 'CONSUM', 'MP-40010', 'MP25-0212', 200, '16.09.2026 08:00', 'D01', NULL, 'SA26-0040', 'dilie'),
('M26357', 'CONSUM', 'AMB-30050', 'MP25-0215', 60, '16.09.2026 08:00', 'D01', NULL, 'SA26-0040', 'dilie'),
('M26364', 'CONSUM', 'MP-40010', 'MP26-0079', 200, '29.09.2026 14:00', 'D01', NULL, 'SA26-0042', 'dilie'),
('M26371', 'CONSUM', 'AMB-30050', 'MP25-0215', 60, '29.09.2026 14:00', 'D01', NULL, 'SA26-0042', 'dilie'),
('M26378', 'INTRARE_PF', 'PF-1101', 'EK26-0311', 24000, '08.07.2026 22:00', 'D02', NULL, '4000311', 'dilie'),
('M26385', 'TRANSFER', 'PF-1101', 'EK26-0311', 24000, '23.07.2026 20:00', 'D02', 'D04', 'ELIB-QP', 'dilie'),
('M26392', 'INTRARE_PF', 'PF-1102', 'EK26-0318', 15000, '22.07.2026 20:00', 'D02', NULL, '4000318', 'dilie'),
('M26399', 'TRANSFER', 'PF-1102', 'EK26-0318', 15000, '06.08.2026 20:00', 'D02', 'D03', 'ELIB-QP', 'dilie'),
('M26406', 'INTRARE_PF', 'PF-1105', 'EK26-0324', 8000, '05.08.2026 21:00', 'D02', NULL, '4000324', 'dilie'),
('M26413', 'TRANSFER', 'PF-1105', 'EK26-0324', 8000, '20.08.2026 20:00', 'D02', 'D04', 'ELIB-QP', 'dilie'),
('M26420', 'INTRARE_PF', 'PF-1101', 'EK26-0329', 30000, '19.08.2026 22:00', 'D02', NULL, '4000329', 'dilie'),
('M26427', 'TRANSFER', 'PF-1101', 'EK26-0329', 30000, '04.09.2026 20:00', 'D02', 'D04', 'ELIB-QP', 'dilie'),
('M26434', 'INTRARE_PF', 'PF-1103', 'EK26-0335', 30000, '02.09.2026 22:00', 'D02', NULL, '4000335', 'dilie'),
('M26441', 'INTRARE_PF', 'PF-1104', 'EK26-0341', 20000, '16.09.2026 21:00', 'D02', NULL, '4000341', 'dilie'),
('M26448', 'INTRARE_PF', 'PF-9101', 'SA26-0031', 56, '15.07.2026 22:00', 'D02', NULL, '4100031', 'dilie'),
('M26455', 'TRANSFER', 'PF-9101', 'SA26-0031', 56, '16.07.2026 20:00', 'D02', 'D05', 'ELIB-QP', 'dilie'),
('M26462', 'INTRARE_PF', 'PF-9101', 'SA26-0034', 56, '05.08.2026 23:00', 'D02', NULL, '4100034', 'dilie'),
('M26469', 'TRANSFER', 'PF-9101', 'SA26-0034', 56, '06.08.2026 20:00', 'D02', 'D05', 'ELIB-QP', 'dilie'),
('M26476', 'INTRARE_PF', 'PF-9101', 'SA26-0037', 56, '27.08.2026 18:00', 'D02', NULL, '4100037', 'dilie'),
('M26483', 'TRANSFER', 'PF-9101', 'SA26-0037', 56, '27.08.2026 20:00', 'D02', 'D05', 'ELIB-QP', 'dilie'),
('M26490', 'INTRARE_PF', 'PF-9101', 'SA26-0040', 56, '17.09.2026 18:00', 'D02', NULL, '4100040', 'dilie'),
('M26497', 'TRANSFER', 'PF-9101', 'SA26-0040', 56, '17.09.2026 20:00', 'D02', 'D05', 'ELIB-QP', 'dilie'),
('M26504', 'LIVRARE', 'PF-9101', 'SA26-0031', 56, '17.07.2026 10:50', 'D05', NULL, 'EXP-26-0391', 'dilie'),
('M26511', 'LIVRARE', 'PF-1101', 'EK26-0311', 6000, '27.07.2026 09:20', 'D04', NULL, 'EXP-26-0396', 'dilie'),
('M26518', 'LIVRARE', 'PF-9101', 'SA26-0034', 56, '07.08.2026 10:35', 'D05', NULL, 'EXP-26-0403', 'dilie'),
('M26525', 'LIVRARE', 'PF-1101', 'EK26-0311', 6000, '12.08.2026 07:50', 'D04', NULL, 'EXP-26-0407', 'dilie'),
('M26532', 'LIVRARE', 'PF-1105', 'EK26-0324', 2400, '24.08.2026 09:30', 'D04', NULL, 'EXP-26-0409', 'dilie'),
('M26539', 'LIVRARE', 'PF-9101', 'SA26-0037', 56, '28.08.2026 10:00', 'D05', NULL, 'EXP-26-0411', 'dilie'),
('M26546', 'LIVRARE', 'PF-1101', 'EK26-0329', 5400, '15.09.2026 07:50', 'D04', NULL, 'EXP-26-0418', 'dilie'),
('M26553', 'LIVRARE', 'PF-9101', 'SA26-0040', 56, '18.09.2026 09:50', 'D05', NULL, 'EXP-26-0420', 'dilie')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.expeditii (
  nr_exp            varchar(20) NOT NULL,
  cod_client        varchar(10) NOT NULL,
  cod_transportator varchar(10) NOT NULL,
  data_exp          varchar(16) NOT NULL,
  adresa_livrare    text NOT NULL,
  nr_onu            varchar(10),
  cant_adr          numeric(8,2),
  um_adr            varchar(5),
  semnatar          varchar(20),
  data_semnare      varchar(16),
  nr_cert_semnatar  varchar(40),
  logger            varchar(20),
  CONSTRAINT expeditii_pk PRIMARY KEY (nr_exp)
);
COMMENT ON TABLE ekg_wms.expeditii IS 'Expediții: despatches; for dry-ice consignments the ADR fields (UN number, quantity, signatory and the ADR 1.3 training certificate authorising the signature).';

INSERT INTO ekg_wms.expeditii (nr_exp, cod_client, cod_transportator, data_exp, adresa_livrare, nr_onu, cant_adr, um_adr, semnatar, data_semnare, nr_cert_semnatar, logger) VALUES
('EXP-26-0391', '800110', '700250', '17.07.2026 11:30', 'Spitalul Clinic de Urgență Oftalmologică, Farmacie, Piața Alexandru Lahovari 1, 010464 București, RO', 'UN1845', 6.0, 'kg', 'dilie', '17.07.2026 11:05', 'ADR-1.3-EKG-2025-017', 'PCM-T20-00417'),
('EXP-26-0396', '800010', '700220', '27.07.2026 10:00', 'Farmexpert D.C.I. S.R.L., Depozit central, Bd. Theodor Pallady 287, 032258 București, RO', NULL, NULL, NULL, NULL, NULL, NULL, 'PCM-T20-00422'),
('EXP-26-0403', '800110', '700250', '07.08.2026 11:15', 'Spitalul Clinic de Urgență Oftalmologică, Farmacie, Piața Alexandru Lahovari 1, 010464 București, RO', 'UN1845', 6.0, 'kg', 'ctudor', '07.08.2026 10:50', 'ADR-1.3-EKG-2024-009', 'PCM-T20-00417'),
('EXP-26-0407', '800220', '700220', '12.08.2026 08:30', 'Moldfarm Distribuție S.R.L., Depozit, Str. Uzinelor 21, MD-2023 Chișinău, MD', NULL, NULL, NULL, NULL, NULL, NULL, 'PCM-L4G-00031'),
('EXP-26-0409', '800020', '700220', '24.08.2026 10:10', 'Mediplus Exim S.R.L., Str. Nicolae Teclu 19, 032368 București, RO', NULL, NULL, NULL, NULL, NULL, NULL, 'PCM-T20-00422'),
('EXP-26-0411', '800120', '700250', '28.08.2026 10:40', 'Spitalul Clinic Județean de Urgență Cluj-Napoca, Farmacie, Str. Clinicilor 3-5, 400006 Cluj-Napoca, RO', 'UN1845', 12.0, 'kg', 'dilie', '28.08.2026 10:15', 'ADR-1.3-EKG-2025-017', 'PCM-L4G-00034'),
('EXP-26-0418', '800220', '700220', '15.09.2026 08:30', 'Moldfarm Distribuție S.R.L., Depozit, Str. Uzinelor 21, MD-2023 Chișinău, MD', NULL, NULL, NULL, NULL, NULL, NULL, 'PCM-L4G-00031'),
('EXP-26-0420', '800130', '700250', '18.09.2026 10:30', 'Spitalul Clinic Județean de Urgență Sf. Spiridon, Farmacie, Bd. Independenței 1, 700111 Iași, RO', 'UN1845', 12.0, 'kg', 'dilie', '18.09.2026 10:05', 'ADR-1.3-EKG-2025-017', 'PCM-L4G-00034')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ekg_wms.documente_exp (
  nr_exp   varchar(20) NOT NULL,
  nr_doc   varchar(40) NOT NULL,
  tip_doc  varchar(30) NOT NULL,
  data_doc date NOT NULL,
  CONSTRAINT documente_exp_pk PRIMARY KEY (nr_exp, nr_doc)
);
COMMENT ON TABLE ekg_wms.documente_exp IS 'Documente expediție: documents accompanying a despatch.';

INSERT INTO ekg_wms.documente_exp (nr_exp, nr_doc, tip_doc, data_doc) VALUES
('EXP-26-0391', 'DGD-26-0391', 'DECLARATIE_ADR', '2026-07-17'),
('EXP-26-0391', 'AV-EKG-0012391', 'AVIZ_INSOTIRE', '2026-07-17'),
('EXP-26-0391', 'FCT-26-0391', 'FISA_TEMPERATURA', '2026-07-17'),
('EXP-26-0403', 'DGD-26-0403', 'DECLARATIE_ADR', '2026-08-07'),
('EXP-26-0403', 'AV-EKG-0012403', 'AVIZ_INSOTIRE', '2026-08-07'),
('EXP-26-0403', 'FCT-26-0403', 'FISA_TEMPERATURA', '2026-08-07'),
('EXP-26-0411', 'DGD-26-0411', 'DECLARATIE_ADR', '2026-08-28'),
('EXP-26-0411', 'AV-EKG-0012411', 'AVIZ_INSOTIRE', '2026-08-28'),
('EXP-26-0411', 'FCT-26-0411', 'FISA_TEMPERATURA', '2026-08-28'),
('EXP-26-0420', 'DGD-26-0420', 'DECLARATIE_ADR', '2026-09-18'),
('EXP-26-0420', 'AV-EKG-0012420', 'AVIZ_INSOTIRE', '2026-09-18'),
('EXP-26-0420', 'FCT-26-0420', 'FISA_TEMPERATURA', '2026-09-18')
ON CONFLICT DO NOTHING;

-- Interface tables filled from the data sharing hub (subscription apply scripts buc_ekg_wms__*).  Same homegrown style.
CREATE TABLE IF NOT EXISTS ekg_wms.furnizori (
  cod_furnizor varchar(10) NOT NULL,
  denumire     varchar(200) NOT NULL,
  tara         varchar(60),
  aprobat      char(1) NOT NULL,
  data_aprob   date,
  stare        varchar(20) NOT NULL,
  actualizat   timestamp NOT NULL,
  CONSTRAINT furnizori_pk PRIMARY KEY (cod_furnizor)
);
COMMENT ON TABLE ekg_wms.furnizori IS 'Furnizori: SAP vendors the WMS may receive from (aprobat D/N = approved), copied from the supplier master; checked at receipt.';

CREATE TABLE IF NOT EXISTS ekg_wms.certificate_furnizor (
  nr_certificat varchar(40) NOT NULL,
  cod_furnizor  varchar(10),
  cod_art       varchar(20),
  lot           varchar(40),
  tip_cert      varchar(3) NOT NULL,
  data_cert     date,
  conform       char(1) NOT NULL,
  actualizat    timestamp NOT NULL,
  CONSTRAINT certificate_furnizor_pk PRIMARY KEY (nr_certificat)
);
COMMENT ON TABLE ekg_wms.certificate_furnizor IS 'Certificate furnizor: supplier certificates (COA/COC, conform D/N) registered in LIMS or the ECM, checked against receptii.nr_certificat at receipt.';

CREATE TABLE IF NOT EXISTS ekg_wms.buletine_analiza (
  nr_buletin  varchar(40) NOT NULL,
  lot_intern  varchar(20) NOT NULL,
  data_bul    date,
  conform     char(1) NOT NULL,
  aprobat_de  varchar(20),
  actualizat  timestamp NOT NULL,
  CONSTRAINT buletine_analiza_pk PRIMARY KEY (nr_buletin)
);
COMMENT ON TABLE ekg_wms.buletine_analiza IS 'Buletine de analiză: the LIMS release bulletin (BA-) of each quarantined lot, conform D/N.';

CREATE TABLE IF NOT EXISTS ekg_wms.imp_decizii_sap (
  lot_intern   varchar(20) NOT NULL,
  data_decizie timestamp NOT NULL,
  decizie      char(1) NOT NULL,
  nr_rezultat  varchar(40),
  data_exp     date,
  cant_elib    integer,
  importat     timestamp NOT NULL,
  CONSTRAINT imp_decizii_sap_pk PRIMARY KEY (lot_intern, data_decizie)
);
COMMENT ON TABLE ekg_wms.imp_decizii_sap IS 'Import decizii SAP: SAP QM usage decisions per lot (decizie E eliberat / R respins, local time) waiting to release or reject the quarantine record.';

CREATE TABLE IF NOT EXISTS ekg_wms.serii_ambalaj (
  nr_serie    varchar(40) NOT NULL,
  cod_art     varchar(20) NOT NULL,
  gtin        varchar(20),
  lot         varchar(40),
  data_exp    date,
  piata       varchar(8),
  stare       varchar(20) NOT NULL,
  sscc_parinte varchar(40),
  depozit     varchar(5),
  actualizat  timestamp NOT NULL,
  CONSTRAINT serii_ambalaj_pk PRIMARY KEY (nr_serie)
);
COMMENT ON TABLE ekg_wms.serii_ambalaj IS 'Serii ambalaj: serialised packs held in stock (GTIN.serial), with their current state, parent case and zone.';

CREATE TABLE IF NOT EXISTS ekg_wms.clasificari_adr (
  id_clasif    varchar(40) NOT NULL,
  cod_art      varchar(20) NOT NULL,
  nr_onu       varchar(20) NOT NULL,
  grupa_amb    varchar(5),
  clasa        varchar(10),
  etichetare   text,
  documente    text,
  data_clasif  date,
  CONSTRAINT clasificari_adr_pk PRIMARY KEY (id_clasif)
);
COMMENT ON TABLE ekg_wms.clasificari_adr IS 'Clasificări ADR: dangerous goods classification of each article (UN number, packing group, class, labels and documents) used to prepare despatches.';

GRANT USAGE ON SCHEMA ekg_wms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ekg_wms TO egeria_user, airflow_user;
