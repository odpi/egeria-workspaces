-- system-qualified-name: SoftwareServer::SYS-001::SAP ERP S/4HANA
-- SAP ERP S/4HANA - Bucharest.  The EKG ERP (client 300, company code RO01, plant RO10, RON with EUR suppliers):
-- production planning incl. the named-patient serum orders, QM usage decisions, the supplier master with EKG's
-- screening and bank-verification Z tables, invoice verification, the payment run, billing, the universal journal with
-- its inbound IDoc feeds (Opcenter, Concur, Workday, Maximo, WMS) and parked journals with their approval workflow.
-- Its tables feed Personalised Manufacturing Schedule, Supplier Master Data, Material Quarantine Dispositions (usage
-- decisions), Treatment Invoices, Subledger Postings, Manual Journal Approvals, Supplier Payments and General Ledger
-- Balances.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS sap_s4hana;
COMMENT ON SCHEMA sap_s4hana IS 'SAP S/4HANA (EKG): SAP tables as replicated by SAP SLT (lower-case names; DATS/TIMS kept as YYYYMMDD/HHMMSS text).';

CREATE TABLE IF NOT EXISTS sap_s4hana.aufk (
  mandt                varchar(3) NOT NULL,
  aufnr                varchar(12) NOT NULL,
  auart                varchar(4) NOT NULL,
  werks                varchar(4) NOT NULL,
  bukrs                varchar(4) NOT NULL,
  ktext                varchar(40),
  erdat                varchar(8) NOT NULL,
  objnr                varchar(22) NOT NULL,
  zz_treatment_order   varchar(20),
  zz_patient_pseudonym varchar(40),
  zz_patient_params    varchar(255),
  CONSTRAINT aufk_pk PRIMARY KEY (mandt, aufnr)
);
COMMENT ON TABLE sap_s4hana.aufk IS 'Order master (ZP01 process order; ZPAT named-patient serum order carrying the sales order and patient pseudonym).';

INSERT INTO sap_s4hana.aufk (mandt, aufnr, auart, werks, bukrs, ktext, erdat, objnr, zz_treatment_order, zz_patient_pseudonym, zz_patient_params) VALUES
('300', '4000311', 'ZP01', 'RO10', 'RO01', 'PF-1101 lot EK26-0311', '20260629', 'OR000004000311', NULL, NULL, NULL),
('300', '4000318', 'ZP01', 'RO10', 'RO01', 'PF-1102 lot EK26-0318', '20260713', 'OR000004000318', NULL, NULL, NULL),
('300', '4000324', 'ZP01', 'RO10', 'RO01', 'PF-1105 lot EK26-0324', '20260727', 'OR000004000324', NULL, NULL, NULL),
('300', '4000329', 'ZP01', 'RO10', 'RO01', 'PF-1101 lot EK26-0329', '20260810', 'OR000004000329', NULL, NULL, NULL),
('300', '4000335', 'ZP01', 'RO10', 'RO01', 'PF-1103 lot EK26-0335', '20260824', 'OR000004000335', NULL, NULL, NULL),
('300', '4000341', 'ZP01', 'RO10', 'RO01', 'PF-1104 lot EK26-0341', '20260907', 'OR000004000341', NULL, NULL, NULL),
('300', '4000347', 'ZP01', 'RO10', 'RO01', 'PF-1102 lot EK26-0347', '20260921', 'OR000004000347', NULL, NULL, NULL),
('300', '4100031', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0031', '20260707', 'OR000004100031', '120031', 'PP-993A9A3720FB', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 2 x 450 ml'),
('300', '4100034', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0034', '20260728', 'OR000004100034', '120034', 'PP-385F3C95C17E', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 2 x 450 ml'),
('300', '4100037', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0037', '20260819', 'OR000004100037', '120037', 'PP-7A15F037482B', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 2 x 450 ml'),
('300', '4100040', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0040', '20260909', 'OR000004100040', '120040', 'PP-52094070B986', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 3 x 450 ml'),
('300', '4100042', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0042', '20260922', 'OR000004100042', '120042', 'PP-22773F9CC79C', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 2 x 450 ml'),
('300', '4100044', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0044', '20260929', 'OR000004100044', '120044', 'PP-1A8B4DC35A0E', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 2 x 450 ml'),
('300', '4100045', 'ZPAT', 'RO10', 'RO01', 'PF-9101 lot SA26-0045', '20261001', 'OR000004100045', '120045', 'PP-80760AE35BFE', 'Ser autolog 20% în NaCl 0,9%; 56 flacoane picurătoare 5 ml; donație 3 x 450 ml')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.afko (
  mandt  varchar(3) NOT NULL,
  aufnr  varchar(12) NOT NULL,
  gstrp  varchar(8) NOT NULL,
  gsuzp  varchar(6) NOT NULL,
  gltrp  varchar(8) NOT NULL,
  gluzp  varchar(6) NOT NULL,
  gstri  varchar(8),
  gsuzi  varchar(6),
  getri  varchar(8),
  geuzi  varchar(6),
  plnbez varchar(40),
  CONSTRAINT afko_pk PRIMARY KEY (mandt, aufnr)
);
COMMENT ON TABLE sap_s4hana.afko IS 'Order header scheduling data: scheduled (gstrp/gltrp) and actual (gstri/getri) start and finish, UTC.';

INSERT INTO sap_s4hana.afko (mandt, aufnr, gstrp, gsuzp, gltrp, gluzp, gstri, gsuzi, getri, geuzi, plnbez) VALUES
('300', '4000311', '20260706', '060000', '20260708', '160000', '20260706', '060000', '20260708', '160000', 'PF-1101'),
('300', '4000318', '20260720', '060000', '20260722', '140000', '20260720', '060000', '20260722', '140000', 'PF-1102'),
('300', '4000324', '20260803', '060000', '20260805', '150000', '20260803', '060000', '20260805', '150000', 'PF-1105'),
('300', '4000329', '20260817', '060000', '20260819', '160000', '20260817', '060000', '20260819', '160000', 'PF-1101'),
('300', '4000335', '20260831', '060000', '20260902', '160000', '20260831', '060000', '20260902', '160000', 'PF-1103'),
('300', '4000341', '20260914', '060000', '20260916', '150000', '20260914', '060000', '20260916', '150000', 'PF-1104'),
('300', '4000347', '20260928', '060000', '20260930', '160000', '20260928', '060000', NULL, NULL, 'PF-1102'),
('300', '4100031', '20260714', '120000', '20260715', '160000', '20260714', '120000', '20260715', '160000', 'PF-9101'),
('300', '4100034', '20260804', '130000', '20260805', '170000', '20260804', '130000', '20260805', '170000', 'PF-9101'),
('300', '4100037', '20260826', '070000', '20260827', '120000', '20260826', '070000', '20260827', '120000', 'PF-9101'),
('300', '4100040', '20260916', '070000', '20260917', '120000', '20260916', '070000', '20260917', '120000', 'PF-9101'),
('300', '4100042', '20260929', '130000', '20260930', '170000', '20260929', '130000', NULL, NULL, 'PF-9101'),
('300', '4100044', '20261006', '070000', '20261007', '120000', NULL, NULL, NULL, NULL, 'PF-9101'),
('300', '4100045', '20261008', '070000', '20261009', '120000', NULL, NULL, NULL, NULL, 'PF-9101')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.afpo (
  mandt varchar(3) NOT NULL,
  aufnr varchar(12) NOT NULL,
  posnr varchar(4) NOT NULL,
  matnr varchar(40) NOT NULL,
  charg varchar(20),
  psmng numeric(13,3) NOT NULL,
  meins varchar(3) NOT NULL,
  dwerk varchar(4) NOT NULL,
  CONSTRAINT afpo_pk PRIMARY KEY (mandt, aufnr, posnr)
);
COMMENT ON TABLE sap_s4hana.afpo IS 'Order item: the material and batch produced.';

INSERT INTO sap_s4hana.afpo (mandt, aufnr, posnr, matnr, charg, psmng, meins, dwerk) VALUES
('300', '4000311', '0001', 'PF-1101', 'EK26-0311', 24000, 'ST', 'RO10'),
('300', '4000318', '0001', 'PF-1102', 'EK26-0318', 15000, 'ST', 'RO10'),
('300', '4000324', '0001', 'PF-1105', 'EK26-0324', 8000, 'ST', 'RO10'),
('300', '4000329', '0001', 'PF-1101', 'EK26-0329', 30000, 'ST', 'RO10'),
('300', '4000335', '0001', 'PF-1103', 'EK26-0335', 30000, 'ST', 'RO10'),
('300', '4000341', '0001', 'PF-1104', 'EK26-0341', 20000, 'ST', 'RO10'),
('300', '4000347', '0001', 'PF-1102', 'EK26-0347', 15000, 'ST', 'RO10'),
('300', '4100031', '0001', 'PF-9101', 'SA26-0031', 56, 'ST', 'RO10'),
('300', '4100034', '0001', 'PF-9101', 'SA26-0034', 56, 'ST', 'RO10'),
('300', '4100037', '0001', 'PF-9101', 'SA26-0037', 56, 'ST', 'RO10'),
('300', '4100040', '0001', 'PF-9101', 'SA26-0040', 56, 'ST', 'RO10'),
('300', '4100042', '0001', 'PF-9101', 'SA26-0042', 56, 'ST', 'RO10'),
('300', '4100044', '0001', 'PF-9101', 'SA26-0044', 56, 'ST', 'RO10'),
('300', '4100045', '0001', 'PF-9101', 'SA26-0045', 56, 'ST', 'RO10')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.jest (
  mandt varchar(3) NOT NULL,
  objnr varchar(22) NOT NULL,
  stat  varchar(5) NOT NULL,
  inact varchar(1),
  CONSTRAINT jest_pk PRIMARY KEY (mandt, objnr, stat)
);
COMMENT ON TABLE sap_s4hana.jest IS 'Object status (I0001 CRTD, I0002 REL, I0009 CNF, I0045 TECO, I0076 DLFL).';

INSERT INTO sap_s4hana.jest (mandt, objnr, stat, inact) VALUES
('300', 'OR000004000311', 'I0002', NULL),
('300', 'OR000004000311', 'I0009', NULL),
('300', 'OR000004000311', 'I0045', NULL),
('300', 'OR000004000318', 'I0002', NULL),
('300', 'OR000004000318', 'I0009', NULL),
('300', 'OR000004000318', 'I0045', NULL),
('300', 'OR000004000324', 'I0002', NULL),
('300', 'OR000004000324', 'I0009', NULL),
('300', 'OR000004000324', 'I0045', NULL),
('300', 'OR000004000329', 'I0002', NULL),
('300', 'OR000004000329', 'I0009', NULL),
('300', 'OR000004000329', 'I0045', NULL),
('300', 'OR000004000335', 'I0002', NULL),
('300', 'OR000004000335', 'I0009', NULL),
('300', 'OR000004000335', 'I0045', NULL),
('300', 'OR000004000341', 'I0002', NULL),
('300', 'OR000004000341', 'I0009', NULL),
('300', 'OR000004000341', 'I0045', NULL),
('300', 'OR000004000347', 'I0002', NULL),
('300', 'OR000004100031', 'I0002', NULL),
('300', 'OR000004100031', 'I0009', NULL),
('300', 'OR000004100031', 'I0045', NULL),
('300', 'OR000004100034', 'I0002', NULL),
('300', 'OR000004100034', 'I0009', NULL),
('300', 'OR000004100034', 'I0045', NULL),
('300', 'OR000004100037', 'I0002', NULL),
('300', 'OR000004100037', 'I0009', NULL),
('300', 'OR000004100037', 'I0045', NULL),
('300', 'OR000004100040', 'I0002', NULL),
('300', 'OR000004100040', 'I0009', NULL),
('300', 'OR000004100040', 'I0045', NULL),
('300', 'OR000004100042', 'I0002', NULL),
('300', 'OR000004100044', 'I0001', NULL),
('300', 'OR000004100044', 'I0076', NULL),
('300', 'OR000004100045', 'I0001', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.likp (
  mandt                varchar(3) NOT NULL,
  vbeln                varchar(10) NOT NULL,
  lfart                varchar(4) NOT NULL,
  lifex                varchar(35),
  lfdat                varchar(8) NOT NULL,
  lfuhr                varchar(6) NOT NULL,
  lifnr                varchar(10),
  zz_patient_pseudonym varchar(40),
  zz_arrival_cond      varchar(255),
  zz_viable_hours      integer,
  wbstk                varchar(1) NOT NULL,
  CONSTRAINT likp_pk PRIMARY KEY (mandt, vbeln)
);
COMMENT ON TABLE sap_s4hana.likp IS 'Inbound deliveries of type ZPMI (patient blood donation): lifex = courier AWB, wbstk C = received; arrival date/time UTC.';

INSERT INTO sap_s4hana.likp (mandt, vbeln, lfart, lifex, lfdat, lfuhr, lifnr, zz_patient_pseudonym, zz_arrival_cond, zz_viable_hours, wbstk) VALUES
('300', '1800005310', 'ZPMI', 'UMC-26-004512', '20260714', '094000', '0000700250', 'PP-993A9A3720FB', '2 pungi donație sânge integral, 2-8 °C, sigilii intacte; etichete identitate pacient verificate cu cererea spitalului', 36, 'C'),
('300', '1800005311', 'ZPMI', 'UMC-26-004733', '20260804', '101500', '0000700250', 'PP-385F3C95C17E', '2 pungi donație sânge integral, 2-8 °C, sigilii intacte; etichete identitate pacient verificate cu cererea spitalului', 36, 'C'),
('300', '1800005312', 'ZPMI', 'UMC-26-004981', '20260825', '162000', '0000700250', 'PP-7A15F037482B', '2 pungi donație sânge integral, 2-8 °C, sigilii intacte; etichete identitate pacient verificate cu cererea spitalului', 30, 'C'),
('300', '1800005313', 'ZPMI', 'UMC-26-005204', '20260915', '150500', '0000700250', 'PP-52094070B986', '2 pungi donație sânge integral, 2-8 °C, sigilii intacte; etichete identitate pacient verificate cu cererea spitalului', 30, 'C'),
('300', '1800005314', 'ZPMI', 'UMC-26-005398', '20260929', '101500', '0000700250', 'PP-22773F9CC79C', '2 pungi donație sânge integral, 2-8 °C, sigilii intacte; etichete identitate pacient verificate cu cererea spitalului', 36, 'C'),
('300', '1800005399', 'ZPMI', 'UMC-26-005455', '20261006', '090000', '0000700250', 'PP-1A8B4DC35A0E', NULL, NULL, 'A')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.qals (
  mandt      varchar(3) NOT NULL,
  prueflos   varchar(12) NOT NULL,
  werk       varchar(4) NOT NULL,
  art        varchar(8) NOT NULL,
  matnr      varchar(40) NOT NULL,
  charg      varchar(10) NOT NULL,
  lifnr      varchar(10),
  ebeln      varchar(10),
  enstehdat  varchar(8) NOT NULL,
  entstezeit varchar(6) NOT NULL,
  losmenge   numeric(13,3) NOT NULL,
  mengeneinh varchar(3) NOT NULL,
  lmenge01   numeric(13,3),
  ktextlos   varchar(40),
  CONSTRAINT qals_pk PRIMARY KEY (mandt, prueflos)
);
COMMENT ON TABLE sap_s4hana.qals IS 'Inspection lots (type 01 goods receipt inspection); lmenge01 = quantity posted to unrestricted stock.';

INSERT INTO sap_s4hana.qals (mandt, prueflos, werk, art, matnr, charg, lifnr, ebeln, enstehdat, entstezeit, losmenge, mengeneinh, lmenge01, ktextlos) VALUES
('300', '010000031200', 'RO10', '01', 'MP-10010', 'MP26-0061', '0000700110', '4500002611', '20260610', '104000', 5, 'G', 5, 'Recepție 5000041207'),
('300', '010000031203', 'RO10', '01', 'MP-20010', 'MP26-0063', '0000700150', '4500002614', '20260612', '091500', 200, 'KG', 200, 'Recepție 5000041219'),
('300', '010000031206', 'RO10', '01', 'AMB-30010', 'MP26-0064', '0000700170', '4500002617', '20260615', '133000', 60000, 'ST', 60000, 'Recepție 5000041231'),
('300', '010000031209', 'RO10', '01', 'MP-10020', 'MP26-0066', '0000700120', '4500002630', '20260629', '112000', 40, 'KG', 40, 'Recepție 5000041288'),
('300', '010000031212', 'RO10', '01', 'AMB-30030', 'MP26-0067', '0000700180', '4500002633', '20260701', '085000', 32000, 'ST', 32000, 'Recepție 5000041296'),
('300', '010000031215', 'RO10', '01', 'MP-10050', 'MP26-0069', '0000700140', '4500002641', '20260713', '141000', 2, 'G', 2, 'Recepție 5000041342'),
('300', '010000031218', 'RO10', '01', 'MP-10030', 'MP26-0071', '0000700130', '4500002652', '20260727', '100500', 5, 'KG', 5, 'Recepție 5000041388'),
('300', '010000031221', 'RO10', '01', 'AMB-30020', 'MP26-0072', '0000700170', '4500002655', '20260728', '124500', 60000, 'ST', 60000, 'Recepție 5000041395'),
('300', '010000031224', 'RO10', '01', 'MP-10010', 'MP26-0074', '0000700110', '4500002668', '20260810', '113500', 5, 'G', 5, 'Recepție 5000041447'),
('300', '010000031227', 'RO10', '01', 'MP-10040', 'MP26-0075', '0000700130', '4500002674', '20260824', '095500', 1, 'KG', 1, 'Recepție 5000041489'),
('300', '010000031230', 'RO10', '01', 'MP-10050', 'MP26-0077', '0000700240', '4500002683', '20260907', '152000', 2, 'G', 0, 'Recepție 5000041530'),
('300', '010000031233', 'RO10', '01', 'MP-40010', 'MP26-0079', '0000700160', '4500002689', '20260914', '103000', 100, 'L', 100, 'Recepție 5000041562'),
('300', '010000031236', 'RO10', '01', 'MP-10020', 'MP26-0081', '0000700120', '4500002697', '20260921', '110000', 40, 'KG', NULL, 'Recepție 5000041601'),
('300', '010000031239', 'RO10', '01', 'AMB-30050', 'MP26-0082', '0000700260', '4500002699', '20260924', '092000', 3000, 'ST', NULL, 'Recepție 5000041622')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.qave (
  mandt          varchar(3) NOT NULL,
  prueflos       varchar(12) NOT NULL,
  kzart          varchar(1) NOT NULL,
  zaehler        varchar(6) NOT NULL,
  vkatart        varchar(1) NOT NULL,
  vauswahlmg     varchar(8) NOT NULL,
  vcode          varchar(4) NOT NULL,
  vdatum         varchar(8) NOT NULL,
  vezeiterf      varchar(6) NOT NULL,
  vname          varchar(12) NOT NULL,
  zz_lims_result varchar(40),
  CONSTRAINT qave_pk PRIMARY KEY (mandt, prueflos, kzart, zaehler)
);
COMMENT ON TABLE sap_s4hana.qave IS 'Usage decisions (A1 accept, R1 reject) with the LIMS result that supported them.';

INSERT INTO sap_s4hana.qave (mandt, prueflos, kzart, zaehler, vkatart, vauswahlmg, vcode, vdatum, vezeiterf, vname, zz_lims_result) VALUES
('300', '010000031200', 'L', '000001', '3', 'RO10-01', 'A1', '20260619', '142000', 'NOPREA', 'LW-240014'),
('300', '010000031203', 'L', '000001', '3', 'RO10-01', 'A1', '20260616', '111000', 'NOPREA', 'LW-240035'),
('300', '010000031206', 'L', '000001', '3', 'RO10-01', 'A1', '20260617', '100500', 'NOPREA', 'LW-240049'),
('300', '010000031209', 'L', '000001', '3', 'RO10-01', 'A1', '20260709', '154500', 'NOPREA', 'LW-240063'),
('300', '010000031212', 'L', '000001', '3', 'RO10-01', 'A1', '20260703', '093000', 'NOPREA', 'LW-240084'),
('300', '010000031215', 'L', '000001', '3', 'RO10-01', 'A1', '20260723', '160000', 'NOPREA', 'LW-240098'),
('300', '010000031218', 'L', '000001', '3', 'RO10-01', 'A1', '20260805', '123000', 'NOPREA', 'LW-240126'),
('300', '010000031221', 'L', '000001', '3', 'RO10-01', 'A1', '20260730', '084000', 'NOPREA', 'LW-240147'),
('300', '010000031224', 'L', '000001', '3', 'RO10-01', 'A1', '20260820', '131500', 'NOPREA', 'LW-240161'),
('300', '010000031227', 'L', '000001', '3', 'RO10-01', 'A1', '20260902', '102000', 'NOPREA', 'LW-240189'),
('300', '010000031230', 'L', '000001', '3', 'RO10-01', 'R1', '20260912', '121000', 'NOPREA', 'LW-240217'),
('300', '010000031233', 'L', '000001', '3', 'RO10-01', 'A1', '20260918', '094500', 'NOPREA', 'LW-240238')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.mch1 (
  mandt varchar(3) NOT NULL,
  matnr varchar(40) NOT NULL,
  charg varchar(10) NOT NULL,
  vfdat varchar(8),
  hsdat varchar(8),
  licha varchar(15),
  lifnr varchar(10),
  zustd varchar(1),
  CONSTRAINT mch1_pk PRIMARY KEY (mandt, matnr, charg)
);
COMMENT ON TABLE sap_s4hana.mch1 IS 'Batch master (expiry, manufacture date, vendor batch, restricted flag).';

INSERT INTO sap_s4hana.mch1 (mandt, matnr, charg, vfdat, hsdat, licha, lifnr, zustd) VALUES
('300', 'MP-10010', 'MP26-0061', '20280331', '20260327', 'HPPL-OXY-2604-1', '0000700110', NULL),
('300', 'MP-20010', 'MP26-0063', '20290531', '20260329', 'CC-NACL-26-1187', '0000700150', NULL),
('300', 'AMB-30010', 'MP26-0064', '20310531', '20260401', 'SG-A1-2605-3391', '0000700170', NULL),
('300', 'MP-10020', 'MP26-0066', '20290131', '20260415', 'ACSD-CTX-6621', '0000700120', NULL),
('300', 'AMB-30030', 'MP26-0067', '20310630', '20260417', 'GXB-V15-26-0777', '0000700180', NULL),
('300', 'MP-10050', 'MP26-0069', '20280630', '20260429', 'BAC-OCT-4012877', '0000700140', NULL),
('300', 'MP-10030', 'MP26-0071', '20290531', '20260513', 'IPCA-MCP-260608', '0000700130', NULL),
('300', 'AMB-30020', 'MP26-0072', '20310630', '20260514', 'SG-A2-2607-0412', '0000700170', NULL),
('300', 'MP-10010', 'MP26-0074', '20280630', '20260527', 'HPPL-OXY-2607-0', '0000700110', NULL),
('300', 'MP-10040', 'MP26-0075', '20290630', '20260610', 'IPCA-OND-260711', '0000700130', NULL),
('300', 'MP-10050', 'MP26-0077', '20280731', '20260624', 'BPT-OCT-260811', '0000700240', 'X'),
('300', 'MP-40010', 'MP26-0079', '20280831', '20260701', 'MRK-NS-26H1904', '0000700160', NULL),
('300', 'MP-10020', 'MP26-0081', '20290831', '20260708', 'ACSD-CTX-6694', '0000700120', 'X'),
('300', 'AMB-30050', 'MP26-0082', '20290831', '20260711', 'RPK-PD5-2609-15', '0000700260', 'X')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.lfa1 (
  mandt         varchar(3) NOT NULL,
  lifnr         varchar(10) NOT NULL,
  name1         varchar(35) NOT NULL,
  name2         varchar(35),
  land1         varchar(3) NOT NULL,
  ktokk         varchar(4) NOT NULL,
  erdat         varchar(8) NOT NULL,
  sperr         varchar(1),
  loevm         varchar(1),
  zzqual_status varchar(1),
  zzqual_date   varchar(8),
  zzwaers       varchar(5),
  CONSTRAINT lfa1_pk PRIMARY KEY (mandt, lifnr)
);
COMMENT ON TABLE sap_s4hana.lfa1 IS 'Vendor master (ktokk ZRAW materials, ZPKG packaging, ZSRV services; sperr = posting block; zzqual_status = EKG GMP supplier qualification A approved / N not approved; zzwaers = order currency).';

INSERT INTO sap_s4hana.lfa1 (mandt, lifnr, name1, name2, land1, ktokk, erdat, sperr, loevm, zzqual_status, zzqual_date, zzwaers) VALUES
('300', '0000700110', 'Hemmo Pharmaceuticals Pvt. Ltd.', NULL, 'IN', 'ZRAW', '20190311', NULL, NULL, 'A', '20190311', 'EUR'),
('300', '0000700120', 'ACS Dobfar S.p.A.', NULL, 'IT', 'ZRAW', '20170620', NULL, NULL, 'A', '20170620', 'EUR'),
('300', '0000700130', 'Ipca Laboratories Ltd.', NULL, 'IN', 'ZRAW', '20180205', NULL, NULL, 'A', '20180205', 'EUR'),
('300', '0000700140', 'Bachem AG', NULL, 'CH', 'ZRAW', '20180917', NULL, NULL, 'A', '20180917', 'EUR'),
('300', '0000700150', 'Chemical Company S.A.', NULL, 'RO', 'ZRAW', '20160411', NULL, NULL, 'A', '20160411', 'RON'),
('300', '0000700160', 'Merck Romania S.R.L.', NULL, 'RO', 'ZRAW', '20170123', NULL, NULL, 'A', '20170123', 'RON'),
('300', '0000700170', 'Stevanato Group S.p.A.', NULL, 'IT', 'ZPKG', '20161107', NULL, NULL, 'A', '20161107', 'EUR'),
('300', '0000700180', 'Gerresheimer Boleslawiec S.A.', NULL, 'PL', 'ZPKG', '20190527', NULL, NULL, 'A', '20190527', 'EUR'),
('300', '0000700190', 'Cartonaj Ilfov S.R.L.', NULL, 'RO', 'ZPKG', '20180813', NULL, NULL, 'A', '20180813', 'RON'),
('300', '0000700200', 'Metrocal Service S.R.L.', NULL, 'RO', 'ZSRV', '20191001', NULL, NULL, 'A', '20191001', 'RON'),
('300', '0000700210', 'Frigotehnica Pantelimon S.R.L.', NULL, 'RO', 'ZSRV', '20210315', NULL, NULL, 'A', '20210315', 'RON'),
('300', '0000700220', 'Carpatica Logistic Frig S.R.L.', NULL, 'RO', 'ZSRV', '20200608', NULL, NULL, 'A', '20200608', 'RON'),
('300', '0000700230', 'Linde Gaz România S.R.L.', NULL, 'RO', 'ZRAW', '20160411', NULL, NULL, 'A', '20160411', 'RON'),
('300', '0000700250', 'Urgent Medical Curier S.R.L.', NULL, 'RO', 'ZSRV', '20220502', NULL, NULL, 'A', '20220502', 'RON'),
('300', '0000700260', 'Rompak Medical S.R.L.', NULL, 'RO', 'ZPKG', '20241118', NULL, NULL, 'A', '20241118', 'RON'),
('300', '0000700240', 'Balkan Pharma Trading Ltd.', NULL, 'BG', 'ZRAW', '20260828', 'X', NULL, 'N', NULL, 'EUR')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.lfbk (
  mandt varchar(3) NOT NULL,
  lifnr varchar(10) NOT NULL,
  banks varchar(3) NOT NULL,
  bankl varchar(15) NOT NULL,
  bankn varchar(35) NOT NULL,
  iban  varchar(34),
  koinh varchar(60),
  bvtyp varchar(4),
  CONSTRAINT lfbk_pk PRIMARY KEY (mandt, lifnr, banks, bankl, bankn)
);
COMMENT ON TABLE sap_s4hana.lfbk IS 'Vendor bank details (current).';

INSERT INTO sap_s4hana.lfbk (mandt, lifnr, banks, bankl, bankn, iban, koinh, bvtyp) VALUES
('300', '0000700110', 'IN', 'HDFC0000060', '50200033871190', NULL, 'Hemmo Pharmaceuticals Pvt. Ltd.', '0001'),
('300', '0000700120', 'IT', 'X05428', '11101000000418822', 'IT33X0542811101000000418822', 'ACS Dobfar S.p.A.', '0001'),
('300', '0000700130', 'IN', 'SBIN0000300', '30118876542', NULL, 'Ipca Laboratories Ltd.', '0001'),
('300', '0000700140', 'CH', '00235', '023511447761', 'CH1700235023511447761', 'Bachem AG', '0001'),
('300', '0000700150', 'RO', 'BTRL', '2240441182100XX1', 'RO60BTRL2240441182100XX1', 'Chemical Company S.A.', '0001'),
('300', '0000700160', 'RO', 'INGB', '0001008210347921', 'RO08INGB0001008210347921', 'Merck Romania S.R.L.', '0001'),
('300', '0000700170', 'IT', 'M03069', '62590100000011237', 'IT39M0306962590100000011237', 'Stevanato Group S.p.A.', '0001'),
('300', '0000700180', 'PL', '1240', '62921111001077123411', 'PL06124062921111001077123411', 'Gerresheimer Boleslawiec S.A.', '0001'),
('300', '0000700190', 'RO', 'BRDE', '445SV31882104450', 'RO49BRDE445SV31882104450', 'Cartonaj Ilfov S.R.L.', '0001'),
('300', '0000700200', 'RO', 'RNCB', '0082004411370001', 'RO48RNCB0082004411370001', 'Metrocal Service S.R.L.', '0001'),
('300', '0000700210', 'RO', 'BACX', '0000002290447100', 'RO30BACX0000002290447100', 'Frigotehnica Pantelimon S.R.L.', '0001'),
('300', '0000700220', 'RO', 'RZBR', '0000060019823344', 'RO36RZBR0000060019823344', 'Carpatica Logistic Frig S.R.L.', '0001'),
('300', '0000700230', 'RO', 'CITI', '0000000723004118', 'RO50CITI0000000723004118', 'Linde Gaz România S.R.L.', '0001'),
('300', '0000700250', 'RO', 'BTRL', '0417012201055XX2', 'RO28BTRL0417012201055XX2', 'Urgent Medical Curier S.R.L.', '0001'),
('300', '0000700260', 'RO', 'INGB', '0001008290013355', 'RO45INGB0001008290013355', 'Rompak Medical S.R.L.', '0001'),
('300', '0000700240', 'BG', 'UNCR', '70001522994180', 'BG42UNCR70001522994180', 'Balkan Pharma Trading Ltd.', '0001')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.bnka (
  banks varchar(3) NOT NULL,
  bankl varchar(15) NOT NULL,
  banka varchar(60) NOT NULL,
  CONSTRAINT bnka_pk PRIMARY KEY (banks, bankl)
);
COMMENT ON TABLE sap_s4hana.bnka IS 'Bank master.';

INSERT INTO sap_s4hana.bnka (banks, bankl, banka) VALUES
('IN', 'HDFC0000060', 'HDFC Bank Ltd, Mumbai'),
('IT', 'X05428', 'Banco BPM S.p.A., Milano'),
('IN', 'SBIN0000300', 'State Bank of India, Mumbai'),
('CH', '00235', 'UBS Switzerland AG, Basel'),
('RO', 'BTRL', 'Banca Transilvania S.A.'),
('RO', 'INGB', 'ING Bank N.V. Amsterdam - Sucursala București'),
('IT', 'M03069', 'Intesa Sanpaolo S.p.A., Padova'),
('PL', '1240', 'Bank Pekao S.A., Bolesławiec'),
('RO', 'BRDE', 'BRD - Groupe Société Générale S.A.'),
('RO', 'RNCB', 'Banca Comercială Română, București'),
('RO', 'BACX', 'UniCredit Bank S.A., București'),
('RO', 'RZBR', 'Raiffeisen Bank S.A., Brașov'),
('RO', 'CITI', 'Citibank Europe plc, Dublin - Sucursala România'),
('BG', 'UNCR', 'UniCredit Bulbank AD, Sofia')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.cdhdr (
  objectclas varchar(15) NOT NULL,
  objectid   varchar(90) NOT NULL,
  changenr   varchar(10) NOT NULL,
  username   varchar(12) NOT NULL,
  udate      varchar(8) NOT NULL,
  utime      varchar(6) NOT NULL,
  tcode      varchar(20),
  change_ind varchar(1) NOT NULL,
  CONSTRAINT cdhdr_pk PRIMARY KEY (objectclas, objectid, changenr)
);
COMMENT ON TABLE sap_s4hana.cdhdr IS 'Change document headers for vendor master (KRED) creation and changes; the 2026-09-22 change of vendor 700210 replaced its bank account.';

INSERT INTO sap_s4hana.cdhdr (objectclas, objectid, changenr, username, udate, utime, tcode, change_ind) VALUES
('KRED', '0000700110', '0007201100', 'ONISTOR', '20190311', '101500', 'XK01', 'I'),
('KRED', '0000700120', '0007201200', 'ONISTOR', '20170620', '101500', 'XK01', 'I'),
('KRED', '0000700130', '0007201300', 'ONISTOR', '20180205', '101500', 'XK01', 'I'),
('KRED', '0000700140', '0007201400', 'ONISTOR', '20180917', '101500', 'XK01', 'I'),
('KRED', '0000700150', '0007201500', 'ONISTOR', '20160411', '101500', 'XK01', 'I'),
('KRED', '0000700160', '0007201600', 'ONISTOR', '20170123', '101500', 'XK01', 'I'),
('KRED', '0000700170', '0007201700', 'ONISTOR', '20161107', '101500', 'XK01', 'I'),
('KRED', '0000700180', '0007201800', 'ONISTOR', '20190527', '101500', 'XK01', 'I'),
('KRED', '0000700190', '0007201900', 'ONISTOR', '20180813', '101500', 'XK01', 'I'),
('KRED', '0000700200', '0007202000', 'ONISTOR', '20191001', '101500', 'XK01', 'I'),
('KRED', '0000700210', '0007202100', 'ONISTOR', '20210315', '101500', 'XK01', 'I'),
('KRED', '0000700210', '0007202101', 'ONISTOR', '20260922', '143100', 'XK02', 'U'),
('KRED', '0000700220', '0007202200', 'ONISTOR', '20200608', '101500', 'XK01', 'I'),
('KRED', '0000700230', '0007202300', 'ONISTOR', '20160411', '101500', 'XK01', 'I'),
('KRED', '0000700250', '0007202500', 'ONISTOR', '20220502', '101500', 'XK01', 'I'),
('KRED', '0000700260', '0007202600', 'ONISTOR', '20241118', '101500', 'XK01', 'I'),
('KRED', '0000700240', '0007202400', 'ONISTOR', '20260828', '101500', 'XK01', 'I')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_bank_verif (
  mandt        varchar(3) NOT NULL,
  lifnr        varchar(10) NOT NULL,
  changenr     varchar(10) NOT NULL,
  verif_date   varchar(8) NOT NULL,
  verif_user   varchar(12) NOT NULL,
  verif_method varchar(10) NOT NULL,
  CONSTRAINT zekg_bank_verif_pk PRIMARY KEY (mandt, lifnr, changenr)
);
COMMENT ON TABLE sap_s4hana.zekg_bank_verif IS 'EKG custom table: verification of vendor bank details after each change (CALLBACK to a known contact, or EMAIL).';

INSERT INTO sap_s4hana.zekg_bank_verif (mandt, lifnr, changenr, verif_date, verif_user, verif_method) VALUES
('300', '0000700110', '0007201100', '20190311', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700120', '0007201200', '20170620', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700130', '0007201300', '20180205', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700140', '0007201400', '20180917', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700150', '0007201500', '20160411', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700160', '0007201600', '20170123', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700170', '0007201700', '20161107', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700180', '0007201800', '20190527', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700190', '0007201900', '20180813', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700200', '0007202000', '20191001', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700210', '0007202101', '20260922', 'ONISTOR', 'EMAIL'),
('300', '0000700220', '0007202200', '20200608', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700230', '0007202300', '20160411', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700250', '0007202500', '20220502', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700260', '0007202600', '20241118', 'MAPOSTOL', 'CALLBACK'),
('300', '0000700240', '0007202400', '20260828', 'MAPOSTOL', 'CALLBACK')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_vend_scrn (
  mandt       varchar(3) NOT NULL,
  lifnr       varchar(10) NOT NULL,
  screen_id   varchar(20) NOT NULL,
  screen_date varchar(8) NOT NULL,
  result      varchar(1) NOT NULL,
  risk_rating varchar(10) NOT NULL,
  anomaly_ref varchar(20),
  CONSTRAINT zekg_vend_scrn_pk PRIMARY KEY (mandt, lifnr, screen_id)
);
COMMENT ON TABLE sap_s4hana.zekg_vend_scrn IS 'EKG custom table: sanctions/adverse media screening of vendors (result C clear, R match under review, B blocked) and risk rating.';

INSERT INTO sap_s4hana.zekg_vend_scrn (mandt, lifnr, screen_id, screen_date, result, risk_rating, anomaly_ref) VALUES
('300', '0000700110', 'SCR-26-0110', '20260901', 'C', 'MEDIUM', NULL),
('300', '0000700120', 'SCR-26-0120', '20260901', 'C', 'LOW', NULL),
('300', '0000700130', 'SCR-26-0130', '20260901', 'C', 'MEDIUM', NULL),
('300', '0000700140', 'SCR-26-0140', '20260901', 'C', 'LOW', NULL),
('300', '0000700150', 'SCR-26-0150', '20260901', 'C', 'LOW', NULL),
('300', '0000700160', 'SCR-26-0160', '20260901', 'C', 'LOW', NULL),
('300', '0000700170', 'SCR-26-0170', '20260901', 'C', 'LOW', NULL),
('300', '0000700180', 'SCR-26-0180', '20260901', 'C', 'LOW', NULL),
('300', '0000700190', 'SCR-26-0190', '20260901', 'C', 'MEDIUM', NULL),
('300', '0000700200', 'SCR-26-0200', '20260901', 'C', 'LOW', NULL),
('300', '0000700210', 'SCR-26-0210', '20260923', 'R', 'HIGH', 'ANOM-26-0007'),
('300', '0000700220', 'SCR-26-0220', '20260901', 'C', 'LOW', NULL),
('300', '0000700230', 'SCR-26-0230', '20260901', 'C', 'LOW', NULL),
('300', '0000700250', 'SCR-26-0250', '20260901', 'C', 'LOW', NULL),
('300', '0000700260', 'SCR-26-0260', '20260901', 'C', 'LOW', NULL),
('300', '0000700240', 'SCR-26-0240', '20260912', 'B', 'HIGH', 'ANOM-26-0005'),
('300', '0000700240', 'SCR-26-0199', '20260828', 'R', 'MEDIUM', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.rbkp (
  mandt       varchar(3) NOT NULL,
  belnr       varchar(10) NOT NULL,
  gjahr       varchar(4) NOT NULL,
  bukrs       varchar(4) NOT NULL,
  lifnr       varchar(10) NOT NULL,
  xblnr       varchar(16) NOT NULL,
  rmwwr       numeric(15,2) NOT NULL,
  waers       varchar(5) NOT NULL,
  bldat       varchar(8) NOT NULL,
  budat       varchar(8) NOT NULL,
  rbstat      varchar(1) NOT NULL,
  zlspr       varchar(1),
  zz_fi_belnr varchar(10),
  CONSTRAINT rbkp_pk PRIMARY KEY (mandt, belnr, gjahr)
);
COMMENT ON TABLE sap_s4hana.rbkp IS 'Supplier invoice headers (MIRO): rbstat 5 posted, A parked; zlspr payment block R price variance, Q quality; zz_fi_belnr = the FI document of a posted invoice.';

INSERT INTO sap_s4hana.rbkp (mandt, belnr, gjahr, bukrs, lifnr, xblnr, rmwwr, waers, bldat, budat, rbstat, zlspr, zz_fi_belnr) VALUES
('300', '5105600001', '2026', 'RO01', '0000700110', 'HPPL/EXP/26183', 7250.00, 'EUR', '20260612', '20260612', '5', NULL, '5105600001'),
('300', '5105600002', '2026', 'RO01', '0000700150', 'CC-26189', 3509.00, 'RON', '20260614', '20260614', '5', NULL, '5105600002'),
('300', '5105600003', '2026', 'RO01', '0000700170', 'SG-INV-26192', 2460.00, 'EUR', '20260617', '20260617', '5', NULL, '5105600003'),
('300', '5105600004', '2026', 'RO01', '0000700120', 'ACSD-FT-26198', 24400.00, 'EUR', '20260701', '20260701', '5', NULL, '5105600004'),
('300', '5105600005', '2026', 'RO01', '0000700180', 'GXB/F/26201', 3776.00, 'EUR', '20260703', '20260703', '5', NULL, '5105600005'),
('300', '5105600006', '2026', 'RO01', '0000700140', 'BAC-RE-26207', 7800.00, 'EUR', '20260715', '20260715', '5', NULL, '5105600006'),
('300', '5105600007', '2026', 'RO01', '0000700130', 'IPCA/EX/26213', 925.00, 'EUR', '20260729', '20260729', '5', NULL, '5105600007'),
('300', '5105600008', '2026', 'RO01', '0000700170', 'SG-INV-26216', 2940.00, 'EUR', '20260730', '20260730', '5', 'R', '5105600008'),
('300', '5105600009', '2026', 'RO01', '0000700110', 'HPPL/EXP/26222', 7250.00, 'EUR', '20260812', '20260812', '5', NULL, '5105600009'),
('300', '5105600010', '2026', 'RO01', '0000700130', 'IPCA/EX/26225', 2200.00, 'EUR', '20260826', '20260826', '5', NULL, '5105600010'),
('300', '5105600011', '2026', 'RO01', '0000700240', 'BPT-26231', 5300.00, 'EUR', '20260909', '20260909', '5', 'Q', '5105600011'),
('300', '5105600012', '2026', 'RO01', '0000700160', 'MRK-RO-26237', 1185.80, 'RON', '20260916', '20260916', '5', NULL, '5105600012'),
('300', '5105600013', '2026', 'RO01', '0000700120', 'ACSD-FT-26243', 24400.00, 'EUR', '20260923', '20260923', 'A', NULL, NULL),
('300', '5105600014', '2026', 'RO01', '0000700200', 'MTC-2026-0741', 8228.00, 'RON', '20260715', '20260715', '5', NULL, '5105600013'),
('300', '5105600015', '2026', 'RO01', '0000700220', 'CLF-26-10412', 11313.50, 'RON', '20260731', '20260731', '5', NULL, '5105600014'),
('300', '5105600016', '2026', 'RO01', '0000700250', 'UMC-F-26-2217', 3460.60, 'RON', '20260810', '20260810', '5', NULL, '5105600015'),
('300', '5105600017', '2026', 'RO01', '0000700210', 'FTP-2026-118', 17182.00, 'RON', '20260814', '20260814', '5', NULL, '5105600016'),
('300', '5105600018', '2026', 'RO01', '0000700230', 'LGR-26-771904', 3805.45, 'RON', '20260831', '20260831', '5', NULL, '5105600017'),
('300', '5105600019', '2026', 'RO01', '0000700220', 'CLF-26-11873', 14302.20, 'RON', '20260831', '20260831', '5', NULL, '5105600018'),
('300', '5105600020', '2026', 'RO01', '0000700210', 'FTP-2026-131', 59169.00, 'RON', '20260919', '20260919', '5', NULL, '5105600019')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.rseg (
  mandt varchar(3) NOT NULL,
  belnr varchar(10) NOT NULL,
  gjahr varchar(4) NOT NULL,
  buzei varchar(6) NOT NULL,
  ebeln varchar(10) NOT NULL,
  ebelp varchar(5) NOT NULL,
  lfbnr varchar(10),
  lfgja varchar(4),
  wrbtr numeric(15,2) NOT NULL,
  matnr varchar(40),
  CONSTRAINT rseg_pk PRIMARY KEY (mandt, belnr, gjahr, buzei)
);
COMMENT ON TABLE sap_s4hana.rseg IS 'Invoice items: purchase order item and the goods receipt material document matched (lfbnr).';

INSERT INTO sap_s4hana.rseg (mandt, belnr, gjahr, buzei, ebeln, ebelp, lfbnr, lfgja, wrbtr, matnr) VALUES
('300', '5105600001', '2026', '000001', '4500002611', '00010', '5000041207', '2026', 7250.00, 'MP-10010'),
('300', '5105600002', '2026', '000001', '4500002614', '00010', '5000041219', '2026', 2900.00, 'MP-20010'),
('300', '5105600003', '2026', '000001', '4500002617', '00010', '5000041231', '2026', 2460.00, 'AMB-30010'),
('300', '5105600004', '2026', '000001', '4500002630', '00010', '5000041288', '2026', 24400.00, 'MP-10020'),
('300', '5105600005', '2026', '000001', '4500002633', '00010', '5000041296', '2026', 3776.00, 'AMB-30030'),
('300', '5105600006', '2026', '000001', '4500002641', '00010', '5000041342', '2026', 7800.00, 'MP-10050'),
('300', '5105600007', '2026', '000001', '4500002652', '00010', '5000041388', '2026', 925.00, 'MP-10030'),
('300', '5105600008', '2026', '000001', '4500002655', '00010', '5000041395', '2026', 2940.00, 'AMB-30020'),
('300', '5105600009', '2026', '000001', '4500002668', '00010', '5000041447', '2026', 7250.00, 'MP-10010'),
('300', '5105600010', '2026', '000001', '4500002674', '00010', '5000041489', '2026', 2200.00, 'MP-10040'),
('300', '5105600011', '2026', '000001', '4500002683', '00010', '5000041530', '2026', 5300.00, 'MP-10050'),
('300', '5105600012', '2026', '000001', '4500002689', '00010', '5000041562', '2026', 980.00, 'MP-40010'),
('300', '5105600013', '2026', '000001', '4500002697', '00010', '5000041601', '2026', 24400.00, 'MP-10020'),
('300', '5105600014', '2026', '000001', '4500002646', '00010', NULL, NULL, 6800.00, NULL),
('300', '5105600015', '2026', '000001', '4500002601', '00010', NULL, NULL, 9350.00, NULL),
('300', '5105600016', '2026', '000001', '4500002602', '00010', NULL, NULL, 2860.00, NULL),
('300', '5105600017', '2026', '000001', '4500002660', '00010', NULL, NULL, 14200.00, NULL),
('300', '5105600018', '2026', '000001', '4500002603', '00010', NULL, NULL, 3145.00, NULL),
('300', '5105600019', '2026', '000001', '4500002601', '00010', NULL, NULL, 11820.00, NULL),
('300', '5105600020', '2026', '000001', '4500002692', '00010', NULL, NULL, 48900.00, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.reguh (
  mandt         varchar(3) NOT NULL,
  laufd         varchar(8) NOT NULL,
  laufi         varchar(6) NOT NULL,
  xvorl         varchar(1) NOT NULL,
  zbukr         varchar(4) NOT NULL,
  lifnr         varchar(10) NOT NULL,
  vblnr         varchar(10) NOT NULL,
  waers         varchar(5) NOT NULL,
  rbetr         numeric(23,2) NOT NULL,
  zbnks         varchar(3),
  zbnky         varchar(15),
  zbnkn         varchar(35),
  ziban         varchar(34),
  ubhkt         varchar(10),
  zaldt         varchar(8) NOT NULL,
  zz_spl_status varchar(1) NOT NULL,
  CONSTRAINT reguh_pk PRIMARY KEY (mandt, laufd, laufi, xvorl, zbukr, lifnr, vblnr)
);
COMMENT ON TABLE sap_s4hana.reguh IS 'Payment run settlement data per payee (payee bank as used; zz_spl_status = vendor screening result read on the proposal).';

INSERT INTO sap_s4hana.reguh (mandt, laufd, laufi, xvorl, zbukr, lifnr, vblnr, waers, rbetr, zbnks, zbnky, zbnkn, ziban, ubhkt, zaldt, zz_spl_status) VALUES
('300', '20260724', 'EKG01', '', 'RO01', '0000700150', '2000000002', 'RON', -3509.00, 'RO', 'BTRL', '2240441182100XX1', 'RO60BTRL2240441182100XX1', '0000512100', '20260724', 'C'),
('300', '20260807', 'EKG02', '', 'RO01', '0000700110', '2000000001', 'EUR', -7250.00, 'IN', 'HDFC0000060', '50200033871190', NULL, '0000512400', '20260807', 'C'),
('300', '20260807', 'EKG03', '', 'RO01', '0000700170', '2000000003', 'EUR', -2460.00, 'IT', 'M03069', '62590100000011237', 'IT39M0306962590100000011237', '0000512400', '20260807', 'C'),
('300', '20260821', 'EKG04', '', 'RO01', '0000700120', '2000000004', 'EUR', -24400.00, 'IT', 'X05428', '11101000000418822', 'IT33X0542811101000000418822', '0000512400', '20260821', 'C'),
('300', '20260821', 'EKG05', '', 'RO01', '0000700180', '2000000005', 'EUR', -3776.00, 'PL', '1240', '62921111001077123411', 'PL06124062921111001077123411', '0000512400', '20260821', 'C'),
('300', '20260821', 'EKG05', '', 'RO01', '0000700200', '2000000008', 'RON', -8228.00, 'RO', 'RNCB', '0082004411370001', 'RO48RNCB0082004411370001', '0000512100', '20260821', 'C'),
('300', '20260904', 'EKG06', '', 'RO01', '0000700140', '2000000006', 'EUR', -7800.00, 'CH', '00235', '023511447761', 'CH1700235023511447761', '0000512400', '20260904', 'C'),
('300', '20260904', 'EKG07', '', 'RO01', '0000700220', '2000000009', 'RON', -11313.50, 'RO', 'RZBR', '0000060019823344', 'RO36RZBR0000060019823344', '0000512100', '20260904', 'C'),
('300', '20260918', 'EKG08', '', 'RO01', '0000700130', '2000000007', 'EUR', -925.00, 'IN', 'SBIN0000300', '30118876542', NULL, '0000512400', '20260918', 'C'),
('300', '20260918', 'EKG08', '', 'RO01', '0000700250', '2000000010', 'RON', -3460.60, 'RO', 'BTRL', '0417012201055XX2', 'RO28BTRL0417012201055XX2', '0000512100', '20260918', 'C'),
('300', '20260918', 'EKG08', '', 'RO01', '0000700210', '2000000011', 'RON', -17182.00, 'RO', 'BRDE', '445SV29004471200', 'RO93BRDE445SV29004471200', '0000512100', '20260918', 'C'),
('300', '20260925', 'EKG09', '', 'RO01', '0000700210', '2000000012', 'RON', -59169.00, 'RO', 'BACX', '0000002290447100', 'RO30BACX0000002290447100', '0000512100', '20260925', 'R')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.regup (
  mandt varchar(3) NOT NULL,
  laufd varchar(8) NOT NULL,
  laufi varchar(6) NOT NULL,
  xvorl varchar(1) NOT NULL,
  zbukr varchar(4) NOT NULL,
  lifnr varchar(10) NOT NULL,
  vblnr varchar(10) NOT NULL,
  bukrs varchar(4) NOT NULL,
  belnr varchar(10) NOT NULL,
  gjahr varchar(4) NOT NULL,
  buzei varchar(3) NOT NULL,
  xblnr varchar(16),
  dmbtr numeric(23,2) NOT NULL,
  CONSTRAINT regup_pk PRIMARY KEY (mandt, laufd, laufi, xvorl, zbukr, lifnr, vblnr, bukrs, belnr, gjahr, buzei)
);
COMMENT ON TABLE sap_s4hana.regup IS 'Items paid by each payment document (belnr = invoice FI document, xblnr = supplier invoice number, amount in payment currency).';

INSERT INTO sap_s4hana.regup (mandt, laufd, laufi, xvorl, zbukr, lifnr, vblnr, bukrs, belnr, gjahr, buzei, xblnr, dmbtr) VALUES
('300', '20260724', 'EKG01', '', 'RO01', '0000700150', '2000000002', 'RO01', '5105600002', '2026', '001', 'CC-26189', 3509.00),
('300', '20260807', 'EKG02', '', 'RO01', '0000700110', '2000000001', 'RO01', '5105600001', '2026', '001', 'HPPL/EXP/26183', 7250.00),
('300', '20260807', 'EKG03', '', 'RO01', '0000700170', '2000000003', 'RO01', '5105600003', '2026', '001', 'SG-INV-26192', 2460.00),
('300', '20260821', 'EKG04', '', 'RO01', '0000700120', '2000000004', 'RO01', '5105600004', '2026', '001', 'ACSD-FT-26198', 24400.00),
('300', '20260821', 'EKG05', '', 'RO01', '0000700180', '2000000005', 'RO01', '5105600005', '2026', '001', 'GXB/F/26201', 3776.00),
('300', '20260821', 'EKG05', '', 'RO01', '0000700200', '2000000008', 'RO01', '5105600013', '2026', '001', 'MTC-2026-0741', 8228.00),
('300', '20260904', 'EKG06', '', 'RO01', '0000700140', '2000000006', 'RO01', '5105600006', '2026', '001', 'BAC-RE-26207', 7800.00),
('300', '20260904', 'EKG07', '', 'RO01', '0000700220', '2000000009', 'RO01', '5105600014', '2026', '001', 'CLF-26-10412', 11313.50),
('300', '20260918', 'EKG08', '', 'RO01', '0000700130', '2000000007', 'RO01', '5105600007', '2026', '001', 'IPCA/EX/26213', 925.00),
('300', '20260918', 'EKG08', '', 'RO01', '0000700250', '2000000010', 'RO01', '5105600015', '2026', '001', 'UMC-F-26-2217', 3460.60),
('300', '20260918', 'EKG08', '', 'RO01', '0000700210', '2000000011', 'RO01', '5105600016', '2026', '001', 'FTP-2026-118', 17182.00),
('300', '20260925', 'EKG09', '', 'RO01', '0000700210', '2000000012', 'RO01', '5105600019', '2026', '001', 'FTP-2026-131', 59169.00)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.bnk_batch_header (
  mandt    varchar(3) NOT NULL,
  batch_no varchar(10) NOT NULL,
  laufd    varchar(8) NOT NULL,
  laufi    varchar(6) NOT NULL,
  zbukr    varchar(4) NOT NULL,
  status   varchar(5) NOT NULL,
  chusr    varchar(12) NOT NULL,
  chdate   varchar(8) NOT NULL,
  chtime   varchar(6) NOT NULL,
  CONSTRAINT bnk_batch_header_pk PRIMARY KEY (mandt, batch_no)
);
COMMENT ON TABLE sap_s4hana.bnk_batch_header IS 'Bank Communication Management payment batches (IBC11 = approved and sent to the bank) with the releasing user.';

INSERT INTO sap_s4hana.bnk_batch_header (mandt, batch_no, laufd, laufi, zbukr, status, chusr, chdate, chtime) VALUES
('300', 'B2600001', '20260724', 'EKG01', 'RO01', 'IBC11', 'MAPOSTOL', '20260724', '054700'),
('300', 'B2600002', '20260807', 'EKG02', 'RO01', 'IBC11', 'GRADU', '20260807', '055400'),
('300', 'B2600003', '20260807', 'EKG03', 'RO01', 'IBC11', 'MAPOSTOL', '20260807', '060100'),
('300', 'B2600004', '20260821', 'EKG04', 'RO01', 'IBC11', 'GRADU', '20260821', '060800'),
('300', 'B2600005', '20260821', 'EKG05', 'RO01', 'IBC11', 'MAPOSTOL', '20260821', '061500'),
('300', 'B2600006', '20260904', 'EKG06', 'RO01', 'IBC11', 'GRADU', '20260904', '062200'),
('300', 'B2600007', '20260904', 'EKG07', 'RO01', 'IBC11', 'MAPOSTOL', '20260904', '062900'),
('300', 'B2600008', '20260918', 'EKG08', 'RO01', 'IBC11', 'MAPOSTOL', '20260918', '063600'),
('300', 'B2600009', '20260925', 'EKG09', 'RO01', 'IBC11', 'GRADU', '20260925', '064300')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.vbak (
  mandt varchar(3) NOT NULL,
  vbeln varchar(10) NOT NULL,
  auart varchar(4) NOT NULL,
  erdat varchar(8) NOT NULL,
  kunnr varchar(10) NOT NULL,
  bstnk varchar(35),
  waerk varchar(5) NOT NULL,
  CONSTRAINT vbak_pk PRIMARY KEY (mandt, vbeln)
);
COMMENT ON TABLE sap_s4hana.vbak IS 'Sales orders (ZNP named-patient serum order from Veeva CRM; ZOR standard order).';

INSERT INTO sap_s4hana.vbak (mandt, vbeln, auart, erdat, kunnr, bstnk, waerk) VALUES
('300', '120031', 'ZNP', '20260706', '0000800110', 'SA26-0031', 'RON'),
('300', '120034', 'ZNP', '20260727', '0000800110', 'SA26-0034', 'RON'),
('300', '120037', 'ZNP', '20260814', '0000800120', 'SA26-0037', 'RON'),
('300', '120040', 'ZNP', '20260904', '0000800130', 'SA26-0040', 'RON'),
('300', '110396', 'ZOR', '20260727', '0000800010', NULL, 'RON'),
('300', '110407', 'ZOR', '20260813', '0000800220', NULL, 'EUR'),
('300', '110409', 'ZOR', '20260824', '0000800020', NULL, 'RON'),
('300', '110418', 'ZOR', '20260916', '0000800220', NULL, 'EUR'),
('300', '120042', 'ZNP', '20260918', '0000800110', 'SA26-0042', 'RON'),
('300', '120044', 'ZNP', '20260921', '0000800120', 'SA26-0044', 'RON'),
('300', '120045', 'ZNP', '20260928', '0000800110', 'SA26-0045', 'RON')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.vbrk (
  mandt varchar(3) NOT NULL,
  vbeln varchar(10) NOT NULL,
  fkart varchar(4) NOT NULL,
  fkdat varchar(8) NOT NULL,
  kunrg varchar(10) NOT NULL,
  xblnr varchar(16),
  netwr numeric(15,2) NOT NULL,
  waerk varchar(5) NOT NULL,
  bukrs varchar(4) NOT NULL,
  mwsbk numeric(15,2) NOT NULL,
  CONSTRAINT vbrk_pk PRIMARY KEY (mandt, vbeln)
);
COMMENT ON TABLE sap_s4hana.vbrk IS 'Billing document headers (ZNPF named-patient invoice, F2 standard); xblnr = legal (e-Factura) invoice number; mwsbk = VAT.';

INSERT INTO sap_s4hana.vbrk (mandt, vbeln, fkart, fkdat, kunrg, xblnr, netwr, waerk, bukrs, mwsbk) VALUES
('300', '90004113', 'ZNPF', '20260720', '0000800110', 'EKG26-000531', 2450.00, 'RON', 'RO01', 269.50),
('300', '90004126', 'ZNPF', '20260810', '0000800110', 'EKG26-000534', 2450.00, 'RON', 'RO01', 269.50),
('300', '90004139', 'ZNPF', '20260831', '0000800120', 'EKG26-000537', 2450.00, 'RON', 'RO01', 269.50),
('300', '90004152', 'ZNPF', '20260921', '0000800130', 'EKG26-000540', 2450.00, 'RON', 'RO01', 269.50),
('300', '90004165', 'F2', '20260727', '0000800010', 'EKG26-000596', 19200.00, 'RON', 'RO01', 2112.00),
('300', '90004178', 'F2', '20260813', '0000800220', 'EKG26-000607', 3720.00, 'EUR', 'RO01', 0.00),
('300', '90004191', 'F2', '20260824', '0000800020', 'EKG26-000609', 34800.00, 'RON', 'RO01', 3828.00),
('300', '90004204', 'F2', '20260916', '0000800220', 'EKG26-000618', 3348.00, 'EUR', 'RO01', 0.00)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.vbrp (
  mandt varchar(3) NOT NULL,
  vbeln varchar(10) NOT NULL,
  posnr varchar(6) NOT NULL,
  matnr varchar(40) NOT NULL,
  fkimg numeric(13,3) NOT NULL,
  netwr numeric(15,2) NOT NULL,
  fbuda varchar(8),
  aubel varchar(10),
  CONSTRAINT vbrp_pk PRIMARY KEY (mandt, vbeln, posnr)
);
COMMENT ON TABLE sap_s4hana.vbrp IS 'Billing items (fbuda = date of delivery to the hospital; aubel = sales order).';

INSERT INTO sap_s4hana.vbrp (mandt, vbeln, posnr, matnr, fkimg, netwr, fbuda, aubel) VALUES
('300', '90004113', '000010', 'PF-9101', 1, 2450.00, '20260717', '120031'),
('300', '90004126', '000010', 'PF-9101', 1, 2450.00, '20260807', '120034'),
('300', '90004139', '000010', 'PF-9101', 1, 2450.00, '20260828', '120037'),
('300', '90004152', '000010', 'PF-9101', 1, 2450.00, '20260918', '120040'),
('300', '90004165', '000010', 'PF-1101', 6000, 19200.00, '20260727', '110396'),
('300', '90004178', '000010', 'PF-1101', 6000, 3720.00, '20260813', '110407'),
('300', '90004191', '000010', 'PF-1105', 2400, 34800.00, '20260824', '110409'),
('300', '90004204', '000010', 'PF-1101', 5400, 3348.00, '20260916', '110418')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.skat (
  mandt varchar(3) NOT NULL,
  spras varchar(1) NOT NULL,
  ktopl varchar(4) NOT NULL,
  saknr varchar(10) NOT NULL,
  txt50 varchar(50) NOT NULL,
  CONSTRAINT skat_pk PRIMARY KEY (mandt, spras, ktopl, saknr)
);
COMMENT ON TABLE sap_s4hana.skat IS 'G/L account texts in Romanian (language key 4, chart of accounts EKRO).';

INSERT INTO sap_s4hana.skat (mandt, spras, ktopl, saknr, txt50) VALUES
('300', '4', 'EKRO', '0000301000', 'Materii prime'),
('300', '4', 'EKRO', '0000381000', 'Ambalaje'),
('300', '4', 'EKRO', '0000345000', 'Produse finite'),
('300', '4', 'EKRO', '0000401000', 'Furnizori'),
('300', '4', 'EKRO', '0000408000', 'Furnizori - facturi nesosite'),
('300', '4', 'EKRO', '0000411100', 'Clienți'),
('300', '4', 'EKRO', '0000418000', 'Clienți - facturi de întocmit'),
('300', '4', 'EKRO', '0000421000', 'Personal - salarii datorate'),
('300', '4', 'EKRO', '0000428200', 'Alte datorii în legătură cu personalul'),
('300', '4', 'EKRO', '0000431000', 'Asigurări sociale (CAS, CASS)'),
('300', '4', 'EKRO', '0000436000', 'Contribuția asiguratorie pentru muncă'),
('300', '4', 'EKRO', '0000442600', 'TVA deductibilă'),
('300', '4', 'EKRO', '0000442700', 'TVA colectată'),
('300', '4', 'EKRO', '0000444000', 'Impozitul pe venituri de natura salariilor'),
('300', '4', 'EKRO', '0000473000', 'Decontări din operații în curs de clarificare'),
('300', '4', 'EKRO', '0000512100', 'Conturi la bănci în lei'),
('300', '4', 'EKRO', '0000512400', 'Conturi la bănci în valută'),
('300', '4', 'EKRO', '0000601000', 'Cheltuieli cu materiile prime'),
('300', '4', 'EKRO', '0000604000', 'Cheltuieli privind materialele nestocate'),
('300', '4', 'EKRO', '0000611000', 'Cheltuieli cu întreținerea și reparațiile'),
('300', '4', 'EKRO', '0000623000', 'Cheltuieli de protocol, reclamă și publicitate'),
('300', '4', 'EKRO', '0000624000', 'Cheltuieli cu transportul de bunuri și personal'),
('300', '4', 'EKRO', '0000625000', 'Cheltuieli cu deplasări, detașări și transferări'),
('300', '4', 'EKRO', '0000628000', 'Alte cheltuieli cu serviciile executate de terți'),
('300', '4', 'EKRO', '0000641000', 'Cheltuieli cu salariile personalului'),
('300', '4', 'EKRO', '0000646000', 'Cheltuieli privind contribuția asiguratorie pentru'),
('300', '4', 'EKRO', '0000665000', 'Cheltuieli din diferențe de curs valutar'),
('300', '4', 'EKRO', '0000681400', 'Cheltuieli privind ajustările pentru deprecierea a'),
('300', '4', 'EKRO', '0000394500', 'Ajustări pentru deprecierea produselor finite'),
('300', '4', 'EKRO', '0000701000', 'Venituri din vânzarea produselor finite'),
('300', '4', 'EKRO', '0000101200', 'Capital subscris vărsat'),
('300', '4', 'EKRO', '0000117000', 'Rezultatul reportat'),
('300', '4', 'EKRO', '0000151800', 'Alte provizioane'),
('300', '4', 'EKRO', '0000711000', 'Venituri aferente costurilor stocurilor de produse'),
('300', '4', 'EKRO', '0000765000', 'Venituri din diferențe de curs valutar')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.edidc (
  mandt  varchar(3) NOT NULL,
  docnum varchar(16) NOT NULL,
  status varchar(2) NOT NULL,
  direct varchar(1) NOT NULL,
  mestyp varchar(30) NOT NULL,
  sndprt varchar(2) NOT NULL,
  sndprn varchar(10) NOT NULL,
  credat varchar(8) NOT NULL,
  cretim varchar(6) NOT NULL,
  upddat varchar(8) NOT NULL,
  updtim varchar(6) NOT NULL,
  CONSTRAINT edidc_pk PRIMARY KEY (mandt, docnum)
);
COMMENT ON TABLE sap_s4hana.edidc IS 'Inbound IDoc control records (status 53 posted, 51 error, 64 ready to post); each is one subledger feed batch.';

INSERT INTO sap_s4hana.edidc (mandt, docnum, status, direct, mestyp, sndprt, sndprn, credat, cretim, upddat, updtim) VALUES
('300', '0000000002261429', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260706', '202000', '20260706', '202200'),
('300', '0000000002261458', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260708', '163000', '20260708', '163200'),
('300', '0000000002261487', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260714', '211000', '20260714', '211200'),
('300', '0000000002261516', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260715', '163000', '20260715', '163200'),
('300', '0000000002261545', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260721', '003000', '20260721', '003200'),
('300', '0000000002261574', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260722', '143000', '20260722', '143200'),
('300', '0000000002261603', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260803', '200500', '20260803', '200700'),
('300', '0000000002261632', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260805', '153000', '20260805', '153200'),
('300', '0000000002261661', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260804', '221000', '20260804', '221200'),
('300', '0000000002261690', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260805', '173000', '20260805', '173200'),
('300', '0000000002261719', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260817', '202000', '20260817', '202200'),
('300', '0000000002261748', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260819', '163000', '20260819', '163200'),
('300', '0000000002261777', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260826', '163000', '20260826', '163200'),
('300', '0000000002261806', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260827', '123000', '20260827', '123200'),
('300', '0000000002261835', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260831', '172600', '20260831', '172800'),
('300', '0000000002261864', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260902', '163000', '20260902', '163200'),
('300', '0000000002261893', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260914', '171400', '20260914', '171600'),
('300', '0000000002261922', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260916', '153000', '20260916', '153200'),
('300', '0000000002261951', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260916', '163000', '20260916', '163200'),
('300', '0000000002261980', '53', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260917', '123000', '20260917', '123200'),
('300', '0000000002262009', '64', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260929', '011000', '20260930', '090000'),
('300', '0000000002262038', '64', '2', 'WMMBXY', 'LS', 'OPCENTERRO', '20260929', '221000', '20260930', '090000'),
('300', '0000000002262067', '53', '2', 'SHPCON', 'LS', 'WMS_EKG', '20260727', '170000', '20260727', '170200'),
('300', '0000000002262096', '53', '2', 'SHPCON', 'LS', 'WMS_EKG', '20260828', '174000', '20260828', '174200'),
('300', '0000000002262125', '53', '2', 'SHPCON', 'LS', 'WMS_EKG', '20260918', '173000', '20260918', '173200'),
('300', '0000000002262154', '53', '2', 'ACC_DOCUMENT', 'LS', 'WORKDAY_RO', '20260807', '203000', '20260807', '203200'),
('300', '0000000002262183', '53', '2', 'ACC_DOCUMENT', 'LS', 'WORKDAY_RO', '20260907', '203000', '20260907', '203200'),
('300', '0000000002262212', '53', '2', 'ACC_DOCUMENT', 'LS', 'CONCUR_EKG', '20260728', '221500', '20260728', '221700'),
('300', '0000000002262241', '53', '2', 'ACC_DOCUMENT', 'LS', 'CONCUR_EKG', '20260828', '221500', '20260828', '221700'),
('300', '0000000002262270', '51', '2', 'ACC_DOCUMENT', 'LS', 'CONCUR_EKG', '20260928', '221500', '20260928', '221600'),
('300', '0000000002262299', '53', '2', 'ACC_DOCUMENT', 'LS', 'MAXIMO_EKG', '20260727', '231000', '20260727', '231200'),
('300', '0000000002262328', '53', '2', 'ACC_DOCUMENT', 'LS', 'MAXIMO_EKG', '20260827', '231000', '20260827', '231200'),
('300', '0000000002262357', '53', '2', 'ACC_DOCUMENT', 'LS', 'MAXIMO_EKG', '20260927', '231000', '20260927', '231200')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.bkpf (
  mandt varchar(3) NOT NULL,
  bukrs varchar(4) NOT NULL,
  belnr varchar(10) NOT NULL,
  gjahr varchar(4) NOT NULL,
  blart varchar(2) NOT NULL,
  bldat varchar(8) NOT NULL,
  budat varchar(8) NOT NULL,
  monat varchar(2) NOT NULL,
  cpudt varchar(8) NOT NULL,
  cputm varchar(6) NOT NULL,
  usnam varchar(12) NOT NULL,
  tcode varchar(20),
  xblnr varchar(16),
  bktxt varchar(60),
  awtyp varchar(5) NOT NULL,
  awkey varchar(20) NOT NULL,
  waers varchar(5) NOT NULL,
  CONSTRAINT bkpf_pk PRIMARY KEY (mandt, bukrs, belnr, gjahr)
);
COMMENT ON TABLE sap_s4hana.bkpf IS 'Accounting document headers (awtyp IDOC: awkey = inbound IDoc; VBRK billing; RMRP invoice; MKPF goods receipt; tcode FBV0 = posted from a parked document).';

INSERT INTO sap_s4hana.bkpf (mandt, bukrs, belnr, gjahr, blart, bldat, budat, monat, cpudt, cputm, usnam, tcode, xblnr, bktxt, awtyp, awkey, waers) VALUES
('300', 'RO01', '5000000001', '2026', 'WE', '20260610', '20260610', '06', '20260610', '110000', 'DILIE', 'MIGO', NULL, 'Recepție MP-10010 lot MP26-0061', 'MKPF', '50000412072026', 'RON'),
('300', 'RO01', '5000000002', '2026', 'WE', '20260612', '20260612', '06', '20260612', '093500', 'DILIE', 'MIGO', NULL, 'Recepție MP-20010 lot MP26-0063', 'MKPF', '50000412192026', 'RON'),
('300', 'RO01', '5000000003', '2026', 'WE', '20260615', '20260615', '06', '20260615', '135000', 'DILIE', 'MIGO', NULL, 'Recepție AMB-30010 lot MP26-0064', 'MKPF', '50000412312026', 'RON'),
('300', 'RO01', '5000000004', '2026', 'WE', '20260629', '20260629', '06', '20260629', '114000', 'DILIE', 'MIGO', NULL, 'Recepție MP-10020 lot MP26-0066', 'MKPF', '50000412882026', 'RON'),
('300', 'RO01', '5000000005', '2026', 'WE', '20260701', '20260701', '07', '20260701', '091000', 'DILIE', 'MIGO', NULL, 'Recepție AMB-30030 lot MP26-0067', 'MKPF', '50000412962026', 'RON'),
('300', 'RO01', '5000000006', '2026', 'WE', '20260713', '20260713', '07', '20260713', '143000', 'DILIE', 'MIGO', NULL, 'Recepție MP-10050 lot MP26-0069', 'MKPF', '50000413422026', 'RON'),
('300', 'RO01', '5000000007', '2026', 'WE', '20260727', '20260727', '07', '20260727', '102500', 'DILIE', 'MIGO', NULL, 'Recepție MP-10030 lot MP26-0071', 'MKPF', '50000413882026', 'RON'),
('300', 'RO01', '5000000008', '2026', 'WE', '20260728', '20260728', '07', '20260728', '130500', 'DILIE', 'MIGO', NULL, 'Recepție AMB-30020 lot MP26-0072', 'MKPF', '50000413952026', 'RON'),
('300', 'RO01', '5000000009', '2026', 'WE', '20260810', '20260810', '08', '20260810', '115500', 'DILIE', 'MIGO', NULL, 'Recepție MP-10010 lot MP26-0074', 'MKPF', '50000414472026', 'RON'),
('300', 'RO01', '5000000010', '2026', 'WE', '20260824', '20260824', '08', '20260824', '101500', 'DILIE', 'MIGO', NULL, 'Recepție MP-10040 lot MP26-0075', 'MKPF', '50000414892026', 'RON'),
('300', 'RO01', '5000000011', '2026', 'WE', '20260907', '20260907', '09', '20260907', '154000', 'DILIE', 'MIGO', NULL, 'Recepție MP-10050 lot MP26-0077', 'MKPF', '50000415302026', 'RON'),
('300', 'RO01', '5000000012', '2026', 'WE', '20260914', '20260914', '09', '20260914', '105000', 'DILIE', 'MIGO', NULL, 'Recepție MP-40010 lot MP26-0079', 'MKPF', '50000415622026', 'RON'),
('300', 'RO01', '5000000013', '2026', 'WE', '20260921', '20260921', '09', '20260921', '112000', 'DILIE', 'MIGO', NULL, 'Recepție MP-10020 lot MP26-0081', 'MKPF', '50000416012026', 'RON'),
('300', 'RO01', '5000000014', '2026', 'WE', '20260924', '20260924', '09', '20260924', '094000', 'DILIE', 'MIGO', NULL, 'Recepție AMB-30050 lot MP26-0082', 'MKPF', '50000416222026', 'RON'),
('300', 'RO01', '5105600001', '2026', 'RE', '20260612', '20260612', '06', '20260612', '113000', 'ONISTOR', 'MIRO', 'HPPL/EXP/26183', 'Factură furnizor HPPL/EXP/26183', 'RMRP', '5105600001', 'EUR'),
('300', 'RO01', '5105600002', '2026', 'RE', '20260614', '20260614', '06', '20260614', '113000', 'ONISTOR', 'MIRO', 'CC-26189', 'Factură furnizor CC-26189', 'RMRP', '5105600002', 'RON'),
('300', 'RO01', '5105600003', '2026', 'RE', '20260617', '20260617', '06', '20260617', '113000', 'ONISTOR', 'MIRO', 'SG-INV-26192', 'Factură furnizor SG-INV-26192', 'RMRP', '5105600003', 'EUR'),
('300', 'RO01', '5105600004', '2026', 'RE', '20260701', '20260701', '07', '20260701', '113000', 'ONISTOR', 'MIRO', 'ACSD-FT-26198', 'Factură furnizor ACSD-FT-26198', 'RMRP', '5105600004', 'EUR'),
('300', 'RO01', '5105600005', '2026', 'RE', '20260703', '20260703', '07', '20260703', '113000', 'ONISTOR', 'MIRO', 'GXB/F/26201', 'Factură furnizor GXB/F/26201', 'RMRP', '5105600005', 'EUR'),
('300', 'RO01', '5105600006', '2026', 'RE', '20260715', '20260715', '07', '20260715', '113000', 'ONISTOR', 'MIRO', 'BAC-RE-26207', 'Factură furnizor BAC-RE-26207', 'RMRP', '5105600006', 'EUR'),
('300', 'RO01', '5105600007', '2026', 'RE', '20260729', '20260729', '07', '20260729', '113000', 'ONISTOR', 'MIRO', 'IPCA/EX/26213', 'Factură furnizor IPCA/EX/26213', 'RMRP', '5105600007', 'EUR'),
('300', 'RO01', '5105600008', '2026', 'RE', '20260730', '20260730', '07', '20260730', '113000', 'ONISTOR', 'MIRO', 'SG-INV-26216', 'Factură furnizor SG-INV-26216', 'RMRP', '5105600008', 'EUR'),
('300', 'RO01', '5105600009', '2026', 'RE', '20260812', '20260812', '08', '20260812', '113000', 'ONISTOR', 'MIRO', 'HPPL/EXP/26222', 'Factură furnizor HPPL/EXP/26222', 'RMRP', '5105600009', 'EUR'),
('300', 'RO01', '5105600010', '2026', 'RE', '20260826', '20260826', '08', '20260826', '113000', 'ONISTOR', 'MIRO', 'IPCA/EX/26225', 'Factură furnizor IPCA/EX/26225', 'RMRP', '5105600010', 'EUR'),
('300', 'RO01', '5105600011', '2026', 'RE', '20260909', '20260909', '09', '20260909', '113000', 'ONISTOR', 'MIRO', 'BPT-26231', 'Factură furnizor BPT-26231', 'RMRP', '5105600011', 'EUR'),
('300', 'RO01', '5105600012', '2026', 'RE', '20260916', '20260916', '09', '20260916', '113000', 'ONISTOR', 'MIRO', 'MRK-RO-26237', 'Factură furnizor MRK-RO-26237', 'RMRP', '5105600012', 'RON'),
('300', 'RO01', '5105600013', '2026', 'RE', '20260715', '20260715', '07', '20260715', '113000', 'ONISTOR', 'MIRO', 'MTC-2026-0741', 'Factură furnizor MTC-2026-0741', 'RMRP', '5105600013', 'RON'),
('300', 'RO01', '5105600014', '2026', 'RE', '20260731', '20260731', '07', '20260731', '113000', 'ONISTOR', 'MIRO', 'CLF-26-10412', 'Factură furnizor CLF-26-10412', 'RMRP', '5105600014', 'RON'),
('300', 'RO01', '5105600015', '2026', 'RE', '20260810', '20260810', '08', '20260810', '113000', 'ONISTOR', 'MIRO', 'UMC-F-26-2217', 'Factură furnizor UMC-F-26-2217', 'RMRP', '5105600015', 'RON'),
('300', 'RO01', '5105600016', '2026', 'RE', '20260814', '20260814', '08', '20260814', '113000', 'ONISTOR', 'MIRO', 'FTP-2026-118', 'Factură furnizor FTP-2026-118', 'RMRP', '5105600016', 'RON'),
('300', 'RO01', '5105600017', '2026', 'RE', '20260831', '20260831', '08', '20260831', '113000', 'ONISTOR', 'MIRO', 'LGR-26-771904', 'Factură furnizor LGR-26-771904', 'RMRP', '5105600017', 'RON'),
('300', 'RO01', '5105600018', '2026', 'RE', '20260831', '20260831', '08', '20260831', '113000', 'ONISTOR', 'MIRO', 'CLF-26-11873', 'Factură furnizor CLF-26-11873', 'RMRP', '5105600018', 'RON'),
('300', 'RO01', '5105600019', '2026', 'RE', '20260919', '20260919', '09', '20260919', '113000', 'ONISTOR', 'MIRO', 'FTP-2026-131', 'Factură furnizor FTP-2026-131', 'RMRP', '5105600019', 'RON'),
('300', 'RO01', '2000000001', '2026', 'ZP', '20260807', '20260807', '08', '20260807', '061000', 'BATCH_F110', 'F110', 'HPPL/EXP/26183', 'Plată HPPL/EXP/26183', 'BKPF', '2000000001', 'EUR'),
('300', 'RO01', '2000000002', '2026', 'ZP', '20260724', '20260724', '07', '20260724', '061000', 'BATCH_F110', 'F110', 'CC-26189', 'Plată CC-26189', 'BKPF', '2000000002', 'RON'),
('300', 'RO01', '2000000003', '2026', 'ZP', '20260807', '20260807', '08', '20260807', '061000', 'BATCH_F110', 'F110', 'SG-INV-26192', 'Plată SG-INV-26192', 'BKPF', '2000000003', 'EUR'),
('300', 'RO01', '2000000004', '2026', 'ZP', '20260821', '20260821', '08', '20260821', '061000', 'BATCH_F110', 'F110', 'ACSD-FT-26198', 'Plată ACSD-FT-26198', 'BKPF', '2000000004', 'EUR'),
('300', 'RO01', '2000000005', '2026', 'ZP', '20260821', '20260821', '08', '20260821', '061000', 'BATCH_F110', 'F110', 'GXB/F/26201', 'Plată GXB/F/26201', 'BKPF', '2000000005', 'EUR'),
('300', 'RO01', '2000000006', '2026', 'ZP', '20260904', '20260904', '09', '20260904', '061000', 'BATCH_F110', 'F110', 'BAC-RE-26207', 'Plată BAC-RE-26207', 'BKPF', '2000000006', 'EUR'),
('300', 'RO01', '2000000007', '2026', 'ZP', '20260918', '20260918', '09', '20260918', '061000', 'BATCH_F110', 'F110', 'IPCA/EX/26213', 'Plată IPCA/EX/26213', 'BKPF', '2000000007', 'EUR'),
('300', 'RO01', '2000000008', '2026', 'ZP', '20260821', '20260821', '08', '20260821', '061000', 'BATCH_F110', 'F110', 'MTC-2026-0741', 'Plată MTC-2026-0741', 'BKPF', '2000000008', 'RON'),
('300', 'RO01', '2000000009', '2026', 'ZP', '20260904', '20260904', '09', '20260904', '061000', 'BATCH_F110', 'F110', 'CLF-26-10412', 'Plată CLF-26-10412', 'BKPF', '2000000009', 'RON'),
('300', 'RO01', '2000000010', '2026', 'ZP', '20260918', '20260918', '09', '20260918', '061000', 'BATCH_F110', 'F110', 'UMC-F-26-2217', 'Plată UMC-F-26-2217', 'BKPF', '2000000010', 'RON'),
('300', 'RO01', '2000000011', '2026', 'ZP', '20260918', '20260918', '09', '20260918', '061000', 'BATCH_F110', 'F110', 'FTP-2026-118', 'Plată FTP-2026-118', 'BKPF', '2000000011', 'RON'),
('300', 'RO01', '2000000012', '2026', 'ZP', '20260925', '20260925', '09', '20260925', '061000', 'BATCH_F110', 'F110', 'FTP-2026-131', 'Plată FTP-2026-131', 'BKPF', '2000000012', 'RON'),
('300', 'RO01', '4900000001', '2026', 'WA', '20260706', '20260706', '07', '20260706', '202000', 'OPCENTER_RFC', 'MIGO_GI', 'EK26-0311', 'Consum ordin 4000311 lot EK26-0311', 'IDOC', '0000000002261429', 'RON'),
('300', 'RO01', '4900000002', '2026', 'WE', '20260708', '20260708', '07', '20260708', '163000', 'OPCENTER_RFC', 'MIGO_GR', 'EK26-0311', 'Predare produs finit lot EK26-0311', 'IDOC', '0000000002261458', 'RON'),
('300', 'RO01', '4900000003', '2026', 'WA', '20260714', '20260714', '07', '20260714', '211000', 'OPCENTER_RFC', 'MIGO_GI', 'SA26-0031', 'Consum ordin 4100031 lot SA26-0031', 'IDOC', '0000000002261487', 'RON'),
('300', 'RO01', '4900000004', '2026', 'WE', '20260715', '20260715', '07', '20260715', '163000', 'OPCENTER_RFC', 'MIGO_GR', 'SA26-0031', 'Predare produs finit lot SA26-0031', 'IDOC', '0000000002261516', 'RON'),
('300', 'RO01', '4900000005', '2026', 'WA', '20260721', '20260721', '07', '20260721', '003000', 'OPCENTER_RFC', 'MIGO_GI', 'EK26-0318', 'Consum ordin 4000318 lot EK26-0318', 'IDOC', '0000000002261545', 'RON'),
('300', 'RO01', '4900000006', '2026', 'WE', '20260722', '20260722', '07', '20260722', '143000', 'OPCENTER_RFC', 'MIGO_GR', 'EK26-0318', 'Predare produs finit lot EK26-0318', 'IDOC', '0000000002261574', 'RON'),
('300', 'RO01', '4900000007', '2026', 'WA', '20260803', '20260803', '08', '20260803', '200500', 'OPCENTER_RFC', 'MIGO_GI', 'EK26-0324', 'Consum ordin 4000324 lot EK26-0324', 'IDOC', '0000000002261603', 'RON'),
('300', 'RO01', '4900000008', '2026', 'WE', '20260805', '20260805', '08', '20260805', '153000', 'OPCENTER_RFC', 'MIGO_GR', 'EK26-0324', 'Predare produs finit lot EK26-0324', 'IDOC', '0000000002261632', 'RON'),
('300', 'RO01', '4900000009', '2026', 'WA', '20260804', '20260804', '08', '20260804', '221000', 'OPCENTER_RFC', 'MIGO_GI', 'SA26-0034', 'Consum ordin 4100034 lot SA26-0034', 'IDOC', '0000000002261661', 'RON'),
('300', 'RO01', '4900000010', '2026', 'WE', '20260805', '20260805', '08', '20260805', '173000', 'OPCENTER_RFC', 'MIGO_GR', 'SA26-0034', 'Predare produs finit lot SA26-0034', 'IDOC', '0000000002261690', 'RON'),
('300', 'RO01', '4900000011', '2026', 'WA', '20260817', '20260817', '08', '20260817', '202000', 'OPCENTER_RFC', 'MIGO_GI', 'EK26-0329', 'Consum ordin 4000329 lot EK26-0329', 'IDOC', '0000000002261719', 'RON'),
('300', 'RO01', '4900000012', '2026', 'WE', '20260819', '20260819', '08', '20260819', '163000', 'OPCENTER_RFC', 'MIGO_GR', 'EK26-0329', 'Predare produs finit lot EK26-0329', 'IDOC', '0000000002261748', 'RON'),
('300', 'RO01', '4900000013', '2026', 'WA', '20260826', '20260826', '08', '20260826', '163000', 'OPCENTER_RFC', 'MIGO_GI', 'SA26-0037', 'Consum ordin 4100037 lot SA26-0037', 'IDOC', '0000000002261777', 'RON'),
('300', 'RO01', '4900000014', '2026', 'WE', '20260827', '20260827', '08', '20260827', '123000', 'OPCENTER_RFC', 'MIGO_GR', 'SA26-0037', 'Predare produs finit lot SA26-0037', 'IDOC', '0000000002261806', 'RON'),
('300', 'RO01', '4900000015', '2026', 'WA', '20260831', '20260831', '08', '20260831', '172600', 'OPCENTER_RFC', 'MIGO_GI', 'EK26-0335', 'Consum ordin 4000335 lot EK26-0335', 'IDOC', '0000000002261835', 'RON'),
('300', 'RO01', '4900000016', '2026', 'WE', '20260902', '20260902', '09', '20260902', '163000', 'OPCENTER_RFC', 'MIGO_GR', 'EK26-0335', 'Predare produs finit lot EK26-0335', 'IDOC', '0000000002261864', 'RON'),
('300', 'RO01', '4900000017', '2026', 'WA', '20260914', '20260914', '09', '20260914', '171400', 'OPCENTER_RFC', 'MIGO_GI', 'EK26-0341', 'Consum ordin 4000341 lot EK26-0341', 'IDOC', '0000000002261893', 'RON'),
('300', 'RO01', '4900000018', '2026', 'WE', '20260916', '20260916', '09', '20260916', '153000', 'OPCENTER_RFC', 'MIGO_GR', 'EK26-0341', 'Predare produs finit lot EK26-0341', 'IDOC', '0000000002261922', 'RON'),
('300', 'RO01', '4900000019', '2026', 'WA', '20260916', '20260916', '09', '20260916', '163000', 'OPCENTER_RFC', 'MIGO_GI', 'SA26-0040', 'Consum ordin 4100040 lot SA26-0040', 'IDOC', '0000000002261951', 'RON'),
('300', 'RO01', '4900000020', '2026', 'WE', '20260917', '20260917', '09', '20260917', '123000', 'OPCENTER_RFC', 'MIGO_GR', 'SA26-0040', 'Predare produs finit lot SA26-0040', 'IDOC', '0000000002261980', 'RON'),
('300', 'RO01', '4910000001', '2026', 'WL', '20260727', '20260727', '07', '20260727', '170000', 'WMS_RFC', 'BAPI', NULL, 'Confirmări expediție WMS 2026-07', 'IDOC', '0000000002262067', 'RON'),
('300', 'RO01', '4910000002', '2026', 'WL', '20260828', '20260828', '08', '20260828', '174000', 'WMS_RFC', 'BAPI', NULL, 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002262096', 'RON'),
('300', 'RO01', '4910000003', '2026', 'WL', '20260918', '20260918', '09', '20260918', '173000', 'WMS_RFC', 'BAPI', NULL, 'Confirmări expediție WMS 2026-09', 'IDOC', '0000000002262125', 'RON'),
('300', 'RO01', '2000000013', '2026', 'ZS', '20260810', '20260810', '08', '20260810', '080000', 'MAPOSTOL', 'F-53', NULL, 'Plată salarii nete PR-RO01-2026-07', 'BKPF', '2000000013', 'RON'),
('300', 'RO01', '2000000014', '2026', 'ZS', '20260825', '20260825', '08', '20260825', '093000', 'MAPOSTOL', 'F-53', NULL, 'Plată contribuții și impozit ANAF PR-RO01-2026-07', 'BKPF', '2000000014', 'RON'),
('300', 'RO01', '1000000001', '2026', 'ZL', '20260731', '20260731', '07', '20260807', '203000', 'WORKDAY_RFC', 'BAPI', 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002262154', 'RON'),
('300', 'RO01', '2000000015', '2026', 'ZS', '20260910', '20260910', '09', '20260910', '080000', 'MAPOSTOL', 'F-53', NULL, 'Plată salarii nete PR-RO01-2026-08', 'BKPF', '2000000015', 'RON'),
('300', 'RO01', '2000000016', '2026', 'ZS', '20260925', '20260925', '09', '20260925', '093000', 'MAPOSTOL', 'F-53', NULL, 'Plată contribuții și impozit ANAF PR-RO01-2026-08', 'BKPF', '2000000016', 'RON'),
('300', 'RO01', '1000000002', '2026', 'ZL', '20260831', '20260831', '08', '20260907', '203000', 'WORKDAY_RFC', 'BAPI', 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002262183', 'RON'),
('300', 'RO01', '1000000003', '2026', 'ZE', '20260728', '20260728', '07', '20260728', '221500', 'CONCUR_RFC', 'BAPI', 'CONCUR-2026-07', 'Decont cheltuieli Concur 2026-07', 'IDOC', '0000000002262212', 'RON'),
('300', 'RO01', '1000000004', '2026', 'ZE', '20260828', '20260828', '08', '20260828', '221500', 'CONCUR_RFC', 'BAPI', 'CONCUR-2026-08', 'Decont cheltuieli Concur 2026-08', 'IDOC', '0000000002262241', 'RON'),
('300', 'RO01', '1000000005', '2026', 'ZM', '20260727', '20260727', '07', '20260727', '231000', 'MAXIMO_RFC', 'BAPI', 'MX-2026-07', 'Costuri ordine de lucru Maximo 2026-07', 'IDOC', '0000000002262299', 'RON'),
('300', 'RO01', '1000000006', '2026', 'ZM', '20260827', '20260827', '08', '20260827', '231000', 'MAXIMO_RFC', 'BAPI', 'MX-2026-08', 'Costuri ordine de lucru Maximo 2026-08', 'IDOC', '0000000002262328', 'RON'),
('300', 'RO01', '1000000007', '2026', 'ZM', '20260927', '20260927', '09', '20260927', '231000', 'MAXIMO_RFC', 'BAPI', 'MX-2026-09', 'Costuri ordine de lucru Maximo 2026-09', 'IDOC', '0000000002262357', 'RON'),
('300', 'RO01', '1900000011', '2026', 'SA', '20260731', '20260731', '07', '20260805', '211100', 'MAPOSTOL', 'FBV0', NULL, 'Accrual audit statutar 2026 - onorariu auditor financiar', 'BKPF', '1900000011', 'RON'),
('300', 'RO01', '1900000014', '2026', 'SA', '20260831', '20260831', '08', '20260903', '112500', 'SFLORESCU', 'FBV0', NULL, 'Provizion concedii de odihnă neefectuate la 31.08.2026', 'BKPF', '1900000014', 'RON'),
('300', 'RO01', '9400000001', '2026', 'RV', '20260720', '20260720', '07', '20260720', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000531', 'Factura EKG26-000531 comanda 120031', 'VBRK', '90004113', 'RON'),
('300', 'RO01', '9400000002', '2026', 'RV', '20260810', '20260810', '08', '20260810', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000534', 'Factura EKG26-000534 comanda 120034', 'VBRK', '90004126', 'RON'),
('300', 'RO01', '9400000003', '2026', 'RV', '20260831', '20260831', '08', '20260831', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000537', 'Factura EKG26-000537 comanda 120037', 'VBRK', '90004139', 'RON'),
('300', 'RO01', '9400000004', '2026', 'RV', '20260921', '20260921', '09', '20260921', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000540', 'Factura EKG26-000540 comanda 120040', 'VBRK', '90004152', 'RON'),
('300', 'RO01', '1400000001', '2026', 'DZ', '20260905', '20260905', '09', '20260905', '100000', 'MAPOSTOL', 'F-28', 'EKG26-000596', 'Încasare EKG26-000596', 'BKPF', '1400000001', 'RON'),
('300', 'RO01', '9400000005', '2026', 'RV', '20260727', '20260727', '07', '20260727', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000596', 'Factura EKG26-000596 comanda 110396', 'VBRK', '90004165', 'RON'),
('300', 'RO01', '1400000002', '2026', 'DZ', '20260911', '20260911', '09', '20260911', '100000', 'MAPOSTOL', 'F-28', 'EKG26-000607', 'Încasare EKG26-000607', 'BKPF', '1400000002', 'EUR'),
('300', 'RO01', '9400000006', '2026', 'RV', '20260813', '20260813', '08', '20260813', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000607', 'Factura EKG26-000607 comanda 110407', 'VBRK', '90004178', 'EUR'),
('300', 'RO01', '9400000007', '2026', 'RV', '20260824', '20260824', '08', '20260824', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000609', 'Factura EKG26-000609 comanda 110409', 'VBRK', '90004191', 'RON'),
('300', 'RO01', '9400000008', '2026', 'RV', '20260916', '20260916', '09', '20260916', '190000', 'BATCH_VF04', 'VF01', 'EKG26-000618', 'Factura EKG26-000618 comanda 110418', 'VBRK', '90004204', 'EUR')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.acdoca (
  rclnt  varchar(3) NOT NULL,
  rldnr  varchar(2) NOT NULL,
  rbukrs varchar(4) NOT NULL,
  gjahr  varchar(4) NOT NULL,
  belnr  varchar(10) NOT NULL,
  docln  varchar(6) NOT NULL,
  racct  varchar(10) NOT NULL,
  rcntr  varchar(20),
  hsl    numeric(23,2) NOT NULL,
  rhcur  varchar(5) NOT NULL,
  wsl    numeric(23,2) NOT NULL,
  rwcur  varchar(5) NOT NULL,
  drcrk  varchar(1) NOT NULL,
  budat  varchar(8) NOT NULL,
  poper  varchar(3) NOT NULL,
  koart  varchar(1) NOT NULL,
  lifnr  varchar(10),
  kunnr  varchar(10),
  matnr  varchar(40),
  zuonr  varchar(18),
  sgtxt  varchar(50),
  awtyp  varchar(5),
  awref  varchar(10),
  netdt  varchar(8),
  augbl  varchar(10),
  augdt  varchar(8),
  CONSTRAINT acdoca_pk PRIMARY KEY (rclnt, rldnr, rbukrs, gjahr, belnr, docln)
);
COMMENT ON TABLE sap_s4hana.acdoca IS 'Universal journal line items, leading ledger 0L (hsl in RON, wsl in document currency, debit positive; netdt net due date; augbl/augdt clearing).';

INSERT INTO sap_s4hana.acdoca (rclnt, rldnr, rbukrs, gjahr, belnr, docln, racct, rcntr, hsl, rhcur, wsl, rwcur, drcrk, budat, poper, koart, lifnr, kunnr, matnr, zuonr, sgtxt, awtyp, awref, netdt, augbl, augdt) VALUES
('300', '0L', 'RO01', '2026', '5000000001', '000001', '0000301000', NULL, 36766.20, 'RON', 36766.20, 'RON', 'S', '20260610', '006', 'M', NULL, NULL, 'MP-10010', 'MP26-0061', 'Recepție MP-10010 lot MP26-0061', 'MKPF', '5000041207', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000001', '000002', '0000408000', NULL, -36766.20, 'RON', -36766.20, 'RON', 'H', '20260610', '006', 'S', NULL, NULL, NULL, '4500002611', 'Recepție MP-10010 lot MP26-0061', 'MKPF', '5000041207', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000002', '000001', '0000301000', NULL, 2900.00, 'RON', 2900.00, 'RON', 'S', '20260612', '006', 'M', NULL, NULL, 'MP-20010', 'MP26-0063', 'Recepție MP-20010 lot MP26-0063', 'MKPF', '5000041219', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000002', '000002', '0000408000', NULL, -2900.00, 'RON', -2900.00, 'RON', 'H', '20260612', '006', 'S', NULL, NULL, NULL, '4500002614', 'Recepție MP-20010 lot MP26-0063', 'MKPF', '5000041219', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000003', '000001', '0000381000', NULL, 12475.15, 'RON', 12475.15, 'RON', 'S', '20260615', '006', 'M', NULL, NULL, 'AMB-30010', 'MP26-0064', 'Recepție AMB-30010 lot MP26-0064', 'MKPF', '5000041231', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000003', '000002', '0000408000', NULL, -12475.15, 'RON', -12475.15, 'RON', 'H', '20260615', '006', 'S', NULL, NULL, NULL, '4500002617', 'Recepție AMB-30010 lot MP26-0064', 'MKPF', '5000041231', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000004', '000001', '0000301000', NULL, 123737.28, 'RON', 123737.28, 'RON', 'S', '20260629', '006', 'M', NULL, NULL, 'MP-10020', 'MP26-0066', 'Recepție MP-10020 lot MP26-0066', 'MKPF', '5000041288', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000004', '000002', '0000408000', NULL, -123737.28, 'RON', -123737.28, 'RON', 'H', '20260629', '006', 'S', NULL, NULL, NULL, '4500002630', 'Recepție MP-10020 lot MP26-0066', 'MKPF', '5000041288', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000005', '000001', '0000381000', NULL, 19176.79, 'RON', 19176.79, 'RON', 'S', '20260701', '007', 'M', NULL, NULL, 'AMB-30030', 'MP26-0067', 'Recepție AMB-30030 lot MP26-0067', 'MKPF', '5000041296', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000005', '000002', '0000408000', NULL, -19176.79, 'RON', -19176.79, 'RON', 'H', '20260701', '007', 'S', NULL, NULL, NULL, '4500002633', 'Recepție AMB-30030 lot MP26-0067', 'MKPF', '5000041296', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000006', '000001', '0000301000', NULL, 39613.08, 'RON', 39613.08, 'RON', 'S', '20260713', '007', 'M', NULL, NULL, 'MP-10050', 'MP26-0069', 'Recepție MP-10050 lot MP26-0069', 'MKPF', '5000041342', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000006', '000002', '0000408000', NULL, -39613.08, 'RON', -39613.08, 'RON', 'H', '20260713', '007', 'S', NULL, NULL, NULL, '4500002641', 'Recepție MP-10050 lot MP26-0069', 'MKPF', '5000041342', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000007', '000001', '0000301000', NULL, 4697.70, 'RON', 4697.70, 'RON', 'S', '20260727', '007', 'M', NULL, NULL, 'MP-10030', 'MP26-0071', 'Recepție MP-10030 lot MP26-0071', 'MKPF', '5000041388', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000007', '000002', '0000408000', NULL, -4697.70, 'RON', -4697.70, 'RON', 'H', '20260727', '007', 'S', NULL, NULL, NULL, '4500002652', 'Recepție MP-10030 lot MP26-0071', 'MKPF', '5000041388', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000008', '000001', '0000381000', NULL, 14016.94, 'RON', 14016.94, 'RON', 'S', '20260728', '007', 'M', NULL, NULL, 'AMB-30020', 'MP26-0072', 'Recepție AMB-30020 lot MP26-0072', 'MKPF', '5000041395', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000008', '000002', '0000408000', NULL, -14016.94, 'RON', -14016.94, 'RON', 'H', '20260728', '007', 'S', NULL, NULL, NULL, '4500002655', 'Recepție AMB-30020 lot MP26-0072', 'MKPF', '5000041395', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000009', '000001', '0000301000', NULL, 36852.48, 'RON', 36852.48, 'RON', 'S', '20260810', '008', 'M', NULL, NULL, 'MP-10010', 'MP26-0074', 'Recepție MP-10010 lot MP26-0074', 'MKPF', '5000041447', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000009', '000002', '0000408000', NULL, -36852.48, 'RON', -36852.48, 'RON', 'H', '20260810', '008', 'S', NULL, NULL, NULL, '4500002668', 'Recepție MP-10010 lot MP26-0074', 'MKPF', '5000041447', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000010', '000001', '0000301000', NULL, 11182.82, 'RON', 11182.82, 'RON', 'S', '20260824', '008', 'M', NULL, NULL, 'MP-10040', 'MP26-0075', 'Recepție MP-10040 lot MP26-0075', 'MKPF', '5000041489', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000010', '000002', '0000408000', NULL, -11182.82, 'RON', -11182.82, 'RON', 'H', '20260824', '008', 'S', NULL, NULL, NULL, '4500002674', 'Recepție MP-10040 lot MP26-0075', 'MKPF', '5000041489', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000011', '000001', '0000301000', NULL, 26979.12, 'RON', 26979.12, 'RON', 'S', '20260907', '009', 'M', NULL, NULL, 'MP-10050', 'MP26-0077', 'Recepție MP-10050 lot MP26-0077', 'MKPF', '5000041530', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000011', '000002', '0000408000', NULL, -26979.12, 'RON', -26979.12, 'RON', 'H', '20260907', '009', 'S', NULL, NULL, NULL, '4500002683', 'Recepție MP-10050 lot MP26-0077', 'MKPF', '5000041530', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000012', '000001', '0000301000', NULL, 980.00, 'RON', 980.00, 'RON', 'S', '20260914', '009', 'M', NULL, NULL, 'MP-40010', 'MP26-0079', 'Recepție MP-40010 lot MP26-0079', 'MKPF', '5000041562', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000012', '000002', '0000408000', NULL, -980.00, 'RON', -980.00, 'RON', 'H', '20260914', '009', 'S', NULL, NULL, NULL, '4500002689', 'Recepție MP-40010 lot MP26-0079', 'MKPF', '5000041562', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000013', '000001', '0000301000', NULL, 124205.76, 'RON', 124205.76, 'RON', 'S', '20260921', '009', 'M', NULL, NULL, 'MP-10020', 'MP26-0081', 'Recepție MP-10020 lot MP26-0081', 'MKPF', '5000041601', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000013', '000002', '0000408000', NULL, -124205.76, 'RON', -124205.76, 'RON', 'H', '20260921', '009', 'S', NULL, NULL, NULL, '4500002697', 'Recepție MP-10020 lot MP26-0081', 'MKPF', '5000041601', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000014', '000001', '0000381000', NULL, 4050.00, 'RON', 4050.00, 'RON', 'S', '20260924', '009', 'M', NULL, NULL, 'AMB-30050', 'MP26-0082', 'Recepție AMB-30050 lot MP26-0082', 'MKPF', '5000041622', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5000000014', '000002', '0000408000', NULL, -4050.00, 'RON', -4050.00, 'RON', 'H', '20260924', '009', 'S', NULL, NULL, NULL, '4500002699', 'Recepție AMB-30050 lot MP26-0082', 'MKPF', '5000041622', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600001', '000001', '0000408000', NULL, 36766.20, 'RON', 7250.00, 'EUR', 'S', '20260612', '006', 'S', NULL, NULL, NULL, 'HPPL/EXP/26183', 'Factură furnizor HPPL/EXP/26183', 'RMRP', '5105600001', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600001', '000002', '0000401000', NULL, -36766.20, 'RON', -7250.00, 'EUR', 'H', '20260612', '006', 'K', '0000700110', NULL, NULL, 'HPPL/EXP/26183', 'Factură furnizor HPPL/EXP/26183', 'RMRP', '5105600001', '20260727', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600002', '000001', '0000408000', NULL, 2900.00, 'RON', 2900.00, 'RON', 'S', '20260614', '006', 'S', NULL, NULL, NULL, 'CC-26189', 'Factură furnizor CC-26189', 'RMRP', '5105600002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600002', '000002', '0000442600', NULL, 609.00, 'RON', 609.00, 'RON', 'S', '20260614', '006', 'S', NULL, NULL, NULL, 'CC-26189', 'Factură furnizor CC-26189', 'RMRP', '5105600002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600002', '000003', '0000401000', NULL, -3509.00, 'RON', -3509.00, 'RON', 'H', '20260614', '006', 'K', '0000700150', NULL, NULL, 'CC-26189', 'Factură furnizor CC-26189', 'RMRP', '5105600002', '20260714', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600003', '000001', '0000408000', NULL, 12475.15, 'RON', 2460.00, 'EUR', 'S', '20260617', '006', 'S', NULL, NULL, NULL, 'SG-INV-26192', 'Factură furnizor SG-INV-26192', 'RMRP', '5105600003', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600003', '000002', '0000401000', NULL, -12475.15, 'RON', -2460.00, 'EUR', 'H', '20260617', '006', 'K', '0000700170', NULL, NULL, 'SG-INV-26192', 'Factură furnizor SG-INV-26192', 'RMRP', '5105600003', '20260801', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600004', '000001', '0000408000', NULL, 123917.84, 'RON', 24400.00, 'EUR', 'S', '20260701', '007', 'S', NULL, NULL, NULL, 'ACSD-FT-26198', 'Factură furnizor ACSD-FT-26198', 'RMRP', '5105600004', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600004', '000002', '0000401000', NULL, -123917.84, 'RON', -24400.00, 'EUR', 'H', '20260701', '007', 'K', '0000700120', NULL, NULL, 'ACSD-FT-26198', 'Factură furnizor ACSD-FT-26198', 'RMRP', '5105600004', '20260815', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600005', '000001', '0000408000', NULL, 19176.79, 'RON', 3776.00, 'EUR', 'S', '20260703', '007', 'S', NULL, NULL, NULL, 'GXB/F/26201', 'Factură furnizor GXB/F/26201', 'RMRP', '5105600005', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600005', '000002', '0000401000', NULL, -19176.79, 'RON', -3776.00, 'EUR', 'H', '20260703', '007', 'K', '0000700180', NULL, NULL, 'GXB/F/26201', 'Factură furnizor GXB/F/26201', 'RMRP', '5105600005', '20260817', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600006', '000001', '0000408000', NULL, 39613.08, 'RON', 7800.00, 'EUR', 'S', '20260715', '007', 'S', NULL, NULL, NULL, 'BAC-RE-26207', 'Factură furnizor BAC-RE-26207', 'RMRP', '5105600006', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600006', '000002', '0000401000', NULL, -39613.08, 'RON', -7800.00, 'EUR', 'H', '20260715', '007', 'K', '0000700140', NULL, NULL, 'BAC-RE-26207', 'Factură furnizor BAC-RE-26207', 'RMRP', '5105600006', '20260829', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600007', '000001', '0000408000', NULL, 4697.70, 'RON', 925.00, 'EUR', 'S', '20260729', '007', 'S', NULL, NULL, NULL, 'IPCA/EX/26213', 'Factură furnizor IPCA/EX/26213', 'RMRP', '5105600007', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600007', '000002', '0000401000', NULL, -4697.70, 'RON', -925.00, 'EUR', 'H', '20260729', '007', 'K', '0000700130', NULL, NULL, 'IPCA/EX/26213', 'Factură furnizor IPCA/EX/26213', 'RMRP', '5105600007', '20260912', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600008', '000001', '0000408000', NULL, 14931.08, 'RON', 2940.00, 'EUR', 'S', '20260730', '007', 'S', NULL, NULL, NULL, 'SG-INV-26216', 'Factură furnizor SG-INV-26216', 'RMRP', '5105600008', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600008', '000002', '0000401000', NULL, -14931.08, 'RON', -2940.00, 'EUR', 'H', '20260730', '007', 'K', '0000700170', NULL, NULL, 'SG-INV-26216', 'Factură furnizor SG-INV-26216', 'RMRP', '5105600008', '20260913', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600009', '000001', '0000408000', NULL, 36852.48, 'RON', 7250.00, 'EUR', 'S', '20260812', '008', 'S', NULL, NULL, NULL, 'HPPL/EXP/26222', 'Factură furnizor HPPL/EXP/26222', 'RMRP', '5105600009', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600009', '000002', '0000401000', NULL, -36852.48, 'RON', -7250.00, 'EUR', 'H', '20260812', '008', 'K', '0000700110', NULL, NULL, 'HPPL/EXP/26222', 'Factură furnizor HPPL/EXP/26222', 'RMRP', '5105600009', '20260926', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600010', '000001', '0000408000', NULL, 11182.82, 'RON', 2200.00, 'EUR', 'S', '20260826', '008', 'S', NULL, NULL, NULL, 'IPCA/EX/26225', 'Factură furnizor IPCA/EX/26225', 'RMRP', '5105600010', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600010', '000002', '0000401000', NULL, -11182.82, 'RON', -2200.00, 'EUR', 'H', '20260826', '008', 'K', '0000700130', NULL, NULL, 'IPCA/EX/26225', 'Factură furnizor IPCA/EX/26225', 'RMRP', '5105600010', '20261010', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600011', '000001', '0000408000', NULL, 26979.12, 'RON', 5300.00, 'EUR', 'S', '20260909', '009', 'S', NULL, NULL, NULL, 'BPT-26231', 'Factură furnizor BPT-26231', 'RMRP', '5105600011', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600011', '000002', '0000401000', NULL, -26979.12, 'RON', -5300.00, 'EUR', 'H', '20260909', '009', 'K', '0000700240', NULL, NULL, 'BPT-26231', 'Factură furnizor BPT-26231', 'RMRP', '5105600011', '20261024', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600012', '000001', '0000408000', NULL, 980.00, 'RON', 980.00, 'RON', 'S', '20260916', '009', 'S', NULL, NULL, NULL, 'MRK-RO-26237', 'Factură furnizor MRK-RO-26237', 'RMRP', '5105600012', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600012', '000002', '0000442600', NULL, 205.80, 'RON', 205.80, 'RON', 'S', '20260916', '009', 'S', NULL, NULL, NULL, 'MRK-RO-26237', 'Factură furnizor MRK-RO-26237', 'RMRP', '5105600012', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600012', '000003', '0000401000', NULL, -1185.80, 'RON', -1185.80, 'RON', 'H', '20260916', '009', 'K', '0000700160', NULL, NULL, 'MRK-RO-26237', 'Factură furnizor MRK-RO-26237', 'RMRP', '5105600012', '20261016', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600013', '000001', '0000611000', 'RO10-150', 6800.00, 'RON', 6800.00, 'RON', 'S', '20260715', '007', 'S', NULL, NULL, NULL, 'MTC-2026-0741', 'Factură furnizor MTC-2026-0741', 'RMRP', '5105600013', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600013', '000002', '0000442600', NULL, 1428.00, 'RON', 1428.00, 'RON', 'S', '20260715', '007', 'S', NULL, NULL, NULL, 'MTC-2026-0741', 'Factură furnizor MTC-2026-0741', 'RMRP', '5105600013', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600013', '000003', '0000401000', NULL, -8228.00, 'RON', -8228.00, 'RON', 'H', '20260715', '007', 'K', '0000700200', NULL, NULL, 'MTC-2026-0741', 'Factură furnizor MTC-2026-0741', 'RMRP', '5105600013', '20260814', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600014', '000001', '0000624000', 'RO10-140', 9350.00, 'RON', 9350.00, 'RON', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'CLF-26-10412', 'Factură furnizor CLF-26-10412', 'RMRP', '5105600014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600014', '000002', '0000442600', NULL, 1963.50, 'RON', 1963.50, 'RON', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'CLF-26-10412', 'Factură furnizor CLF-26-10412', 'RMRP', '5105600014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600014', '000003', '0000401000', NULL, -11313.50, 'RON', -11313.50, 'RON', 'H', '20260731', '007', 'K', '0000700220', NULL, NULL, 'CLF-26-10412', 'Factură furnizor CLF-26-10412', 'RMRP', '5105600014', '20260830', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600015', '000001', '0000624000', 'RO10-140', 2860.00, 'RON', 2860.00, 'RON', 'S', '20260810', '008', 'S', NULL, NULL, NULL, 'UMC-F-26-2217', 'Factură furnizor UMC-F-26-2217', 'RMRP', '5105600015', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600015', '000002', '0000442600', NULL, 600.60, 'RON', 600.60, 'RON', 'S', '20260810', '008', 'S', NULL, NULL, NULL, 'UMC-F-26-2217', 'Factură furnizor UMC-F-26-2217', 'RMRP', '5105600015', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600015', '000003', '0000401000', NULL, -3460.60, 'RON', -3460.60, 'RON', 'H', '20260810', '008', 'K', '0000700250', NULL, NULL, 'UMC-F-26-2217', 'Factură furnizor UMC-F-26-2217', 'RMRP', '5105600015', '20260909', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600016', '000001', '0000611000', 'RO10-150', 14200.00, 'RON', 14200.00, 'RON', 'S', '20260814', '008', 'S', NULL, NULL, NULL, 'FTP-2026-118', 'Factură furnizor FTP-2026-118', 'RMRP', '5105600016', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600016', '000002', '0000442600', NULL, 2982.00, 'RON', 2982.00, 'RON', 'S', '20260814', '008', 'S', NULL, NULL, NULL, 'FTP-2026-118', 'Factură furnizor FTP-2026-118', 'RMRP', '5105600016', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600016', '000003', '0000401000', NULL, -17182.00, 'RON', -17182.00, 'RON', 'H', '20260814', '008', 'K', '0000700210', NULL, NULL, 'FTP-2026-118', 'Factură furnizor FTP-2026-118', 'RMRP', '5105600016', '20260913', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600017', '000001', '0000604000', 'RO10-140', 3145.00, 'RON', 3145.00, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'LGR-26-771904', 'Factură furnizor LGR-26-771904', 'RMRP', '5105600017', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600017', '000002', '0000442600', NULL, 660.45, 'RON', 660.45, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'LGR-26-771904', 'Factură furnizor LGR-26-771904', 'RMRP', '5105600017', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600017', '000003', '0000401000', NULL, -3805.45, 'RON', -3805.45, 'RON', 'H', '20260831', '008', 'K', '0000700230', NULL, NULL, 'LGR-26-771904', 'Factură furnizor LGR-26-771904', 'RMRP', '5105600017', '20260930', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600018', '000001', '0000624000', 'RO10-140', 11820.00, 'RON', 11820.00, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'CLF-26-11873', 'Factură furnizor CLF-26-11873', 'RMRP', '5105600018', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600018', '000002', '0000442600', NULL, 2482.20, 'RON', 2482.20, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'CLF-26-11873', 'Factură furnizor CLF-26-11873', 'RMRP', '5105600018', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600018', '000003', '0000401000', NULL, -14302.20, 'RON', -14302.20, 'RON', 'H', '20260831', '008', 'K', '0000700220', NULL, NULL, 'CLF-26-11873', 'Factură furnizor CLF-26-11873', 'RMRP', '5105600018', '20260930', NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600019', '000001', '0000611000', 'RO10-150', 48900.00, 'RON', 48900.00, 'RON', 'S', '20260919', '009', 'S', NULL, NULL, NULL, 'FTP-2026-131', 'Factură furnizor FTP-2026-131', 'RMRP', '5105600019', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600019', '000002', '0000442600', NULL, 10269.00, 'RON', 10269.00, 'RON', 'S', '20260919', '009', 'S', NULL, NULL, NULL, 'FTP-2026-131', 'Factură furnizor FTP-2026-131', 'RMRP', '5105600019', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '5105600019', '000003', '0000401000', NULL, -59169.00, 'RON', -59169.00, 'RON', 'H', '20260919', '009', 'K', '0000700210', NULL, NULL, 'FTP-2026-131', 'Factură furnizor FTP-2026-131', 'RMRP', '5105600019', '20261019', NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000001', '000001', '0000401000', NULL, 36852.48, 'RON', 7250.00, 'EUR', 'S', '20260807', '008', 'K', '0000700110', NULL, NULL, 'HPPL/EXP/26183', 'Plată HPPL/EXP/26183', 'BKPF', '2000000001', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000001', '000002', '0000512400', NULL, -36852.48, 'RON', -7250.00, 'EUR', 'H', '20260807', '008', 'S', NULL, NULL, NULL, 'HPPL/EXP/26183', 'Plată HPPL/EXP/26183', 'BKPF', '2000000001', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000002', '000001', '0000401000', NULL, 3509.00, 'RON', 3509.00, 'RON', 'S', '20260724', '007', 'K', '0000700150', NULL, NULL, 'CC-26189', 'Plată CC-26189', 'BKPF', '2000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000002', '000002', '0000512100', NULL, -3509.00, 'RON', -3509.00, 'RON', 'H', '20260724', '007', 'S', NULL, NULL, NULL, 'CC-26189', 'Plată CC-26189', 'BKPF', '2000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000003', '000001', '0000401000', NULL, 12504.43, 'RON', 2460.00, 'EUR', 'S', '20260807', '008', 'K', '0000700170', NULL, NULL, 'SG-INV-26192', 'Plată SG-INV-26192', 'BKPF', '2000000003', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000003', '000002', '0000512400', NULL, -12504.43, 'RON', -2460.00, 'EUR', 'H', '20260807', '008', 'S', NULL, NULL, NULL, 'SG-INV-26192', 'Plată SG-INV-26192', 'BKPF', '2000000003', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000004', '000001', '0000401000', NULL, 124027.64, 'RON', 24400.00, 'EUR', 'S', '20260821', '008', 'K', '0000700120', NULL, NULL, 'ACSD-FT-26198', 'Plată ACSD-FT-26198', 'BKPF', '2000000004', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000004', '000002', '0000512400', NULL, -124027.64, 'RON', -24400.00, 'EUR', 'H', '20260821', '008', 'S', NULL, NULL, NULL, 'ACSD-FT-26198', 'Plată ACSD-FT-26198', 'BKPF', '2000000004', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000005', '000001', '0000401000', NULL, 19193.79, 'RON', 3776.00, 'EUR', 'S', '20260821', '008', 'K', '0000700180', NULL, NULL, 'GXB/F/26201', 'Plată GXB/F/26201', 'BKPF', '2000000005', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000005', '000002', '0000512400', NULL, -19193.79, 'RON', -3776.00, 'EUR', 'H', '20260821', '008', 'S', NULL, NULL, NULL, 'GXB/F/26201', 'Plată GXB/F/26201', 'BKPF', '2000000005', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000006', '000001', '0000401000', NULL, 39705.12, 'RON', 7800.00, 'EUR', 'S', '20260904', '009', 'K', '0000700140', NULL, NULL, 'BAC-RE-26207', 'Plată BAC-RE-26207', 'BKPF', '2000000006', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000006', '000002', '0000512400', NULL, -39705.12, 'RON', -7800.00, 'EUR', 'H', '20260904', '009', 'S', NULL, NULL, NULL, 'BAC-RE-26207', 'Plată BAC-RE-26207', 'BKPF', '2000000006', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000007', '000001', '0000401000', NULL, 4708.62, 'RON', 925.00, 'EUR', 'S', '20260918', '009', 'K', '0000700130', NULL, NULL, 'IPCA/EX/26213', 'Plată IPCA/EX/26213', 'BKPF', '2000000007', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000007', '000002', '0000512400', NULL, -4708.62, 'RON', -925.00, 'EUR', 'H', '20260918', '009', 'S', NULL, NULL, NULL, 'IPCA/EX/26213', 'Plată IPCA/EX/26213', 'BKPF', '2000000007', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000008', '000001', '0000401000', NULL, 8228.00, 'RON', 8228.00, 'RON', 'S', '20260821', '008', 'K', '0000700200', NULL, NULL, 'MTC-2026-0741', 'Plată MTC-2026-0741', 'BKPF', '2000000008', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000008', '000002', '0000512100', NULL, -8228.00, 'RON', -8228.00, 'RON', 'H', '20260821', '008', 'S', NULL, NULL, NULL, 'MTC-2026-0741', 'Plată MTC-2026-0741', 'BKPF', '2000000008', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000009', '000001', '0000401000', NULL, 11313.50, 'RON', 11313.50, 'RON', 'S', '20260904', '009', 'K', '0000700220', NULL, NULL, 'CLF-26-10412', 'Plată CLF-26-10412', 'BKPF', '2000000009', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000009', '000002', '0000512100', NULL, -11313.50, 'RON', -11313.50, 'RON', 'H', '20260904', '009', 'S', NULL, NULL, NULL, 'CLF-26-10412', 'Plată CLF-26-10412', 'BKPF', '2000000009', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000010', '000001', '0000401000', NULL, 3460.60, 'RON', 3460.60, 'RON', 'S', '20260918', '009', 'K', '0000700250', NULL, NULL, 'UMC-F-26-2217', 'Plată UMC-F-26-2217', 'BKPF', '2000000010', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000010', '000002', '0000512100', NULL, -3460.60, 'RON', -3460.60, 'RON', 'H', '20260918', '009', 'S', NULL, NULL, NULL, 'UMC-F-26-2217', 'Plată UMC-F-26-2217', 'BKPF', '2000000010', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000011', '000001', '0000401000', NULL, 17182.00, 'RON', 17182.00, 'RON', 'S', '20260918', '009', 'K', '0000700210', NULL, NULL, 'FTP-2026-118', 'Plată FTP-2026-118', 'BKPF', '2000000011', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000011', '000002', '0000512100', NULL, -17182.00, 'RON', -17182.00, 'RON', 'H', '20260918', '009', 'S', NULL, NULL, NULL, 'FTP-2026-118', 'Plată FTP-2026-118', 'BKPF', '2000000011', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000012', '000001', '0000401000', NULL, 59169.00, 'RON', 59169.00, 'RON', 'S', '20260925', '009', 'K', '0000700210', NULL, NULL, 'FTP-2026-131', 'Plată FTP-2026-131', 'BKPF', '2000000012', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000012', '000002', '0000512100', NULL, -59169.00, 'RON', -59169.00, 'RON', 'H', '20260925', '009', 'S', NULL, NULL, NULL, 'FTP-2026-131', 'Plată FTP-2026-131', 'BKPF', '2000000012', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000001', '000001', '0000601000', 'RO10-110', 6745.54, 'RON', 6745.54, 'RON', 'S', '20260706', '007', 'S', NULL, NULL, 'PF-1101', 'EK26-0311', 'Consum ordin 4000311 lot EK26-0311', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000001', '000002', '0000301000', NULL, -6745.54, 'RON', -6745.54, 'RON', 'H', '20260706', '007', 'S', NULL, NULL, NULL, 'EK26-0311', 'Consum ordin 4000311 lot EK26-0311', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000002', '000001', '0000345000', NULL, 9106.48, 'RON', 9106.48, 'RON', 'S', '20260708', '007', 'S', NULL, NULL, 'PF-1101', 'EK26-0311', 'Predare produs finit lot EK26-0311', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000002', '000002', '0000711000', 'RO10-110', -9106.48, 'RON', -9106.48, 'RON', 'H', '20260708', '007', 'S', NULL, NULL, NULL, 'EK26-0311', 'Predare produs finit lot EK26-0311', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000003', '000001', '0000601000', 'RO10-115', 82.96, 'RON', 82.96, 'RON', 'S', '20260714', '007', 'S', NULL, NULL, 'PF-9101', 'SA26-0031', 'Consum ordin 4100031 lot SA26-0031', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000003', '000002', '0000301000', NULL, -82.96, 'RON', -82.96, 'RON', 'H', '20260714', '007', 'S', NULL, NULL, NULL, 'SA26-0031', 'Consum ordin 4100031 lot SA26-0031', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000004', '000001', '0000345000', NULL, 112.00, 'RON', 112.00, 'RON', 'S', '20260715', '007', 'S', NULL, NULL, 'PF-9101', 'SA26-0031', 'Predare produs finit lot SA26-0031', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000004', '000002', '0000711000', 'RO10-115', -112.00, 'RON', -112.00, 'RON', 'H', '20260715', '007', 'S', NULL, NULL, NULL, 'SA26-0031', 'Predare produs finit lot SA26-0031', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000005', '000001', '0000601000', 'RO10-110', 56627.40, 'RON', 56627.40, 'RON', 'S', '20260721', '007', 'S', NULL, NULL, 'PF-1102', 'EK26-0318', 'Consum ordin 4000318 lot EK26-0318', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000005', '000002', '0000301000', NULL, -56627.40, 'RON', -56627.40, 'RON', 'H', '20260721', '007', 'S', NULL, NULL, NULL, 'EK26-0318', 'Consum ordin 4000318 lot EK26-0318', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000006', '000001', '0000345000', NULL, 76446.99, 'RON', 76446.99, 'RON', 'S', '20260722', '007', 'S', NULL, NULL, 'PF-1102', 'EK26-0318', 'Predare produs finit lot EK26-0318', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000006', '000002', '0000711000', 'RO10-110', -76446.99, 'RON', -76446.99, 'RON', 'H', '20260722', '007', 'S', NULL, NULL, NULL, 'EK26-0318', 'Predare produs finit lot EK26-0318', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000007', '000001', '0000601000', 'RO10-110', 17985.53, 'RON', 17985.53, 'RON', 'S', '20260803', '008', 'S', NULL, NULL, 'PF-1105', 'EK26-0324', 'Consum ordin 4000324 lot EK26-0324', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000007', '000002', '0000301000', NULL, -17985.53, 'RON', -17985.53, 'RON', 'H', '20260803', '008', 'S', NULL, NULL, NULL, 'EK26-0324', 'Consum ordin 4000324 lot EK26-0324', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000008', '000001', '0000345000', NULL, 24280.47, 'RON', 24280.47, 'RON', 'S', '20260805', '008', 'S', NULL, NULL, 'PF-1105', 'EK26-0324', 'Predare produs finit lot EK26-0324', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000008', '000002', '0000711000', 'RO10-110', -24280.47, 'RON', -24280.47, 'RON', 'H', '20260805', '008', 'S', NULL, NULL, NULL, 'EK26-0324', 'Predare produs finit lot EK26-0324', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000009', '000001', '0000601000', 'RO10-115', 82.96, 'RON', 82.96, 'RON', 'S', '20260804', '008', 'S', NULL, NULL, 'PF-9101', 'SA26-0034', 'Consum ordin 4100034 lot SA26-0034', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000009', '000002', '0000301000', NULL, -82.96, 'RON', -82.96, 'RON', 'H', '20260804', '008', 'S', NULL, NULL, NULL, 'SA26-0034', 'Consum ordin 4100034 lot SA26-0034', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000010', '000001', '0000345000', NULL, 112.00, 'RON', 112.00, 'RON', 'S', '20260805', '008', 'S', NULL, NULL, 'PF-9101', 'SA26-0034', 'Predare produs finit lot SA26-0034', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000010', '000002', '0000711000', 'RO10-115', -112.00, 'RON', -112.00, 'RON', 'H', '20260805', '008', 'S', NULL, NULL, NULL, 'SA26-0034', 'Predare produs finit lot SA26-0034', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000011', '000001', '0000601000', 'RO10-110', 6751.51, 'RON', 6751.51, 'RON', 'S', '20260817', '008', 'S', NULL, NULL, 'PF-1101', 'EK26-0329', 'Consum ordin 4000329 lot EK26-0329', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000011', '000002', '0000301000', NULL, -6751.51, 'RON', -6751.51, 'RON', 'H', '20260817', '008', 'S', NULL, NULL, NULL, 'EK26-0329', 'Consum ordin 4000329 lot EK26-0329', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000012', '000001', '0000345000', NULL, 9114.54, 'RON', 9114.54, 'RON', 'S', '20260819', '008', 'S', NULL, NULL, 'PF-1101', 'EK26-0329', 'Predare produs finit lot EK26-0329', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000012', '000002', '0000711000', 'RO10-110', -9114.54, 'RON', -9114.54, 'RON', 'H', '20260819', '008', 'S', NULL, NULL, NULL, 'EK26-0329', 'Predare produs finit lot EK26-0329', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000013', '000001', '0000601000', 'RO10-115', 82.96, 'RON', 82.96, 'RON', 'S', '20260826', '008', 'S', NULL, NULL, 'PF-9101', 'SA26-0037', 'Consum ordin 4100037 lot SA26-0037', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000013', '000002', '0000301000', NULL, -82.96, 'RON', -82.96, 'RON', 'H', '20260826', '008', 'S', NULL, NULL, NULL, 'SA26-0037', 'Consum ordin 4100037 lot SA26-0037', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000014', '000001', '0000345000', NULL, 112.00, 'RON', 112.00, 'RON', 'S', '20260827', '008', 'S', NULL, NULL, 'PF-9101', 'SA26-0037', 'Predare produs finit lot SA26-0037', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000014', '000002', '0000711000', 'RO10-115', -112.00, 'RON', -112.00, 'RON', 'H', '20260827', '008', 'S', NULL, NULL, NULL, 'SA26-0037', 'Predare produs finit lot SA26-0037', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000015', '000001', '0000601000', 'RO10-110', 7500.51, 'RON', 7500.51, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, 'PF-1103', 'EK26-0335', 'Consum ordin 4000335 lot EK26-0335', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000015', '000002', '0000301000', NULL, -7500.51, 'RON', -7500.51, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'EK26-0335', 'Consum ordin 4000335 lot EK26-0335', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000016', '000001', '0000345000', NULL, 10125.69, 'RON', 10125.69, 'RON', 'S', '20260902', '009', 'S', NULL, NULL, 'PF-1103', 'EK26-0335', 'Predare produs finit lot EK26-0335', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000016', '000002', '0000711000', 'RO10-110', -10125.69, 'RON', -10125.69, 'RON', 'H', '20260902', '009', 'S', NULL, NULL, NULL, 'EK26-0335', 'Predare produs finit lot EK26-0335', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000017', '000001', '0000601000', 'RO10-110', 5724.79, 'RON', 5724.79, 'RON', 'S', '20260914', '009', 'S', NULL, NULL, 'PF-1104', 'EK26-0341', 'Consum ordin 4000341 lot EK26-0341', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000017', '000002', '0000301000', NULL, -5724.79, 'RON', -5724.79, 'RON', 'H', '20260914', '009', 'S', NULL, NULL, NULL, 'EK26-0341', 'Consum ordin 4000341 lot EK26-0341', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000018', '000001', '0000345000', NULL, 7728.47, 'RON', 7728.47, 'RON', 'S', '20260916', '009', 'S', NULL, NULL, 'PF-1104', 'EK26-0341', 'Predare produs finit lot EK26-0341', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000018', '000002', '0000711000', 'RO10-110', -7728.47, 'RON', -7728.47, 'RON', 'H', '20260916', '009', 'S', NULL, NULL, NULL, 'EK26-0341', 'Predare produs finit lot EK26-0341', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000019', '000001', '0000601000', 'RO10-115', 82.96, 'RON', 82.96, 'RON', 'S', '20260916', '009', 'S', NULL, NULL, 'PF-9101', 'SA26-0040', 'Consum ordin 4100040 lot SA26-0040', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000019', '000002', '0000301000', NULL, -82.96, 'RON', -82.96, 'RON', 'H', '20260916', '009', 'S', NULL, NULL, NULL, 'SA26-0040', 'Consum ordin 4100040 lot SA26-0040', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000020', '000001', '0000345000', NULL, 112.00, 'RON', 112.00, 'RON', 'S', '20260917', '009', 'S', NULL, NULL, 'PF-9101', 'SA26-0040', 'Predare produs finit lot SA26-0040', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4900000020', '000002', '0000711000', 'RO10-115', -112.00, 'RON', -112.00, 'RON', 'H', '20260917', '009', 'S', NULL, NULL, NULL, 'SA26-0040', 'Predare produs finit lot SA26-0040', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000001', '000001', '0000711000', NULL, 111.99, 'RON', 111.99, 'RON', 'S', '20260727', '007', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0391', 'Confirmări expediție WMS 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000001', '000002', '0000345000', NULL, -111.99, 'RON', -111.99, 'RON', 'H', '20260727', '007', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0391', 'Confirmări expediție WMS 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000001', '000003', '0000711000', NULL, 2276.40, 'RON', 2276.40, 'RON', 'S', '20260727', '007', 'S', NULL, NULL, 'PF-1101', 'EXP-26-0396', 'Confirmări expediție WMS 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000001', '000004', '0000345000', NULL, -2276.40, 'RON', -2276.40, 'RON', 'H', '20260727', '007', 'S', NULL, NULL, 'PF-1101', 'EXP-26-0396', 'Confirmări expediție WMS 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000001', '0000711000', NULL, 111.99, 'RON', 111.99, 'RON', 'S', '20260828', '008', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0403', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000002', '0000345000', NULL, -111.99, 'RON', -111.99, 'RON', 'H', '20260828', '008', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0403', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000003', '0000711000', NULL, 2276.40, 'RON', 2276.40, 'RON', 'S', '20260828', '008', 'S', NULL, NULL, 'PF-1101', 'EXP-26-0407', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000004', '0000345000', NULL, -2276.40, 'RON', -2276.40, 'RON', 'H', '20260828', '008', 'S', NULL, NULL, 'PF-1101', 'EXP-26-0407', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000005', '0000711000', NULL, 7284.24, 'RON', 7284.24, 'RON', 'S', '20260828', '008', 'S', NULL, NULL, 'PF-1105', 'EXP-26-0409', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000006', '0000345000', NULL, -7284.24, 'RON', -7284.24, 'RON', 'H', '20260828', '008', 'S', NULL, NULL, 'PF-1105', 'EXP-26-0409', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000007', '0000711000', NULL, 111.99, 'RON', 111.99, 'RON', 'S', '20260828', '008', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0411', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000002', '000008', '0000345000', NULL, -111.99, 'RON', -111.99, 'RON', 'H', '20260828', '008', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0411', 'Confirmări expediție WMS 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000003', '000001', '0000711000', NULL, 1640.52, 'RON', 1640.52, 'RON', 'S', '20260918', '009', 'S', NULL, NULL, 'PF-1101', 'EXP-26-0418', 'Confirmări expediție WMS 2026-09', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000003', '000002', '0000345000', NULL, -1640.52, 'RON', -1640.52, 'RON', 'H', '20260918', '009', 'S', NULL, NULL, 'PF-1101', 'EXP-26-0418', 'Confirmări expediție WMS 2026-09', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000003', '000003', '0000711000', NULL, 111.99, 'RON', 111.99, 'RON', 'S', '20260918', '009', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0420', 'Confirmări expediție WMS 2026-09', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '4910000003', '000004', '0000345000', NULL, -111.99, 'RON', -111.99, 'RON', 'H', '20260918', '009', 'S', NULL, NULL, 'PF-9101', 'EXP-26-0420', 'Confirmări expediție WMS 2026-09', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000001', '0000512100', NULL, 2150000, 'RON', 2150000, 'RON', 'S', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000002', '0000512400', NULL, 480000, 'RON', 480000, 'RON', 'S', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000003', '0000301000', NULL, 120000, 'RON', 120000, 'RON', 'S', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000004', '0000345000', NULL, 210000, 'RON', 210000, 'RON', 'S', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000005', '0000401000', NULL, -95000, 'RON', -95000, 'RON', 'H', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000006', '0000411100', NULL, 140000, 'RON', 140000, 'RON', 'S', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000007', '0000101200', NULL, -1000000, 'RON', -1000000, 'RON', 'H', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '0000000000', '000008', '0000117000', NULL, -2005000, 'RON', -2005000, 'RON', 'H', '20260101', '000', 'S', NULL, NULL, NULL, NULL, 'Report sold 2025', 'GLYEC', NULL, NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000013', '000001', '0000421000', NULL, 237798.55, 'RON', 237798.55, 'RON', 'S', '20260810', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Plată salarii nete PR-RO01-2026-07', 'BKPF', '2000000013', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000013', '000002', '0000512100', NULL, -237798.55, 'RON', -237798.55, 'RON', 'H', '20260810', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Plată salarii nete PR-RO01-2026-07', 'BKPF', '2000000013', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000014', '000001', '0000431000', NULL, 142272.64, 'RON', 142272.64, 'RON', 'S', '20260825', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Plată contribuții și impozit ANAF PR-RO01-2026-07', 'BKPF', '2000000014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000014', '000002', '0000444000', NULL, 26422.06, 'RON', 26422.06, 'RON', 'S', '20260825', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Plată contribuții și impozit ANAF PR-RO01-2026-07', 'BKPF', '2000000014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000014', '000003', '0000436000', NULL, 9146.10, 'RON', 9146.10, 'RON', 'S', '20260825', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Plată contribuții și impozit ANAF PR-RO01-2026-07', 'BKPF', '2000000014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000014', '000004', '0000512100', NULL, -177840.80, 'RON', -177840.80, 'RON', 'H', '20260825', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Plată contribuții și impozit ANAF PR-RO01-2026-07', 'BKPF', '2000000014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000001', '000001', '0000641000', NULL, 406493.25, 'RON', 406493.25, 'RON', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000001', '000002', '0000646000', NULL, 9146.10, 'RON', 9146.10, 'RON', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000001', '000003', '0000421000', NULL, -237798.55, 'RON', -237798.55, 'RON', 'H', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000001', '000004', '0000431000', NULL, -142272.64, 'RON', -142272.64, 'RON', 'H', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000001', '000005', '0000444000', NULL, -26422.06, 'RON', -26422.06, 'RON', 'H', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000001', '000006', '0000436000', NULL, -9146.10, 'RON', -9146.10, 'RON', 'H', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-RO01-2026-07', 'Stat de plată Workday PR-RO01-2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000015', '000001', '0000421000', NULL, 233073.85, 'RON', 233073.85, 'RON', 'S', '20260910', '009', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Plată salarii nete PR-RO01-2026-08', 'BKPF', '2000000015', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000015', '000002', '0000512100', NULL, -233073.85, 'RON', -233073.85, 'RON', 'H', '20260910', '009', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Plată salarii nete PR-RO01-2026-08', 'BKPF', '2000000015', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000016', '000001', '0000431000', NULL, 139445.90, 'RON', 139445.90, 'RON', 'S', '20260925', '009', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Plată contribuții și impozit ANAF PR-RO01-2026-08', 'BKPF', '2000000016', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000016', '000002', '0000444000', NULL, 25897.10, 'RON', 25897.10, 'RON', 'S', '20260925', '009', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Plată contribuții și impozit ANAF PR-RO01-2026-08', 'BKPF', '2000000016', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000016', '000003', '0000436000', NULL, 8964.38, 'RON', 8964.38, 'RON', 'S', '20260925', '009', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Plată contribuții și impozit ANAF PR-RO01-2026-08', 'BKPF', '2000000016', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '2000000016', '000004', '0000512100', NULL, -174307.38, 'RON', -174307.38, 'RON', 'H', '20260925', '009', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Plată contribuții și impozit ANAF PR-RO01-2026-08', 'BKPF', '2000000016', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000002', '000001', '0000641000', NULL, 398416.85, 'RON', 398416.85, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000002', '000002', '0000646000', NULL, 8964.38, 'RON', 8964.38, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000002', '000003', '0000421000', NULL, -233073.85, 'RON', -233073.85, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000002', '000004', '0000431000', NULL, -139445.90, 'RON', -139445.90, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000002', '000005', '0000444000', NULL, -25897.10, 'RON', -25897.10, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000002', '000006', '0000436000', NULL, -8964.38, 'RON', -8964.38, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-RO01-2026-08', 'Stat de plată Workday PR-RO01-2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000003', '000001', '0000625000', NULL, 5354.10, 'RON', 5354.10, 'RON', 'S', '20260728', '007', 'S', NULL, NULL, NULL, 'CONCUR-2026-07', 'Decont cheltuieli Concur 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000003', '000002', '0000428200', NULL, -5354.10, 'RON', -5354.10, 'RON', 'H', '20260728', '007', 'S', NULL, NULL, NULL, 'CONCUR-2026-07', 'Decont cheltuieli Concur 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000004', '000001', '0000625000', NULL, 5354.43, 'RON', 5354.43, 'RON', 'S', '20260828', '008', 'S', NULL, NULL, NULL, 'CONCUR-2026-08', 'Decont cheltuieli Concur 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000004', '000002', '0000428200', NULL, -5354.43, 'RON', -5354.43, 'RON', 'H', '20260828', '008', 'S', NULL, NULL, NULL, 'CONCUR-2026-08', 'Decont cheltuieli Concur 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000005', '000001', '0000611000', 'RO10-150', 8420.55, 'RON', 8420.55, 'RON', 'S', '20260727', '007', 'S', NULL, NULL, NULL, 'MX-2026-07', 'Costuri ordine de lucru Maximo 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000005', '000002', '0000408000', NULL, -8420.55, 'RON', -8420.55, 'RON', 'H', '20260727', '007', 'S', NULL, NULL, NULL, 'MX-2026-07', 'Costuri ordine de lucru Maximo 2026-07', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000006', '000001', '0000611000', 'RO10-150', 12960.10, 'RON', 12960.10, 'RON', 'S', '20260827', '008', 'S', NULL, NULL, NULL, 'MX-2026-08', 'Costuri ordine de lucru Maximo 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000006', '000002', '0000408000', NULL, -12960.10, 'RON', -12960.10, 'RON', 'H', '20260827', '008', 'S', NULL, NULL, NULL, 'MX-2026-08', 'Costuri ordine de lucru Maximo 2026-08', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000007', '000001', '0000611000', 'RO10-150', 9875.40, 'RON', 9875.40, 'RON', 'S', '20260927', '009', 'S', NULL, NULL, NULL, 'MX-2026-09', 'Costuri ordine de lucru Maximo 2026-09', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1000000007', '000002', '0000408000', NULL, -9875.40, 'RON', -9875.40, 'RON', 'H', '20260927', '009', 'S', NULL, NULL, NULL, 'MX-2026-09', 'Costuri ordine de lucru Maximo 2026-09', 'IDOC', '0000000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1900000011', '000001', '0000628000', 'RO10-210', 72000.00, 'RON', 72000.00, 'RON', 'S', '20260731', '007', 'S', NULL, NULL, NULL, NULL, 'Accrual audit statutar 2026 - onorariu auditor fin', 'BKPF', '1900000011', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1900000011', '000002', '0000408000', NULL, -72000.00, 'RON', -72000.00, 'RON', 'H', '20260731', '007', 'S', NULL, NULL, NULL, NULL, 'Accrual audit statutar 2026 - onorariu auditor fin', 'BKPF', '1900000011', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1900000014', '000001', '0000641000', 'RO10-220', 118400.00, 'RON', 118400.00, 'RON', 'S', '20260831', '008', 'S', NULL, NULL, NULL, NULL, 'Provizion concedii de odihnă neefectuate la 31.08.', 'BKPF', '1900000014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1900000014', '000002', '0000151800', NULL, -118400.00, 'RON', -118400.00, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, NULL, 'Provizion concedii de odihnă neefectuate la 31.08.', 'BKPF', '1900000014', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000001', '000001', '0000411100', NULL, 2719.50, 'RON', 2719.50, 'RON', 'S', '20260720', '007', 'D', NULL, '0000800110', NULL, 'EKG26-000531', 'Factura EKG26-000531 comanda 120031', 'VBRK', '90004113', '20260918', NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000001', '000002', '0000701000', NULL, -2450.00, 'RON', -2450.00, 'RON', 'H', '20260720', '007', 'S', NULL, NULL, 'PF-9101', 'EKG26-000531', 'Factura EKG26-000531 comanda 120031', 'VBRK', '90004113', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000001', '000003', '0000442700', NULL, -269.50, 'RON', -269.50, 'RON', 'H', '20260720', '007', 'S', NULL, NULL, NULL, 'EKG26-000531', 'Factura EKG26-000531 comanda 120031', 'VBRK', '90004113', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000002', '000001', '0000411100', NULL, 2719.50, 'RON', 2719.50, 'RON', 'S', '20260810', '008', 'D', NULL, '0000800110', NULL, 'EKG26-000534', 'Factura EKG26-000534 comanda 120034', 'VBRK', '90004126', '20261009', NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000002', '000002', '0000701000', NULL, -2450.00, 'RON', -2450.00, 'RON', 'H', '20260810', '008', 'S', NULL, NULL, 'PF-9101', 'EKG26-000534', 'Factura EKG26-000534 comanda 120034', 'VBRK', '90004126', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000002', '000003', '0000442700', NULL, -269.50, 'RON', -269.50, 'RON', 'H', '20260810', '008', 'S', NULL, NULL, NULL, 'EKG26-000534', 'Factura EKG26-000534 comanda 120034', 'VBRK', '90004126', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000003', '000001', '0000411100', NULL, 2719.50, 'RON', 2719.50, 'RON', 'S', '20260831', '008', 'D', NULL, '0000800120', NULL, 'EKG26-000537', 'Factura EKG26-000537 comanda 120037', 'VBRK', '90004139', '20261030', NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000003', '000002', '0000701000', NULL, -2450.00, 'RON', -2450.00, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, 'PF-9101', 'EKG26-000537', 'Factura EKG26-000537 comanda 120037', 'VBRK', '90004139', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000003', '000003', '0000442700', NULL, -269.50, 'RON', -269.50, 'RON', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'EKG26-000537', 'Factura EKG26-000537 comanda 120037', 'VBRK', '90004139', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000004', '000001', '0000411100', NULL, 2719.50, 'RON', 2719.50, 'RON', 'S', '20260921', '009', 'D', NULL, '0000800130', NULL, 'EKG26-000540', 'Factura EKG26-000540 comanda 120040', 'VBRK', '90004152', '20261120', NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000004', '000002', '0000701000', NULL, -2450.00, 'RON', -2450.00, 'RON', 'H', '20260921', '009', 'S', NULL, NULL, 'PF-9101', 'EKG26-000540', 'Factura EKG26-000540 comanda 120040', 'VBRK', '90004152', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000004', '000003', '0000442700', NULL, -269.50, 'RON', -269.50, 'RON', 'H', '20260921', '009', 'S', NULL, NULL, NULL, 'EKG26-000540', 'Factura EKG26-000540 comanda 120040', 'VBRK', '90004152', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1400000001', '000001', '0000512100', NULL, 21312.00, 'RON', 21312.00, 'RON', 'S', '20260905', '009', 'S', NULL, NULL, NULL, 'EKG26-000596', 'Încasare EKG26-000596', 'BKPF', '1400000001', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1400000001', '000002', '0000411100', NULL, -21312.00, 'RON', -21312.00, 'RON', 'H', '20260905', '009', 'D', NULL, '0000800010', NULL, 'EKG26-000596', 'Încasare EKG26-000596', 'BKPF', '1400000001', NULL, '1400000001', '20260905'),
('300', '0L', 'RO01', '2026', '9400000005', '000001', '0000411100', NULL, 21312.00, 'RON', 21312.00, 'RON', 'S', '20260727', '007', 'D', NULL, '0000800010', NULL, 'EKG26-000596', 'Factura EKG26-000596 comanda 110396', 'VBRK', '90004165', '20260910', '1400000001', '20260905'),
('300', '0L', 'RO01', '2026', '9400000005', '000002', '0000701000', NULL, -19200.00, 'RON', -19200.00, 'RON', 'H', '20260727', '007', 'S', NULL, NULL, 'PF-1101', 'EKG26-000596', 'Factura EKG26-000596 comanda 110396', 'VBRK', '90004165', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000005', '000003', '0000442700', NULL, -2112.00, 'RON', -2112.00, 'RON', 'H', '20260727', '007', 'S', NULL, NULL, NULL, 'EKG26-000596', 'Factura EKG26-000596 comanda 110396', 'VBRK', '90004165', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1400000002', '000001', '0000512400', NULL, 18936.29, 'RON', 18936.29, 'EUR', 'S', '20260911', '009', 'S', NULL, NULL, NULL, 'EKG26-000607', 'Încasare EKG26-000607', 'BKPF', '1400000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '1400000002', '000002', '0000411100', NULL, -18909.13, 'RON', -3720.00, 'EUR', 'H', '20260911', '009', 'D', NULL, '0000800220', NULL, 'EKG26-000607', 'Încasare EKG26-000607', 'BKPF', '1400000002', NULL, '1400000002', '20260911'),
('300', '0L', 'RO01', '2026', '1400000002', '000003', '0000765000', NULL, -27.16, 'RON', -27.16, 'EUR', 'H', '20260911', '009', 'S', NULL, NULL, NULL, 'EKG26-000607', 'Încasare EKG26-000607', 'BKPF', '1400000002', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000006', '000001', '0000411100', NULL, 18909.13, 'RON', 3720.00, 'EUR', 'S', '20260813', '008', 'D', NULL, '0000800220', NULL, 'EKG26-000607', 'Factura EKG26-000607 comanda 110407', 'VBRK', '90004178', '20260927', '1400000002', '20260911'),
('300', '0L', 'RO01', '2026', '9400000006', '000002', '0000701000', NULL, -18909.13, 'RON', -3720.00, 'EUR', 'H', '20260813', '008', 'S', NULL, NULL, 'PF-1101', 'EKG26-000607', 'Factura EKG26-000607 comanda 110407', 'VBRK', '90004178', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000007', '000001', '0000411100', NULL, 38628.00, 'RON', 38628.00, 'RON', 'S', '20260824', '008', 'D', NULL, '0000800020', NULL, 'EKG26-000609', 'Factura EKG26-000609 comanda 110409', 'VBRK', '90004191', '20261008', NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000007', '000002', '0000701000', NULL, -34800.00, 'RON', -34800.00, 'RON', 'H', '20260824', '008', 'S', NULL, NULL, 'PF-1105', 'EKG26-000609', 'Factura EKG26-000609 comanda 110409', 'VBRK', '90004191', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000007', '000003', '0000442700', NULL, -3828.00, 'RON', -3828.00, 'RON', 'H', '20260824', '008', 'S', NULL, NULL, NULL, 'EKG26-000609', 'Factura EKG26-000609 comanda 110409', 'VBRK', '90004191', NULL, NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000008', '000001', '0000411100', NULL, 17042.66, 'RON', 3348.00, 'EUR', 'S', '20260916', '009', 'D', NULL, '0000800220', NULL, 'EKG26-000618', 'Factura EKG26-000618 comanda 110418', 'VBRK', '90004204', '20261031', NULL, NULL),
('300', '0L', 'RO01', '2026', '9400000008', '000002', '0000701000', NULL, -17042.66, 'RON', -3348.00, 'EUR', 'H', '20260916', '009', 'S', NULL, NULL, 'PF-1101', 'EKG26-000618', 'Factura EKG26-000618 comanda 110418', 'VBRK', '90004204', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.vbkpf (
  mandt varchar(3) NOT NULL,
  bukrs varchar(4) NOT NULL,
  belnr varchar(10) NOT NULL,
  gjahr varchar(4) NOT NULL,
  blart varchar(2) NOT NULL,
  budat varchar(8) NOT NULL,
  monat varchar(2) NOT NULL,
  usnam varchar(12) NOT NULL,
  cpudt varchar(8) NOT NULL,
  cputm varchar(6) NOT NULL,
  bktxt varchar(60),
  bstat varchar(1) NOT NULL,
  CONSTRAINT vbkpf_pk PRIMARY KEY (mandt, bukrs, belnr, gjahr)
);
COMMENT ON TABLE sap_s4hana.vbkpf IS 'Parked document headers (landed with history: rows are retained after posting; bstat V = still parked).';

INSERT INTO sap_s4hana.vbkpf (mandt, bukrs, belnr, gjahr, blart, budat, monat, usnam, cpudt, cputm, bktxt, bstat) VALUES
('300', 'RO01', '1900000011', '2026', 'SA', '20260731', '07', 'MAPOSTOL', '20260805', '204800', 'Accrual audit statutar 2026 - onorariu auditor financiar', ' '),
('300', 'RO01', '1900000014', '2026', 'SA', '20260831', '08', 'SFLORESCU', '20260902', '101500', 'Provizion concedii de odihnă neefectuate la 31.08.2026', ' '),
('300', 'RO01', '1900000019', '2026', 'SA', '20260930', '09', 'SFLORESCU', '20260929', '142000', 'Ajustare depreciere lot EK26-0335 (certificare amânată)', 'V'),
('300', 'RO01', '1900000021', '2026', 'SA', '20260930', '09', 'MAPOSTOL', '20260930', '093500', 'Reevaluare datorii furnizori în EUR la cursul BNR 30.09.2026', 'V')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.vbsegs (
  mandt varchar(3) NOT NULL,
  bukrs varchar(4) NOT NULL,
  belnr varchar(10) NOT NULL,
  gjahr varchar(4) NOT NULL,
  buzei varchar(3) NOT NULL,
  saknr varchar(10) NOT NULL,
  shkzg varchar(1) NOT NULL,
  dmbtr numeric(23,2) NOT NULL,
  kostl varchar(20),
  CONSTRAINT vbsegs_pk PRIMARY KEY (mandt, bukrs, belnr, gjahr, buzei)
);
COMMENT ON TABLE sap_s4hana.vbsegs IS 'Parked G/L account line items.';

INSERT INTO sap_s4hana.vbsegs (mandt, bukrs, belnr, gjahr, buzei, saknr, shkzg, dmbtr, kostl) VALUES
('300', 'RO01', '1900000011', '2026', '001', '0000628000', 'S', 72000.00, 'RO10-210'),
('300', 'RO01', '1900000011', '2026', '002', '0000408000', 'H', 72000.00, NULL),
('300', 'RO01', '1900000014', '2026', '001', '0000641000', 'S', 118400.00, 'RO10-220'),
('300', 'RO01', '1900000014', '2026', '002', '0000151800', 'H', 118400.00, NULL),
('300', 'RO01', '1900000019', '2026', '001', '0000681400', 'S', 96300.00, 'RO10-110'),
('300', 'RO01', '1900000019', '2026', '002', '0000394500', 'H', 96300.00, NULL),
('300', 'RO01', '1900000021', '2026', '001', '0000665000', 'S', 58200.00, NULL),
('300', 'RO01', '1900000021', '2026', '002', '0000401000', 'H', 58200.00, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.swwwihead (
  wi_id          bigint NOT NULL,
  wi_type        varchar(1) NOT NULL,
  wi_rh_task     varchar(14) NOT NULL,
  wi_text        varchar(120),
  wi_stat        varchar(12) NOT NULL,
  wi_cd          varchar(8) NOT NULL,
  wi_ct          varchar(6) NOT NULL,
  wi_aed         varchar(8),
  wi_aet         varchar(6),
  wi_aagent      varchar(12),
  wi_result      varchar(20),
  wi_result_note text,
  CONSTRAINT swwwihead_pk PRIMARY KEY (wi_id)
);
COMMENT ON TABLE sap_s4hana.swwwihead IS 'Workflow work items of the parked journal approval step; decision and note flattened from the container.';

INSERT INTO sap_s4hana.swwwihead (wi_id, wi_type, wi_rh_task, wi_text, wi_stat, wi_cd, wi_ct, wi_aed, wi_aet, wi_aagent, wi_result, wi_result_note) VALUES
(3300217, 'W', 'TS78500112', 'Aprobare document contabil preînregistrat 1900000011 (72000.00 RON)', 'COMPLETED', '20260805', '204800', '20260805', '205100', 'GRADU', 'APPROVE', NULL),
(3300224, 'W', 'TS78500112', 'Aprobare document contabil preînregistrat 1900000014 (118400.00 RON)', 'COMPLETED', '20260902', '101500', '20260902', '164000', 'MAPOSTOL', 'RETURN', 'Atașați calculul pe angajați exportat din Workday.'),
(3300231, 'W', 'TS78500112', 'Aprobare document contabil preînregistrat 1900000014 (118400.00 RON)', 'COMPLETED', '20260902', '101500', '20260903', '110500', 'GRADU', 'APPROVE', 'Calcul Workday atașat.'),
(3300238, 'W', 'TS78500112', 'Aprobare document contabil preînregistrat 1900000019 (96300.00 RON)', 'COMPLETED', '20260929', '142000', '20260929', '170200', 'GRADU', 'REJECT', 'Așteptați concluzia investigației DEV-RO-000236 înainte de ajustare.'),
(3300245, 'W', 'TS78500112', 'Aprobare document contabil preînregistrat 1900000021 (58200.00 RON)', 'READY', '20260930', '093500', NULL, NULL, NULL, NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.sww_wi2obj (
  wi_id  bigint NOT NULL,
  catid  varchar(2) NOT NULL,
  typeid varchar(32) NOT NULL,
  instid varchar(70) NOT NULL,
  CONSTRAINT sww_wi2obj_pk PRIMARY KEY (wi_id, catid, typeid, instid)
);
COMMENT ON TABLE sap_s4hana.sww_wi2obj IS 'Work item to business object links (FIPP = parked document, key = company code + document number + year).';

INSERT INTO sap_s4hana.sww_wi2obj (wi_id, catid, typeid, instid) VALUES
(3300217, 'BO', 'FIPP', 'RO0119000000112026'),
(3300224, 'BO', 'FIPP', 'RO0119000000142026'),
(3300231, 'BO', 'FIPP', 'RO0119000000142026'),
(3300238, 'BO', 'FIPP', 'RO0119000000192026'),
(3300245, 'BO', 'FIPP', 'RO0119000000212026')
ON CONFLICT DO NOTHING;

-- EKG Z tables filled from the data sharing hub (subscription apply scripts buc_sap_s4hana__*).
CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_cnq_rpt (
  mandt       varchar(3) NOT NULL,
  report_id   varchar(20) NOT NULL,
  pseudo_id   varchar(40),
  subm_date   varchar(8),
  subm_time   varchar(6),
  wrbtr       numeric(15,2) NOT NULL,
  waers       varchar(5) NOT NULL,
  rpt_status  varchar(20) NOT NULL,
  docnum      varchar(16),
  recon_stat  varchar(1) NOT NULL,
  aedat       varchar(8) NOT NULL,
  CONSTRAINT zekg_cnq_rpt_pk PRIMARY KEY (mandt, report_id)
);
COMMENT ON TABLE sap_s4hana.zekg_cnq_rpt IS 'EKG: Concur expense reports for reconciliation against the monthly Concur accounting IDoc (docnum of the posted CONCUR_EKG IDoc; recon_stat P posted, O open = approved but not yet in a posted IDoc, N not approved).';

CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_qm_lims (
  mandt       varchar(3) NOT NULL,
  prueflos    varchar(12) NOT NULL,
  lims_result varchar(40) NOT NULL,
  verwmerkm   varchar(40) NOT NULL,
  messwert    varchar(60),
  meinh       varchar(20),
  toleranzun  varchar(60),
  toleranzob  varchar(60),
  bewertg     varchar(1) NOT NULL,
  pruefdatuv  varchar(8),
  pruefzeit   varchar(6),
  pruefer     varchar(12),
  CONSTRAINT zekg_qm_lims_pk PRIMARY KEY (mandt, prueflos, lims_result)
);
COMMENT ON TABLE sap_s4hana.zekg_qm_lims IS 'EKG: LabWare results recorded against the goods-receipt inspection lot (bewertg A accepted / R rejected), referenced by the usage decision (qave.zz_lims_result).';

CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_pat_link (
  mandt       varchar(3) NOT NULL,
  pseudo_id   varchar(40) NOT NULL,
  treat_order varchar(20),
  matnr       varchar(40),
  issued_date varchar(8),
  issued_time varchar(6),
  pat_params  varchar(255),
  aufnr       varchar(12),
  CONSTRAINT zekg_pat_link_pk PRIMARY KEY (mandt, pseudo_id)
);
COMMENT ON TABLE sap_s4hana.zekg_pat_link IS 'EKG: patient pseudonyms issued for named-patient treatment orders, with the parameters the process order must carry (aufk.zz_patient_params) and the process order once created.';

CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_pay_anom (
  mandt       varchar(3) NOT NULL,
  anomaly_id  varchar(20) NOT NULL,
  lifnr       varchar(10),
  anom_type   varchar(40) NOT NULL,
  severity    varchar(20),
  anom_status varchar(30) NOT NULL,
  det_date    varchar(8),
  det_time    varchar(6),
  descr       text,
  CONSTRAINT zekg_pay_anom_pk PRIMARY KEY (mandt, anomaly_id)
);
COMMENT ON TABLE sap_s4hana.zekg_pay_anom IS 'EKG: payment anomaly findings raised against a vendor, worked by accounts payable before the next payment run; a confirmed finding leads to a screening entry (zekg_vend_scrn.anomaly_ref).';

CREATE TABLE IF NOT EXISTS sap_s4hana.zekg_ther_evt (
  mandt       varchar(3) NOT NULL,
  charg       varchar(10) NOT NULL,
  evt_type    varchar(20) NOT NULL,
  evt_date    varchar(8) NOT NULL,
  evt_time    varchar(6) NOT NULL,
  pseudo_id   varchar(40),
  treat_order varchar(20),
  location    varchar(120),
  CONSTRAINT zekg_ther_evt_pk PRIMARY KEY (mandt, charg, evt_type, evt_date, evt_time)
);
COMMENT ON TABLE sap_s4hana.zekg_ther_evt IS 'EKG: delivery and administration confirmations of named-patient therapies; a confirmed administration releases the treatment order for billing (vbrk fkart ZNPF).';

GRANT USAGE ON SCHEMA sap_s4hana TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA sap_s4hana TO egeria_user, airflow_user;
