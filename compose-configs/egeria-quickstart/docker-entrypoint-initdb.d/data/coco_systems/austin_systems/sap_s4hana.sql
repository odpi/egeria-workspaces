-- system-qualified-name: SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923
-- SAP S/4HANA - Austin.  The Austin ERP (client 100, company code US01, plant US10): production planning, quality
-- management usage decisions, billing, the universal journal with its inbound IDoc feeds, parked journals with their
-- approval workflow, and the payment run.  Its tables feed Personalised Manufacturing Schedule, Material Quarantine
-- Dispositions (usage decisions), Treatment Invoices (revenue recognition), Subledger Postings, Manual Journal
-- Approvals, Supplier Payments (payment instructions) and General Ledger Balances.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS sap_s4hana;
COMMENT ON SCHEMA sap_s4hana IS 'SAP S/4HANA (Austin): SAP tables as replicated by SAP SLT (lower-case names; DATS/TIMS kept as YYYYMMDD/HHMMSS text).';

CREATE TABLE IF NOT EXISTS sap_s4hana.aufk (
  mandt                varchar(3) NOT NULL,
  aufnr                varchar(12) NOT NULL,
  auart                varchar(4) NOT NULL,
  werks                varchar(4) NOT NULL,
  bukrs                varchar(4) NOT NULL,
  ktext                varchar(40),
  erdat                varchar(8) NOT NULL,
  objnr                varchar(22) NOT NULL,
  zz_gmp_plan_order    varchar(20),
  zz_treatment_order   varchar(20),
  zz_patient_pseudonym varchar(40),
  zz_patient_params    varchar(255),
  CONSTRAINT aufk_pk PRIMARY KEY (mandt, aufnr)
);
COMMENT ON TABLE sap_s4hana.aufk IS 'Order master (ZP01 process order for Coco planning orders and Austin batches; ZPAT patient-specific order with the portal order and patient pseudonym).';

INSERT INTO sap_s4hana.aufk (mandt, aufnr, auart, werks, bukrs, ktext, erdat, objnr, zz_gmp_plan_order, zz_treatment_order, zz_patient_pseudonym, zz_patient_params) VALUES
('100', '1000412', 'ZP01', 'US10', 'US01', '3000 batch A26-3000-0141', '20260727', 'OR000001000412', 'GMP-PO-26-0412', NULL, NULL, NULL),
('100', '1000431', 'ZP01', 'US10', 'US01', '2050 batch A26-2050-0087', '20260810', 'OR000001000431', 'GMP-PO-26-0431', NULL, NULL, NULL),
('100', '1000448', 'ZP01', 'US10', 'US01', '9000 batch A26-9000-0019', '20260825', 'OR000001000448', 'GMP-PO-26-0448', NULL, NULL, NULL),
('100', '1000457', 'ZP01', 'US10', 'US01', '3000 batch A26-3000-0142', '20260831', 'OR000001000457', 'GMP-PO-26-0457', NULL, NULL, NULL),
('100', '1000466', 'ZP01', 'US10', 'US01', '2050 batch A26-2050-0088', '20260921', 'OR000001000466', 'GMP-PO-26-0466', NULL, NULL, NULL),
('100', '1000402', 'ZP01', 'US10', 'US01', 'AU-4410 batch A26-4410-0052', '20260713', 'OR000001000402', NULL, NULL, NULL, NULL),
('100', '1000452', 'ZP01', 'US10', 'US01', 'AU-4630 batch A26-4630-0017', '20260907', 'OR000001000452', NULL, NULL, NULL, NULL),
('100', '1000481', 'ZPAT', 'US10', 'US01', 'AU-7710 batch A26-7710-P015', '20260706', 'OR000001000481', NULL, 'TO-26-0015', 'PP-FA1AF588F5B4', 'Target dose 20 x 10^6 viable cells; weight 83 kg; apheresis at UTSW'),
('100', '1000482', 'ZPAT', 'US10', 'US01', 'AU-7710 batch A26-7710-P016', '20260803', 'OR000001000482', NULL, 'TO-26-0016', 'PP-CCD4B098EAFF', 'Target dose 20 x 10^6 viable cells; weight 93 kg; apheresis at UTSW'),
('100', '1000483', 'ZPAT', 'US10', 'US01', 'AU-7710 batch A26-7710-P017', '20260825', 'OR000001000483', NULL, 'TO-26-0017', 'PP-08BA47CBA05B', 'Target dose 20 x 10^6 viable cells; weight 81 kg; apheresis at DSMC'),
('100', '1000484', 'ZPAT', 'US10', 'US01', 'AU-7710 batch A26-7710-P018', '20260908', 'OR000001000484', NULL, 'TO-26-0018', 'PP-06CCD43B6C3E', 'Target dose 20 x 10^6 viable cells; weight 90 kg; apheresis at DSMC'),
('100', '1000479', 'ZPAT', 'US10', 'US01', 'AU-7710 batch A26-7710-P014', '20260608', 'OR000001000479', NULL, 'TO-26-0014', 'PP-3349A011D084', 'Target dose 20 x 10^6 viable cells; weight 85 kg; apheresis at DSMC'),
('100', '1000491', 'ZPAT', 'US10', 'US01', 'AU-7710 batch A26-7710-P019', '20260925', 'OR000001000491', NULL, 'TO-26-0019', 'PP-585B1C61A454', 'Target dose 20 x 10^6 viable cells; weight 84 kg; apheresis at BSW')
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
('100', '1000412', '20260803', '060000', '20260805', '180000', '20260803', '060000', '20260805', '180000', '3000'),
('100', '1000431', '20260817', '060000', '20260819', '140000', '20260817', '060000', '20260819', '140000', '2050'),
('100', '1000448', '20260901', '070000', '20260902', '190000', '20260901', '070000', '20260902', '190000', '9000'),
('100', '1000457', '20260907', '060000', '20260909', '180000', '20260907', '060000', '20260909', '180000', '3000'),
('100', '1000466', '20260928', '060000', '20260930', '180000', '20260928', '060000', NULL, NULL, '2050'),
('100', '1000402', '20260720', '070000', '20260721', '173000', '20260720', '070000', '20260721', '173000', 'AU-4410'),
('100', '1000452', '20260914', '070000', '20260915', '160000', '20260914', '070000', '20260915', '160000', 'AU-4630'),
('100', '1000481', '20260713', '070000', '20260724', '160000', '20260713', '070000', '20260724', '160000', 'AU-7710'),
('100', '1000482', '20260810', '070000', '20260821', '153000', '20260810', '070000', '20260821', '153000', 'AU-7710'),
('100', '1000483', '20260901', '070000', '20260912', '140000', '20260901', '070000', '20260912', '140000', 'AU-7710'),
('100', '1000484', '20260915', '070000', '20260926', '150000', '20260915', '070000', '20260926', '150000', 'AU-7710'),
('100', '1000479', '20260615', '070000', '20260626', '150000', NULL, NULL, NULL, NULL, 'AU-7710'),
('100', '1000491', '20261002', '070000', '20261013', '150000', NULL, NULL, NULL, NULL, 'AU-7710')
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
('100', '1000412', '0001', '3000', 'A26-3000-0141', 120000, 'ST', 'US10'),
('100', '1000431', '0001', '2050', 'A26-2050-0087', 90000, 'ST', 'US10'),
('100', '1000448', '0001', '9000', 'A26-9000-0019', 2500, 'ST', 'US10'),
('100', '1000457', '0001', '3000', 'A26-3000-0142', 120000, 'ST', 'US10'),
('100', '1000466', '0001', '2050', 'A26-2050-0088', 90000, 'ST', 'US10'),
('100', '1000402', '0001', 'AU-4410', 'A26-4410-0052', 3200, 'ST', 'US10'),
('100', '1000452', '0001', 'AU-4630', 'A26-4630-0017', 4000, 'ST', 'US10'),
('100', '1000481', '0001', 'AU-7710', 'A26-7710-P015', 1, 'EA', 'US10'),
('100', '1000482', '0001', 'AU-7710', 'A26-7710-P016', 1, 'EA', 'US10'),
('100', '1000483', '0001', 'AU-7710', 'A26-7710-P017', 1, 'EA', 'US10'),
('100', '1000484', '0001', 'AU-7710', 'A26-7710-P018', 1, 'EA', 'US10'),
('100', '1000479', '0001', 'AU-7710', 'A26-7710-P014', 1, 'EA', 'US10'),
('100', '1000491', '0001', 'AU-7710', 'A26-7710-P019', 1, 'EA', 'US10')
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
('100', 'OR000001000412', 'I0002', NULL),
('100', 'OR000001000412', 'I0009', NULL),
('100', 'OR000001000412', 'I0045', NULL),
('100', 'OR000001000431', 'I0002', NULL),
('100', 'OR000001000431', 'I0009', NULL),
('100', 'OR000001000431', 'I0045', NULL),
('100', 'OR000001000448', 'I0002', NULL),
('100', 'OR000001000448', 'I0009', NULL),
('100', 'OR000001000448', 'I0045', NULL),
('100', 'OR000001000457', 'I0002', NULL),
('100', 'OR000001000457', 'I0009', NULL),
('100', 'OR000001000457', 'I0045', NULL),
('100', 'OR000001000466', 'I0002', NULL),
('100', 'OR000001000402', 'I0002', NULL),
('100', 'OR000001000402', 'I0009', NULL),
('100', 'OR000001000402', 'I0045', NULL),
('100', 'OR000001000452', 'I0002', NULL),
('100', 'OR000001000452', 'I0009', NULL),
('100', 'OR000001000452', 'I0045', NULL),
('100', 'OR000001000481', 'I0002', NULL),
('100', 'OR000001000481', 'I0009', NULL),
('100', 'OR000001000481', 'I0045', NULL),
('100', 'OR000001000482', 'I0002', NULL),
('100', 'OR000001000482', 'I0009', NULL),
('100', 'OR000001000482', 'I0045', NULL),
('100', 'OR000001000483', 'I0002', NULL),
('100', 'OR000001000483', 'I0009', NULL),
('100', 'OR000001000483', 'I0045', NULL),
('100', 'OR000001000484', 'I0002', NULL),
('100', 'OR000001000484', 'I0009', NULL),
('100', 'OR000001000484', 'I0045', NULL),
('100', 'OR000001000479', 'I0001', NULL),
('100', 'OR000001000479', 'I0076', NULL),
('100', 'OR000001000491', 'I0001', NULL)
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
COMMENT ON TABLE sap_s4hana.likp IS 'Inbound deliveries of type ZPMI (patient material): lifex = courier shipment ID, wbstk C = goods received; arrival date/time UTC.';

INSERT INTO sap_s4hana.likp (mandt, vbeln, lfart, lifex, lfdat, lfuhr, lifnr, zz_patient_pseudonym, zz_arrival_cond, zz_viable_hours, wbstk) VALUES
('100', '1800004411', 'ZPMI', 'PM-26-0015', '20260711', '154000', '0000100110', 'PP-FA1AF588F5B4', 'Received at the cell suite; shipper temperature logger within -150 C; chain of identity labels verified', 68, 'C'),
('100', '1800004412', 'ZPMI', 'PM-26-0016', '20260807', '180500', '0000100110', 'PP-CCD4B098EAFF', 'Received at the cell suite; shipper temperature logger within -150 C; chain of identity labels verified', 70, 'C'),
('100', '1800004413', 'ZPMI', 'PM-26-0017', '20260829', '201000', '0000100140', 'PP-08BA47CBA05B', 'Received at the cell suite; shipper temperature logger within -150 C; chain of identity labels verified', 66, 'C'),
('100', '1800004414', 'ZPMI', 'PM-26-0018', '20260912', '213000', '0000100140', 'PP-06CCD43B6C3E', 'Received at the cell suite; shipper temperature logger within -150 C; chain of identity labels verified', 64, 'C'),
('100', '1800004419', 'ZPMI', 'PM-26-0019', '20260930', '180000', '0000100140', 'PP-585B1C61A454', NULL, NULL, 'A')
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
('100', '010000012400', 'US10', '01', 'RM-400410', 'RM26-0098', '0000100120', '4500001866', '20260615', '112000', 40, 'L', 40, 'GR inspection AUS1-R-26-0098'),
('100', '010000012403', 'US10', '01', 'RM-100110', 'RM26-0101', '0000100010', '4500001871', '20260622', '141000', 250, 'KG', 250, 'GR inspection AUS1-R-26-0101'),
('100', '010000012406', 'US10', '01', 'RM-200210', 'RM26-0102', '0000100040', '4500001874', '20260624', '093500', 800, 'KG', 800, 'GR inspection AUS1-R-26-0102'),
('100', '010000012409', 'US10', '01', 'RM-200220', 'RM26-0103', '0000100050', '4500001875', '20260624', '102000', 40, 'KG', 40, 'GR inspection AUS1-R-26-0103'),
('100', '010000012412', 'US10', '01', 'RM-100120', 'RM26-0104', '0000100020', '4500001880', '20260706', '130500', 180, 'KG', 180, 'GR inspection AUS1-R-26-0104'),
('100', '010000012415', 'US10', '01', 'RM-100130', 'RM26-0105', '0000100030', '4500001883', '20260713', '115000', 600, 'G', 600, 'GR inspection AUS1-R-26-0105'),
('100', '010000012418', 'US10', '01', 'PK-300310', 'RM26-0106', '0000100060', '4500001884', '20260715', '084000', 8000, 'EA', 8000, 'GR inspection AUS1-R-26-0106'),
('100', '010000012421', 'US10', '01', 'RM-100110', 'RM26-0107', '0000100010', '4500001902', '20260810', '152500', 250, 'KG', 250, 'GR inspection AUS1-R-26-0107'),
('100', '010000012424', 'US10', '01', 'RM-100150', 'RM26-0108', '0000100050', '4500001905', '20260817', '100000', 1200, 'G', 1200, 'GR inspection AUS1-R-26-0108'),
('100', '010000012427', 'US10', '01', 'RM-200240', 'RM26-0109', '0000100080', '4500001911', '20260903', '091000', 300, 'KG', 0, 'GR inspection AUS1-R-26-0109'),
('100', '010000012430', 'US10', '01', 'RM-100120', 'RM26-0110', '0000100020', '4500001915', '20260914', '144500', 180, 'KG', 180, 'GR inspection AUS1-R-26-0110'),
('100', '010000012433', 'US10', '01', 'RM-400410', 'RM26-0111', '0000100120', '4500001921', '20260922', '123000', 60, 'L', NULL, 'GR inspection AUS1-R-26-0111'),
('100', '010000012436', 'US10', '01', 'RM-100110', 'RM26-0112', '0000100010', '4500001924', '20260928', '101500', 250, 'KG', NULL, 'GR inspection AUS1-R-26-0112')
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
('100', '010000012400', 'L', '000001', '3', 'US10-01', 'A1', '20260619', '153000', 'DOKAFOR', 'LW-3100103'),
('100', '010000012403', 'L', '000001', '3', 'US10-01', 'A1', '20260702', '162000', 'DOKAFOR', 'LW-3100106'),
('100', '010000012406', 'L', '000001', '3', 'US10-01', 'A1', '20260630', '110500', 'DOKAFOR', 'LW-3100109'),
('100', '010000012409', 'L', '000001', '3', 'US10-01', 'A1', '20260629', '154500', 'DOKAFOR', 'LW-3100112'),
('100', '010000012412', 'L', '000001', '3', 'US10-01', 'A1', '20260716', '103000', 'DOKAFOR', 'LW-3100115'),
('100', '010000012415', 'L', '000001', '3', 'US10-01', 'A1', '20260724', '140000', 'DOKAFOR', 'LW-3100118'),
('100', '010000012418', 'L', '000001', '3', 'US10-01', 'A1', '20260717', '091500', 'DOKAFOR', 'LW-3100120'),
('100', '010000012421', 'L', '000001', '3', 'US10-01', 'A1', '20260821', '134000', 'DOKAFOR', 'LW-3100123'),
('100', '010000012424', 'L', '000001', '3', 'US10-01', 'A1', '20260827', '161000', 'DOKAFOR', 'LW-3100126'),
('100', '010000012427', 'L', '000001', '3', 'US10-01', 'R1', '20260911', '112500', 'DOKAFOR', 'LW-3100129'),
('100', '010000012430', 'L', '000001', '3', 'US10-01', 'A1', '20260924', '105000', 'DOKAFOR', 'LW-3100132')
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
('100', 'RM-400410', 'RM26-0098', '20261231', '20260416', 'GCC-MED-260603', '0000100120', NULL),
('100', 'RM-100110', 'RM26-0101', '20290531', '20260423', 'HH-LOS-2605117', '0000100010', NULL),
('100', 'RM-200210', 'RM26-0102', '20290331', '20260425', 'DFE-102-6612004', '0000100040', NULL),
('100', 'RM-200220', 'RM26-0103', '20281231', '20260425', 'SPC-MS-1188342', '0000100050', NULL),
('100', 'RM-100120', 'RM26-0104', '20290131', '20260507', 'DRL-CLP-26B0441', '0000100020', NULL),
('100', 'RM-100130', 'RM26-0105', '20290630', '20260514', 'HPM-CIS-240771', '0000100030', NULL),
('100', 'PK-300310', 'RM26-0106', '20310731', '20260516', 'SCH-V50-7781205', '0000100060', NULL),
('100', 'RM-100110', 'RM26-0107', '20290731', '20260611', 'HH-LOS-2607203', '0000100010', NULL),
('100', 'RM-100150', 'RM26-0108', '20280831', '20260618', 'SPC-MTX-1190087', '0000100050', NULL),
('100', 'RM-200240', 'RM26-0109', '20290831', '20260705', 'ROQ-P-6014592', '0000100080', 'X'),
('100', 'RM-100120', 'RM26-0110', '20290831', '20260716', 'DRL-CLP-26C0917', '0000100020', NULL),
('100', 'RM-400410', 'RM26-0111', '20270331', '20260724', 'GCC-MED-260912', '0000100120', 'X'),
('100', 'RM-100110', 'RM26-0112', '20290831', '20260730', 'HH-LOS-2609044', '0000100010', 'X')
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
  CONSTRAINT vbrk_pk PRIMARY KEY (mandt, vbeln)
);
COMMENT ON TABLE sap_s4hana.vbrk IS 'Billing document headers (xblnr = Oracle Receivables invoice number, created from the OMS order).';

INSERT INTO sap_s4hana.vbrk (mandt, vbeln, fkart, fkdat, kunrg, xblnr, netwr, waerk, bukrs) VALUES
('100', '9000000518', 'F2', '20260729', '0000200040', 'AR-26-10431', 148000.00, 'USD', 'US01'),
('100', '9000000521', 'F2', '20260825', '0000200070', 'AR-26-10434', 148000.00, 'USD', 'US01'),
('100', '9000000524', 'F2', '20260916', '0000200040', 'AR-26-10437', 148000.00, 'USD', 'US01')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.vbrp (
  mandt              varchar(3) NOT NULL,
  vbeln              varchar(10) NOT NULL,
  posnr              varchar(6) NOT NULL,
  matnr              varchar(40) NOT NULL,
  netwr              numeric(15,2) NOT NULL,
  fbuda              varchar(8),
  zz_treatment_order varchar(20),
  CONSTRAINT vbrp_pk PRIMARY KEY (mandt, vbeln, posnr)
);
COMMENT ON TABLE sap_s4hana.vbrp IS 'Billing items (fbuda = date the therapy was delivered).';

INSERT INTO sap_s4hana.vbrp (mandt, vbeln, posnr, matnr, netwr, fbuda, zz_treatment_order) VALUES
('100', '9000000518', '000010', 'AU-7710', 148000.00, '20260729', 'TO-26-0015'),
('100', '9000000521', '000010', 'AU-7710', 148000.00, '20260825', 'TO-26-0016'),
('100', '9000000524', '000010', 'AU-7710', 148000.00, '20260916', 'TO-26-0017')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_s4hana.skat (
  mandt varchar(3) NOT NULL,
  spras varchar(1) NOT NULL,
  ktopl varchar(4) NOT NULL,
  saknr varchar(10) NOT NULL,
  txt50 varchar(50) NOT NULL,
  CONSTRAINT skat_pk PRIMARY KEY (mandt, spras, ktopl, saknr)
);
COMMENT ON TABLE sap_s4hana.skat IS 'G/L account texts (chart of accounts YCOA).';

INSERT INTO sap_s4hana.skat (mandt, spras, ktopl, saknr, txt50) VALUES
('100', 'E', 'YCOA', '0001131000', 'Bank - outgoing payments clearing'),
('100', 'E', 'YCOA', '0001200000', 'Trade receivables'),
('100', 'E', 'YCOA', '0001200100', 'Unbilled receivables'),
('100', 'E', 'YCOA', '0001300100', 'Raw materials inventory'),
('100', 'E', 'YCOA', '0001400100', 'Work in process'),
('100', 'E', 'YCOA', '0001600900', 'Construction in progress'),
('100', 'E', 'YCOA', '0002100000', 'Trade payables'),
('100', 'E', 'YCOA', '0002100500', 'Accrued expenses'),
('100', 'E', 'YCOA', '0002300100', 'Accrued payroll and withholdings'),
('100', 'E', 'YCOA', '0004000100', 'Product revenue - distributors'),
('100', 'E', 'YCOA', '0004000300', 'Product revenue - personalised therapy'),
('100', 'E', 'YCOA', '0005100110', 'Manufacturing conversion cost'),
('100', 'E', 'YCOA', '0005100115', 'Cell therapy conversion cost'),
('100', 'E', 'YCOA', '0006100100', 'Salaries - exempt'),
('100', 'E', 'YCOA', '0006100200', 'Wages - hourly'),
('100', 'E', 'YCOA', '0006100300', 'Payroll taxes and benefits'),
('100', 'E', 'YCOA', '0006200300', 'Consulting fees'),
('100', 'E', 'YCOA', '0006300100', 'Utilities'),
('100', 'E', 'YCOA', '0006400100', 'Repairs and maintenance'),
('100', 'E', 'YCOA', '0006400200', 'Facilities services'),
('100', 'E', 'YCOA', '0006500100', 'Freight and courier')
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
('100', '0000000004718237', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260616', '210000', '20260616', '210300'),
('100', '0000000004718274', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260625', '210000', '20260625', '210300'),
('100', '0000000004718311', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260716', '210000', '20260716', '210300'),
('100', '0000000004718348', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260814', '210000', '20260814', '210300'),
('100', '0000000004718385', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260818', '210000', '20260818', '210300'),
('100', '0000000004718422', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260902', '210000', '20260902', '210300'),
('100', '0000000004718459', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260915', '210000', '20260915', '210300'),
('100', '0000000004718496', '53', '2', 'INVOIC', 'LS', 'ARIBA_AUS', '20260923', '210000', '20260923', '210300'),
('100', '0000000004718533', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260717', '015000', '20260717', '015300'),
('100', '0000000004718570', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260720', '152730', '20260720', '153030'),
('100', '0000000004718607', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260803', '205000', '20260803', '205300'),
('100', '0000000004718644', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260814', '014000', '20260814', '014300'),
('100', '0000000004718681', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260817', '195000', '20260817', '195300'),
('100', '0000000004718718', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260901', '155000', '20260901', '155300'),
('100', '0000000004718755', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260905', '011000', '20260905', '011300'),
('100', '0000000004718792', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260907', '205000', '20260907', '205300'),
('100', '0000000004718829', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260914', '150500', '20260914', '150800'),
('100', '0000000004718866', '53', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260919', '013000', '20260919', '013300'),
('100', '0000000004718903', '64', '2', 'WMMBXY', 'LS', 'OPCENTER', '20260928', '205000', '20260928', '110500'),
('100', '0000000004718940', '53', '2', 'ACC_DOCUMENT', 'LS', 'WORKDAY_US', '20260730', '203000', '20260730', '203300'),
('100', '0000000004718977', '53', '2', 'ACC_DOCUMENT', 'LS', 'WORKDAY_US', '20260830', '203000', '20260830', '203300'),
('100', '0000000004719014', '53', '2', 'ACC_DOCUMENT', 'LS', 'WORKDAY_US', '20260929', '203000', '20260929', '203300'),
('100', '0000000004719051', '53', '2', 'ACC_DOCUMENT', 'LS', 'MAXIMO_AUS', '20260728', '231000', '20260728', '231300'),
('100', '0000000004719088', '53', '2', 'ACC_DOCUMENT', 'LS', 'MAXIMO_AUS', '20260828', '231000', '20260828', '231300'),
('100', '0000000004719125', '51', '2', 'ACC_DOCUMENT', 'LS', 'MAXIMO_AUS', '20260928', '231000', '20260928', '231100')
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
COMMENT ON TABLE sap_s4hana.bkpf IS 'Accounting document headers (awtyp IDOC: awkey = inbound IDoc number; VBRK: billing document; tcode FBV0 = posted from a parked document).';

INSERT INTO sap_s4hana.bkpf (mandt, bukrs, belnr, gjahr, blart, bldat, budat, monat, cpudt, cputm, usnam, tcode, xblnr, bktxt, awtyp, awkey, waers) VALUES
('100', 'US01', '5105600001', '2026', 'RE', '20260616', '20260616', '06', '20260616', '210000', 'ARIBA_RFC', 'BAPI', 'GCC-26-0615', 'Ariba invoice GCC-26-0615', 'IDOC', '0000000004718237', 'USD'),
('100', 'US01', '5105600002', '2026', 'RE', '20260623', '20260623', '06', '20260625', '210000', 'ARIBA_RFC', 'BAPI', 'HH-INV-260611', 'Ariba invoice HH-INV-260611', 'IDOC', '0000000004718274', 'USD'),
('100', 'US01', '5105600003', '2026', 'RE', '20260624', '20260624', '06', '20260625', '210000', 'ARIBA_RFC', 'BAPI', 'DFE-90412277', 'Ariba invoice DFE-90412277', 'IDOC', '0000000004718274', 'USD'),
('100', 'US01', '5105600004', '2026', 'RE', '20260625', '20260625', '06', '20260625', '210000', 'ARIBA_RFC', 'BAPI', 'SPC-INV-558812', 'Ariba invoice SPC-INV-558812', 'IDOC', '0000000004718274', 'USD'),
('100', 'US01', '5105600005', '2026', 'RE', '20260714', '20260714', '07', '20260716', '210000', 'ARIBA_RFC', 'BAPI', 'HPM-2026-07-1188', 'Ariba invoice HPM-2026-07-1188', 'IDOC', '0000000004718311', 'USD'),
('100', 'US01', '5105600006', '2026', 'RE', '20260716', '20260716', '07', '20260716', '210000', 'ARIBA_RFC', 'BAPI', 'SCH-US-3310027', 'Ariba invoice SCH-US-3310027', 'IDOC', '0000000004718311', 'USD'),
('100', 'US01', '5105600007', '2026', 'RE', '20260811', '20260811', '08', '20260814', '210000', 'ARIBA_RFC', 'BAPI', 'HH-INV-260809', 'Ariba invoice HH-INV-260809', 'IDOC', '0000000004718348', 'USD'),
('100', 'US01', '5105600008', '2026', 'RE', '20260814', '20260814', '08', '20260814', '210000', 'ARIBA_RFC', 'BAPI', 'LCS-2026-0814', 'Ariba invoice LCS-2026-0814', 'IDOC', '0000000004718348', 'USD'),
('100', 'US01', '5105600009', '2026', 'RE', '20260818', '20260818', '08', '20260818', '210000', 'ARIBA_RFC', 'BAPI', 'SPC-INV-561470', 'Ariba invoice SPC-INV-561470', 'IDOC', '0000000004718385', 'USD'),
('100', 'US01', '5105600010', '2026', 'RE', '20260831', '20260831', '08', '20260902', '210000', 'ARIBA_RFC', 'BAPI', 'LBL-88213', 'Ariba invoice LBL-88213', 'IDOC', '0000000004718422', 'USD'),
('100', 'US01', '5105600011', '2026', 'RE', '20260902', '20260902', '09', '20260902', '210000', 'ARIBA_RFC', 'BAPI', 'HCF-10277', 'Ariba invoice HCF-10277', 'IDOC', '0000000004718422', 'USD'),
('100', 'US01', '5105600012', '2026', 'RE', '20260915', '20260915', '09', '20260915', '210000', 'ARIBA_RFC', 'BAPI', 'DRL/26/EXP/0917', 'Ariba invoice DRL/26/EXP/0917', 'IDOC', '0000000004718459', 'USD'),
('100', 'US01', '5105600013', '2026', 'RE', '20260923', '20260923', '09', '20260923', '210000', 'ARIBA_RFC', 'BAPI', 'GCC-26-0922', 'Ariba invoice GCC-26-0922', 'IDOC', '0000000004718496', 'USD'),
('100', 'US01', '4900000001', '2026', 'WA', '20260717', '20260717', '07', '20260717', '015000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-7710-P015', 'Goods issue to order 1000481 batch A26-7710-P015', 'IDOC', '0000000004718533', 'USD'),
('100', 'US01', '4900000002', '2026', 'WA', '20260720', '20260720', '07', '20260720', '152730', 'OPCENTER_RFC', 'MIGO_GI', 'A26-4410-0052', 'Goods issue to order 1000402 batch A26-4410-0052', 'IDOC', '0000000004718570', 'USD'),
('100', 'US01', '4900000003', '2026', 'WA', '20260803', '20260803', '08', '20260803', '205000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-3000-0141', 'Goods issue to order 1000412 batch A26-3000-0141', 'IDOC', '0000000004718607', 'USD'),
('100', 'US01', '4900000004', '2026', 'WA', '20260814', '20260814', '08', '20260814', '014000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-7710-P016', 'Goods issue to order 1000482 batch A26-7710-P016', 'IDOC', '0000000004718644', 'USD'),
('100', 'US01', '4900000005', '2026', 'WA', '20260817', '20260817', '08', '20260817', '195000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-2050-0087', 'Goods issue to order 1000431 batch A26-2050-0087', 'IDOC', '0000000004718681', 'USD'),
('100', 'US01', '4900000006', '2026', 'WA', '20260901', '20260901', '09', '20260901', '155000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-9000-0019', 'Goods issue to order 1000448 batch A26-9000-0019', 'IDOC', '0000000004718718', 'USD'),
('100', 'US01', '4900000007', '2026', 'WA', '20260905', '20260905', '09', '20260905', '011000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-7710-P017', 'Goods issue to order 1000483 batch A26-7710-P017', 'IDOC', '0000000004718755', 'USD'),
('100', 'US01', '4900000008', '2026', 'WA', '20260907', '20260907', '09', '20260907', '205000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-3000-0142', 'Goods issue to order 1000457 batch A26-3000-0142', 'IDOC', '0000000004718792', 'USD'),
('100', 'US01', '4900000009', '2026', 'WA', '20260914', '20260914', '09', '20260914', '150500', 'OPCENTER_RFC', 'MIGO_GI', 'A26-4630-0017', 'Goods issue to order 1000452 batch A26-4630-0017', 'IDOC', '0000000004718829', 'USD'),
('100', 'US01', '4900000010', '2026', 'WA', '20260919', '20260919', '09', '20260919', '013000', 'OPCENTER_RFC', 'MIGO_GI', 'A26-7710-P018', 'Goods issue to order 1000484 batch A26-7710-P018', 'IDOC', '0000000004718866', 'USD'),
('100', 'US01', '1000000001', '2026', 'ZP', '20260731', '20260731', '07', '20260730', '203000', 'WORKDAY_RFC', 'BAPI', 'PR-US01-2026-07', 'Workday payroll PR-US01-2026-07', 'IDOC', '0000000004718940', 'USD'),
('100', 'US01', '1000000002', '2026', 'ZP', '20260831', '20260831', '08', '20260830', '203000', 'WORKDAY_RFC', 'BAPI', 'PR-US01-2026-08', 'Workday payroll PR-US01-2026-08', 'IDOC', '0000000004718977', 'USD'),
('100', 'US01', '1000000003', '2026', 'ZP', '20260930', '20260930', '09', '20260929', '203000', 'WORKDAY_RFC', 'BAPI', 'PR-US01-2026-09', 'Workday payroll PR-US01-2026-09', 'IDOC', '0000000004719014', 'USD'),
('100', 'US01', '1000000004', '2026', 'ZM', '20260728', '20260728', '07', '20260728', '231000', 'MAXIMO_RFC', 'BAPI', 'MX-2026-07', 'Maximo work order costs 2026-07', 'IDOC', '0000000004719051', 'USD'),
('100', 'US01', '1000000005', '2026', 'ZM', '20260828', '20260828', '08', '20260828', '231000', 'MAXIMO_RFC', 'BAPI', 'MX-2026-08', 'Maximo work order costs 2026-08', 'IDOC', '0000000004719088', 'USD'),
('100', 'US01', '1500000194', '2026', 'KZ', '20260716', '20260716', '07', '20260716', '061500', 'BATCH_F110', 'F110', 'GCC-26-0615', 'Payment GCC-26-0615', 'BKPF', '1500000194', 'USD'),
('100', 'US01', '1500000211', '2026', 'KZ', '20260821', '20260821', '08', '20260821', '061500', 'BATCH_F110', 'F110', 'HH-INV-260611', 'Payment HH-INV-260611', 'BKPF', '1500000211', 'USD'),
('100', 'US01', '1500000198', '2026', 'KZ', '20260724', '20260724', '07', '20260724', '061500', 'BATCH_F110', 'F110', 'DFE-90412277', 'Payment DFE-90412277', 'BKPF', '1500000198', 'USD'),
('100', 'US01', '1500000199', '2026', 'KZ', '20260724', '20260724', '07', '20260724', '061500', 'BATCH_F110', 'F110', 'SPC-INV-558812', 'Payment SPC-INV-558812', 'BKPF', '1500000199', 'USD'),
('100', 'US01', '1500000224', '2026', 'KZ', '20260911', '20260911', '09', '20260911', '061500', 'BATCH_F110', 'F110', 'HPM-2026-07-1188', 'Payment HPM-2026-07-1188', 'BKPF', '1500000224', 'USD'),
('100', 'US01', '1500000207', '2026', 'KZ', '20260814', '20260814', '08', '20260814', '061500', 'BATCH_F110', 'F110', 'SCH-US-3310027', 'Payment SCH-US-3310027', 'BKPF', '1500000207', 'USD'),
('100', 'US01', '1500000225', '2026', 'KZ', '20260911', '20260911', '09', '20260911', '061500', 'BATCH_F110', 'F110', 'LCS-2026-0814', 'Payment LCS-2026-0814', 'BKPF', '1500000225', 'USD'),
('100', 'US01', '1500000229', '2026', 'KZ', '20260917', '20260917', '09', '20260917', '061500', 'BATCH_F110', 'F110', 'SPC-INV-561470', 'Payment SPC-INV-561470', 'BKPF', '1500000229', 'USD'),
('100', 'US01', '1500000234', '2026', 'KZ', '20260925', '20260925', '09', '20260925', '061500', 'BATCH_F110', 'F110', 'LBL-88213', 'Payment LBL-88213', 'BKPF', '1500000234', 'USD'),
('100', 'US01', '1500000233', '2026', 'KZ', '20260925', '20260925', '09', '20260925', '061500', 'BATCH_F110', 'F110', 'HCF-10277', 'Payment HCF-10277', 'BKPF', '1500000233', 'USD'),
('100', 'US01', '1900000041', '2026', 'SA', '20260731', '20260731', '07', '20260803', '154000', 'LCARRANZA', 'FBV0', NULL, 'Q2 utilities true-up accrual, Austin plant', 'BKPF', '1900000041', 'USD'),
('100', 'US01', '1900000047', '2026', 'SA', '20260831', '20260831', '08', '20260902', '102500', 'LCARRANZA', 'FBV0', NULL, 'Reclass cell therapy costs from CC-110 to CC-115', 'BKPF', '1900000047', 'USD'),
('100', 'US01', '1900000055', '2026', 'SA', '20260930', '20260930', '09', '20260929', '113500', 'LCARRANZA', 'FBV0', NULL, 'Accrue Sep calibration and facilities services', 'BKPF', '1900000055', 'USD'),
('100', 'US01', '9400000001', '2026', 'RV', '20260729', '20260729', '07', '20260729', '200000', 'OMS_RFC', 'VF01', 'AR-26-10431', 'Billing 9000000518 for TO-26-0015', 'VBRK', '9000000518', 'USD'),
('100', 'US01', '9400000002', '2026', 'RV', '20260825', '20260825', '08', '20260825', '200000', 'OMS_RFC', 'VF01', 'AR-26-10434', 'Billing 9000000521 for TO-26-0016', 'VBRK', '9000000521', 'USD'),
('100', 'US01', '9400000003', '2026', 'RV', '20260916', '20260916', '09', '20260916', '200000', 'OMS_RFC', 'VF01', 'AR-26-10437', 'Billing 9000000524 for TO-26-0017', 'VBRK', '9000000524', 'USD')
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
  CONSTRAINT acdoca_pk PRIMARY KEY (rclnt, rldnr, rbukrs, gjahr, belnr, docln)
);
COMMENT ON TABLE sap_s4hana.acdoca IS 'Universal journal line items, leading ledger 0L (hsl in company code currency, debit positive).';

INSERT INTO sap_s4hana.acdoca (rclnt, rldnr, rbukrs, gjahr, belnr, docln, racct, rcntr, hsl, rhcur, drcrk, budat, poper, koart, lifnr, kunnr, matnr, zuonr, sgtxt, awtyp, awref) VALUES
('100', '0L', 'US01', '2026', '5105600001', '000001', '0001300100', NULL, 34000.00, 'USD', 'S', '20260616', '006', 'S', NULL, NULL, NULL, 'GCC-26-0615', 'Ariba invoice GCC-26-0615', 'IDOC', '5105600001'),
('100', '0L', 'US01', '2026', '5105600001', '000002', '0002100000', NULL, -34000.00, 'USD', 'H', '20260616', '006', 'K', '0000100120', NULL, NULL, 'GCC-26-0615', 'Ariba invoice GCC-26-0615', 'IDOC', '5105600001'),
('100', '0L', 'US01', '2026', '5105600002', '000001', '0001300100', NULL, 77500.00, 'USD', 'S', '20260623', '006', 'S', NULL, NULL, NULL, 'HH-INV-260611', 'Ariba invoice HH-INV-260611', 'IDOC', '5105600002'),
('100', '0L', 'US01', '2026', '5105600002', '000002', '0002100000', NULL, -77500.00, 'USD', 'H', '20260623', '006', 'K', '0000100010', NULL, NULL, 'HH-INV-260611', 'Ariba invoice HH-INV-260611', 'IDOC', '5105600002'),
('100', '0L', 'US01', '2026', '5105600003', '000001', '0001300100', NULL, 4800.00, 'USD', 'S', '20260624', '006', 'S', NULL, NULL, NULL, 'DFE-90412277', 'Ariba invoice DFE-90412277', 'IDOC', '5105600003'),
('100', '0L', 'US01', '2026', '5105600003', '000002', '0002100000', NULL, -4800.00, 'USD', 'H', '20260624', '006', 'K', '0000100040', NULL, NULL, 'DFE-90412277', 'Ariba invoice DFE-90412277', 'IDOC', '5105600003'),
('100', '0L', 'US01', '2026', '5105600004', '000001', '0001300100', NULL, 560.00, 'USD', 'S', '20260625', '006', 'S', NULL, NULL, NULL, 'SPC-INV-558812', 'Ariba invoice SPC-INV-558812', 'IDOC', '5105600004'),
('100', '0L', 'US01', '2026', '5105600004', '000002', '0002100000', NULL, -560.00, 'USD', 'H', '20260625', '006', 'K', '0000100050', NULL, NULL, 'SPC-INV-558812', 'Ariba invoice SPC-INV-558812', 'IDOC', '5105600004'),
('100', '0L', 'US01', '2026', '5105600005', '000001', '0001300100', NULL, 57000.00, 'USD', 'S', '20260714', '007', 'S', NULL, NULL, NULL, 'HPM-2026-07-1188', 'Ariba invoice HPM-2026-07-1188', 'IDOC', '5105600005'),
('100', '0L', 'US01', '2026', '5105600005', '000002', '0002100000', NULL, -57000.00, 'USD', 'H', '20260714', '007', 'K', '0000100030', NULL, NULL, 'HPM-2026-07-1188', 'Ariba invoice HPM-2026-07-1188', 'IDOC', '5105600005'),
('100', '0L', 'US01', '2026', '5105600006', '000001', '0001300100', NULL, 3360.00, 'USD', 'S', '20260716', '007', 'S', NULL, NULL, NULL, 'SCH-US-3310027', 'Ariba invoice SCH-US-3310027', 'IDOC', '5105600006'),
('100', '0L', 'US01', '2026', '5105600006', '000002', '0002100000', NULL, -3360.00, 'USD', 'H', '20260716', '007', 'K', '0000100060', NULL, NULL, 'SCH-US-3310027', 'Ariba invoice SCH-US-3310027', 'IDOC', '5105600006'),
('100', '0L', 'US01', '2026', '5105600007', '000001', '0001300100', NULL, 77500.00, 'USD', 'S', '20260811', '008', 'S', NULL, NULL, NULL, 'HH-INV-260809', 'Ariba invoice HH-INV-260809', 'IDOC', '5105600007'),
('100', '0L', 'US01', '2026', '5105600007', '000002', '0002100000', NULL, -77500.00, 'USD', 'H', '20260811', '008', 'K', '0000100010', NULL, NULL, 'HH-INV-260809', 'Ariba invoice HH-INV-260809', 'IDOC', '5105600007'),
('100', '0L', 'US01', '2026', '5105600008', '000001', '0006400100', NULL, 6850.00, 'USD', 'S', '20260814', '008', 'S', NULL, NULL, NULL, 'LCS-2026-0814', 'Ariba invoice LCS-2026-0814', 'IDOC', '5105600008'),
('100', '0L', 'US01', '2026', '5105600008', '000002', '0002100000', NULL, -6850.00, 'USD', 'H', '20260814', '008', 'K', '0000100090', NULL, NULL, 'LCS-2026-0814', 'Ariba invoice LCS-2026-0814', 'IDOC', '5105600008'),
('100', '0L', 'US01', '2026', '5105600009', '000001', '0001300100', NULL, 45600.00, 'USD', 'S', '20260818', '008', 'S', NULL, NULL, NULL, 'SPC-INV-561470', 'Ariba invoice SPC-INV-561470', 'IDOC', '5105600009'),
('100', '0L', 'US01', '2026', '5105600009', '000002', '0002100000', NULL, -45600.00, 'USD', 'H', '20260818', '008', 'K', '0000100050', NULL, NULL, 'SPC-INV-561470', 'Ariba invoice SPC-INV-561470', 'IDOC', '5105600009'),
('100', '0L', 'US01', '2026', '5105600010', '000001', '0006500100', NULL, 9300.00, 'USD', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'LBL-88213', 'Ariba invoice LBL-88213', 'IDOC', '5105600010'),
('100', '0L', 'US01', '2026', '5105600010', '000002', '0002100000', NULL, -9300.00, 'USD', 'H', '20260831', '008', 'K', '0000100110', NULL, NULL, 'LBL-88213', 'Ariba invoice LBL-88213', 'IDOC', '5105600010'),
('100', '0L', 'US01', '2026', '5105600011', '000001', '0006400200', NULL, 12400.00, 'USD', 'S', '20260902', '009', 'S', NULL, NULL, NULL, 'HCF-10277', 'Ariba invoice HCF-10277', 'IDOC', '5105600011'),
('100', '0L', 'US01', '2026', '5105600011', '000002', '0002100000', NULL, -12400.00, 'USD', 'H', '20260902', '009', 'K', '0000100100', NULL, NULL, 'HCF-10277', 'Ariba invoice HCF-10277', 'IDOC', '5105600011'),
('100', '0L', 'US01', '2026', '5105600012', '000001', '0001300100', NULL, 75600.00, 'USD', 'S', '20260915', '009', 'S', NULL, NULL, NULL, 'DRL/26/EXP/0917', 'Ariba invoice DRL/26/EXP/0917', 'IDOC', '5105600012'),
('100', '0L', 'US01', '2026', '5105600012', '000002', '0002100000', NULL, -75600.00, 'USD', 'H', '20260915', '009', 'K', '0000100020', NULL, NULL, 'DRL/26/EXP/0917', 'Ariba invoice DRL/26/EXP/0917', 'IDOC', '5105600012'),
('100', '0L', 'US01', '2026', '5105600013', '000001', '0001300100', NULL, 51000.00, 'USD', 'S', '20260923', '009', 'S', NULL, NULL, NULL, 'GCC-26-0922', 'Ariba invoice GCC-26-0922', 'IDOC', '5105600013'),
('100', '0L', 'US01', '2026', '5105600013', '000002', '0002100000', NULL, -51000.00, 'USD', 'H', '20260923', '009', 'K', '0000100120', NULL, NULL, 'GCC-26-0922', 'Ariba invoice GCC-26-0922', 'IDOC', '5105600013'),
('100', '0L', 'US01', '2026', '4900000001', '000001', '0001400100', 'CC-US10-115', 2125.00, 'USD', 'S', '20260717', '007', 'S', NULL, NULL, 'AU-7710', 'A26-7710-P015', 'Goods issue to order 1000481 batch A26-7710-P015', 'IDOC', '4900000001'),
('100', '0L', 'US01', '2026', '4900000001', '000002', '0001300100', NULL, -2125.00, 'USD', 'H', '20260717', '007', 'S', NULL, NULL, NULL, 'A26-7710-P015', 'Goods issue to order 1000481 batch A26-7710-P015', 'IDOC', '4900000001'),
('100', '0L', 'US01', '2026', '4900000002', '000001', '0001400100', 'CC-US10-110', 131609.20, 'USD', 'S', '20260720', '007', 'S', NULL, NULL, 'AU-4410', 'A26-4410-0052', 'Goods issue to order 1000402 batch A26-4410-0052', 'IDOC', '4900000002'),
('100', '0L', 'US01', '2026', '4900000002', '000002', '0001300100', NULL, -131609.20, 'USD', 'H', '20260720', '007', 'S', NULL, NULL, NULL, 'A26-4410-0052', 'Goods issue to order 1000402 batch A26-4410-0052', 'IDOC', '4900000002'),
('100', '0L', 'US01', '2026', '4900000003', '000001', '0001400100', 'CC-US10-110', 3956.20, 'USD', 'S', '20260803', '008', 'S', NULL, NULL, '3000', 'A26-3000-0141', 'Goods issue to order 1000412 batch A26-3000-0141', 'IDOC', '4900000003'),
('100', '0L', 'US01', '2026', '4900000003', '000002', '0001300100', NULL, -3956.20, 'USD', 'H', '20260803', '008', 'S', NULL, NULL, NULL, 'A26-3000-0141', 'Goods issue to order 1000412 batch A26-3000-0141', 'IDOC', '4900000003'),
('100', '0L', 'US01', '2026', '4900000004', '000001', '0001400100', 'CC-US10-115', 2125.00, 'USD', 'S', '20260814', '008', 'S', NULL, NULL, 'AU-7710', 'A26-7710-P016', 'Goods issue to order 1000482 batch A26-7710-P016', 'IDOC', '4900000004'),
('100', '0L', 'US01', '2026', '4900000004', '000002', '0001300100', NULL, -2125.00, 'USD', 'H', '20260814', '008', 'S', NULL, NULL, NULL, 'A26-7710-P016', 'Goods issue to order 1000482 batch A26-7710-P016', 'IDOC', '4900000004'),
('100', '0L', 'US01', '2026', '4900000005', '000001', '0001400100', 'CC-US10-110', 3825.50, 'USD', 'S', '20260817', '008', 'S', NULL, NULL, '2050', 'A26-2050-0087', 'Goods issue to order 1000431 batch A26-2050-0087', 'IDOC', '4900000005'),
('100', '0L', 'US01', '2026', '4900000005', '000002', '0001300100', NULL, -3825.50, 'USD', 'H', '20260817', '008', 'S', NULL, NULL, NULL, 'A26-2050-0087', 'Goods issue to order 1000431 batch A26-2050-0087', 'IDOC', '4900000005'),
('100', '0L', 'US01', '2026', '4900000006', '000001', '0001400100', 'CC-US10-110', 13516.00, 'USD', 'S', '20260901', '009', 'S', NULL, NULL, '9000', 'A26-9000-0019', 'Goods issue to order 1000448 batch A26-9000-0019', 'IDOC', '4900000006'),
('100', '0L', 'US01', '2026', '4900000006', '000002', '0001300100', NULL, -13516.00, 'USD', 'H', '20260901', '009', 'S', NULL, NULL, NULL, 'A26-9000-0019', 'Goods issue to order 1000448 batch A26-9000-0019', 'IDOC', '4900000006'),
('100', '0L', 'US01', '2026', '4900000007', '000001', '0001400100', 'CC-US10-115', 2125.00, 'USD', 'S', '20260905', '009', 'S', NULL, NULL, 'AU-7710', 'A26-7710-P017', 'Goods issue to order 1000483 batch A26-7710-P017', 'IDOC', '4900000007'),
('100', '0L', 'US01', '2026', '4900000007', '000002', '0001300100', NULL, -2125.00, 'USD', 'H', '20260905', '009', 'S', NULL, NULL, NULL, 'A26-7710-P017', 'Goods issue to order 1000483 batch A26-7710-P017', 'IDOC', '4900000007'),
('100', '0L', 'US01', '2026', '4900000008', '000001', '0001400100', 'CC-US10-110', 3956.20, 'USD', 'S', '20260907', '009', 'S', NULL, NULL, '3000', 'A26-3000-0142', 'Goods issue to order 1000457 batch A26-3000-0142', 'IDOC', '4900000008'),
('100', '0L', 'US01', '2026', '4900000008', '000002', '0001300100', NULL, -3956.20, 'USD', 'H', '20260907', '009', 'S', NULL, NULL, NULL, 'A26-3000-0142', 'Goods issue to order 1000457 batch A26-3000-0142', 'IDOC', '4900000008'),
('100', '0L', 'US01', '2026', '4900000009', '000001', '0001400100', 'CC-US10-110', 40853.60, 'USD', 'S', '20260914', '009', 'S', NULL, NULL, 'AU-4630', 'A26-4630-0017', 'Goods issue to order 1000452 batch A26-4630-0017', 'IDOC', '4900000009'),
('100', '0L', 'US01', '2026', '4900000009', '000002', '0001300100', NULL, -40853.60, 'USD', 'H', '20260914', '009', 'S', NULL, NULL, NULL, 'A26-4630-0017', 'Goods issue to order 1000452 batch A26-4630-0017', 'IDOC', '4900000009'),
('100', '0L', 'US01', '2026', '4900000010', '000001', '0001400100', 'CC-US10-115', 2125.00, 'USD', 'S', '20260919', '009', 'S', NULL, NULL, 'AU-7710', 'A26-7710-P018', 'Goods issue to order 1000484 batch A26-7710-P018', 'IDOC', '4900000010'),
('100', '0L', 'US01', '2026', '4900000010', '000002', '0001300100', NULL, -2125.00, 'USD', 'H', '20260919', '009', 'S', NULL, NULL, NULL, 'A26-7710-P018', 'Goods issue to order 1000484 batch A26-7710-P018', 'IDOC', '4900000010'),
('100', '0L', 'US01', '2026', '1000000001', '000001', '0006100100', NULL, 137083.34, 'USD', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-US01-2026-07', 'Workday payroll PR-US01-2026-07', 'IDOC', '1000000001'),
('100', '0L', 'US01', '2026', '1000000001', '000002', '0006100200', NULL, 31365.00, 'USD', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-US01-2026-07', 'Workday payroll PR-US01-2026-07', 'IDOC', '1000000001'),
('100', '0L', 'US01', '2026', '1000000001', '000003', '0006100300', NULL, 36469.05, 'USD', 'S', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-US01-2026-07', 'Workday payroll PR-US01-2026-07', 'IDOC', '1000000001'),
('100', '0L', 'US01', '2026', '1000000001', '000004', '0002300100', NULL, -204917.39, 'USD', 'H', '20260731', '007', 'S', NULL, NULL, NULL, 'PR-US01-2026-07', 'Workday payroll PR-US01-2026-07', 'IDOC', '1000000001'),
('100', '0L', 'US01', '2026', '1000000002', '000001', '0006100100', NULL, 137083.34, 'USD', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-US01-2026-08', 'Workday payroll PR-US01-2026-08', 'IDOC', '1000000002'),
('100', '0L', 'US01', '2026', '1000000002', '000002', '0006100200', NULL, 28323.16, 'USD', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-US01-2026-08', 'Workday payroll PR-US01-2026-08', 'IDOC', '1000000002'),
('100', '0L', 'US01', '2026', '1000000002', '000003', '0006100300', NULL, 35810.50, 'USD', 'S', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-US01-2026-08', 'Workday payroll PR-US01-2026-08', 'IDOC', '1000000002'),
('100', '0L', 'US01', '2026', '1000000002', '000004', '0002300100', NULL, -201217.00, 'USD', 'H', '20260831', '008', 'S', NULL, NULL, NULL, 'PR-US01-2026-08', 'Workday payroll PR-US01-2026-08', 'IDOC', '1000000002'),
('100', '0L', 'US01', '2026', '1000000003', '000001', '0006100100', NULL, 141044.45, 'USD', 'S', '20260930', '009', 'S', NULL, NULL, NULL, 'PR-US01-2026-09', 'Workday payroll PR-US01-2026-09', 'IDOC', '1000000003'),
('100', '0L', 'US01', '2026', '1000000003', '000002', '0006100200', NULL, 26529.50, 'USD', 'S', '20260930', '009', 'S', NULL, NULL, NULL, 'PR-US01-2026-09', 'Workday payroll PR-US01-2026-09', 'IDOC', '1000000003'),
('100', '0L', 'US01', '2026', '1000000003', '000003', '0006100300', NULL, 36279.76, 'USD', 'S', '20260930', '009', 'S', NULL, NULL, NULL, 'PR-US01-2026-09', 'Workday payroll PR-US01-2026-09', 'IDOC', '1000000003'),
('100', '0L', 'US01', '2026', '1000000003', '000004', '0002300100', NULL, -203853.71, 'USD', 'H', '20260930', '009', 'S', NULL, NULL, NULL, 'PR-US01-2026-09', 'Workday payroll PR-US01-2026-09', 'IDOC', '1000000003'),
('100', '0L', 'US01', '2026', '1000000004', '000001', '0006400100', 'CC-US10-150', 18420.55, 'USD', 'S', '20260728', '007', 'S', NULL, NULL, NULL, 'MX-2026-07', 'Maximo work order costs 2026-07', 'IDOC', '1000000004'),
('100', '0L', 'US01', '2026', '1000000004', '000002', '0002100500', NULL, -18420.55, 'USD', 'H', '20260728', '007', 'S', NULL, NULL, NULL, 'MX-2026-07', 'Maximo work order costs 2026-07', 'IDOC', '1000000004'),
('100', '0L', 'US01', '2026', '1000000005', '000001', '0006400100', 'CC-US10-150', 22960.10, 'USD', 'S', '20260828', '008', 'S', NULL, NULL, NULL, 'MX-2026-08', 'Maximo work order costs 2026-08', 'IDOC', '1000000005'),
('100', '0L', 'US01', '2026', '1000000005', '000002', '0002100500', NULL, -22960.10, 'USD', 'H', '20260828', '008', 'S', NULL, NULL, NULL, 'MX-2026-08', 'Maximo work order costs 2026-08', 'IDOC', '1000000005'),
('100', '0L', 'US01', '2026', '1500000194', '000001', '0002100000', NULL, 34000.00, 'USD', 'S', '20260716', '007', 'K', '0000100120', NULL, NULL, 'GCC-26-0615', 'Payment GCC-26-0615', 'BKPF', '1500000194'),
('100', '0L', 'US01', '2026', '1500000194', '000002', '0001131000', NULL, -34000.00, 'USD', 'H', '20260716', '007', 'S', NULL, NULL, NULL, 'GCC-26-0615', 'Payment GCC-26-0615', 'BKPF', '1500000194'),
('100', '0L', 'US01', '2026', '1500000211', '000001', '0002100000', NULL, 77500.00, 'USD', 'S', '20260821', '008', 'K', '0000100010', NULL, NULL, 'HH-INV-260611', 'Payment HH-INV-260611', 'BKPF', '1500000211'),
('100', '0L', 'US01', '2026', '1500000211', '000002', '0001131000', NULL, -77500.00, 'USD', 'H', '20260821', '008', 'S', NULL, NULL, NULL, 'HH-INV-260611', 'Payment HH-INV-260611', 'BKPF', '1500000211'),
('100', '0L', 'US01', '2026', '1500000198', '000001', '0002100000', NULL, 4800.00, 'USD', 'S', '20260724', '007', 'K', '0000100040', NULL, NULL, 'DFE-90412277', 'Payment DFE-90412277', 'BKPF', '1500000198'),
('100', '0L', 'US01', '2026', '1500000198', '000002', '0001131000', NULL, -4800.00, 'USD', 'H', '20260724', '007', 'S', NULL, NULL, NULL, 'DFE-90412277', 'Payment DFE-90412277', 'BKPF', '1500000198'),
('100', '0L', 'US01', '2026', '1500000199', '000001', '0002100000', NULL, 560.00, 'USD', 'S', '20260724', '007', 'K', '0000100050', NULL, NULL, 'SPC-INV-558812', 'Payment SPC-INV-558812', 'BKPF', '1500000199'),
('100', '0L', 'US01', '2026', '1500000199', '000002', '0001131000', NULL, -560.00, 'USD', 'H', '20260724', '007', 'S', NULL, NULL, NULL, 'SPC-INV-558812', 'Payment SPC-INV-558812', 'BKPF', '1500000199'),
('100', '0L', 'US01', '2026', '1500000224', '000001', '0002100000', NULL, 57000.00, 'USD', 'S', '20260911', '009', 'K', '0000100030', NULL, NULL, 'HPM-2026-07-1188', 'Payment HPM-2026-07-1188', 'BKPF', '1500000224'),
('100', '0L', 'US01', '2026', '1500000224', '000002', '0001131000', NULL, -57000.00, 'USD', 'H', '20260911', '009', 'S', NULL, NULL, NULL, 'HPM-2026-07-1188', 'Payment HPM-2026-07-1188', 'BKPF', '1500000224'),
('100', '0L', 'US01', '2026', '1500000207', '000001', '0002100000', NULL, 3360.00, 'USD', 'S', '20260814', '008', 'K', '0000100060', NULL, NULL, 'SCH-US-3310027', 'Payment SCH-US-3310027', 'BKPF', '1500000207'),
('100', '0L', 'US01', '2026', '1500000207', '000002', '0001131000', NULL, -3360.00, 'USD', 'H', '20260814', '008', 'S', NULL, NULL, NULL, 'SCH-US-3310027', 'Payment SCH-US-3310027', 'BKPF', '1500000207'),
('100', '0L', 'US01', '2026', '1500000225', '000001', '0002100000', NULL, 6850.00, 'USD', 'S', '20260911', '009', 'K', '0000100090', NULL, NULL, 'LCS-2026-0814', 'Payment LCS-2026-0814', 'BKPF', '1500000225'),
('100', '0L', 'US01', '2026', '1500000225', '000002', '0001131000', NULL, -6850.00, 'USD', 'H', '20260911', '009', 'S', NULL, NULL, NULL, 'LCS-2026-0814', 'Payment LCS-2026-0814', 'BKPF', '1500000225'),
('100', '0L', 'US01', '2026', '1500000229', '000001', '0002100000', NULL, 45600.00, 'USD', 'S', '20260917', '009', 'K', '0000100050', NULL, NULL, 'SPC-INV-561470', 'Payment SPC-INV-561470', 'BKPF', '1500000229'),
('100', '0L', 'US01', '2026', '1500000229', '000002', '0001131000', NULL, -45600.00, 'USD', 'H', '20260917', '009', 'S', NULL, NULL, NULL, 'SPC-INV-561470', 'Payment SPC-INV-561470', 'BKPF', '1500000229'),
('100', '0L', 'US01', '2026', '1500000234', '000001', '0002100000', NULL, 9300.00, 'USD', 'S', '20260925', '009', 'K', '0000100110', NULL, NULL, 'LBL-88213', 'Payment LBL-88213', 'BKPF', '1500000234'),
('100', '0L', 'US01', '2026', '1500000234', '000002', '0001131000', NULL, -9300.00, 'USD', 'H', '20260925', '009', 'S', NULL, NULL, NULL, 'LBL-88213', 'Payment LBL-88213', 'BKPF', '1500000234'),
('100', '0L', 'US01', '2026', '1500000233', '000001', '0002100000', NULL, 12400.00, 'USD', 'S', '20260925', '009', 'K', '0000100100', NULL, NULL, 'HCF-10277', 'Payment HCF-10277', 'BKPF', '1500000233'),
('100', '0L', 'US01', '2026', '1500000233', '000002', '0001131000', NULL, -12400.00, 'USD', 'H', '20260925', '009', 'S', NULL, NULL, NULL, 'HCF-10277', 'Payment HCF-10277', 'BKPF', '1500000233'),
('100', '0L', 'US01', '2026', '1900000041', '000001', '0006300100', 'CC-US10-150', 48200.00, 'USD', 'S', '20260731', '007', 'S', NULL, NULL, NULL, NULL, 'Q2 utilities true-up accrual, Austin plant', 'BKPF', '1900000041'),
('100', '0L', 'US01', '2026', '1900000041', '000002', '0002100500', NULL, -48200.00, 'USD', 'H', '20260731', '007', 'S', NULL, NULL, NULL, NULL, 'Q2 utilities true-up accrual, Austin plant', 'BKPF', '1900000041'),
('100', '0L', 'US01', '2026', '1900000047', '000001', '0005100115', 'CC-US10-115', 86500.00, 'USD', 'S', '20260831', '008', 'S', NULL, NULL, NULL, NULL, 'Reclass cell therapy costs from CC-110 to CC-115', 'BKPF', '1900000047'),
('100', '0L', 'US01', '2026', '1900000047', '000002', '0005100110', NULL, -86500.00, 'USD', 'H', '20260831', '008', 'S', NULL, NULL, NULL, NULL, 'Reclass cell therapy costs from CC-110 to CC-115', 'BKPF', '1900000047'),
('100', '0L', 'US01', '2026', '1900000055', '000001', '0006400100', 'CC-US10-150', 38900.00, 'USD', 'S', '20260930', '009', 'S', NULL, NULL, NULL, NULL, 'Accrue Sep calibration and facilities services', 'BKPF', '1900000055'),
('100', '0L', 'US01', '2026', '1900000055', '000002', '0002100500', NULL, -38900.00, 'USD', 'H', '20260930', '009', 'S', NULL, NULL, NULL, NULL, 'Accrue Sep calibration and facilities services', 'BKPF', '1900000055'),
('100', '0L', 'US01', '2026', '9400000001', '000001', '0001200000', NULL, 148000.00, 'USD', 'S', '20260729', '007', 'D', NULL, '0000200040', NULL, 'AR-26-10431', 'Billing 9000000518 for TO-26-0015', 'VBRK', '9000000518'),
('100', '0L', 'US01', '2026', '9400000001', '000002', '0004000300', NULL, -148000.00, 'USD', 'H', '20260729', '007', 'S', NULL, NULL, 'AU-7710', 'AR-26-10431', 'Billing 9000000518 for TO-26-0015', 'VBRK', '9000000518'),
('100', '0L', 'US01', '2026', '9400000002', '000001', '0001200000', NULL, 148000.00, 'USD', 'S', '20260825', '008', 'D', NULL, '0000200070', NULL, 'AR-26-10434', 'Billing 9000000521 for TO-26-0016', 'VBRK', '9000000521'),
('100', '0L', 'US01', '2026', '9400000002', '000002', '0004000300', NULL, -148000.00, 'USD', 'H', '20260825', '008', 'S', NULL, NULL, 'AU-7710', 'AR-26-10434', 'Billing 9000000521 for TO-26-0016', 'VBRK', '9000000521'),
('100', '0L', 'US01', '2026', '9400000003', '000001', '0001200000', NULL, 148000.00, 'USD', 'S', '20260916', '009', 'D', NULL, '0000200040', NULL, 'AR-26-10437', 'Billing 9000000524 for TO-26-0017', 'VBRK', '9000000524'),
('100', '0L', 'US01', '2026', '9400000003', '000002', '0004000300', NULL, -148000.00, 'USD', 'H', '20260916', '009', 'S', NULL, NULL, 'AU-7710', 'AR-26-10437', 'Billing 9000000524 for TO-26-0017', 'VBRK', '9000000524')
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
COMMENT ON TABLE sap_s4hana.vbkpf IS 'Parked document headers (landed with history: rows are retained after the document is posted; bstat V = still parked).';

INSERT INTO sap_s4hana.vbkpf (mandt, bukrs, belnr, gjahr, blart, budat, monat, usnam, cpudt, cputm, bktxt, bstat) VALUES
('100', 'US01', '1900000041', '2026', 'SA', '20260731', '07', 'LCARRANZA', '20260803', '094000', 'Q2 utilities true-up accrual, Austin plant', ' '),
('100', 'US01', '1900000047', '2026', 'SA', '20260831', '08', 'LCARRANZA', '20260901', '160500', 'Reclass cell therapy costs from CC-110 to CC-115', ' '),
('100', 'US01', '1900000055', '2026', 'SA', '20260930', '09', 'LCARRANZA', '20260928', '103000', 'Accrue Sep calibration and facilities services', ' '),
('100', 'US01', '1900000058', '2026', 'SA', '20260930', '09', 'LCARRANZA', '20260929', '141000', 'Capitalise validation consultant fees to CIP', 'V'),
('100', 'US01', '1900000059', '2026', 'SA', '20260930', '09', 'LCARRANZA', '20260930', '114500', 'Revenue cut-off: accrue Dendrivax order TO-26-0018', 'V')
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
('100', 'US01', '1900000041', '2026', '001', '0006300100', 'S', 48200.00, 'CC-US10-150'),
('100', 'US01', '1900000041', '2026', '002', '0002100500', 'H', 48200.00, NULL),
('100', 'US01', '1900000047', '2026', '001', '0005100115', 'S', 86500.00, 'CC-US10-115'),
('100', 'US01', '1900000047', '2026', '002', '0005100110', 'H', 86500.00, NULL),
('100', 'US01', '1900000055', '2026', '001', '0006400100', 'S', 38900.00, 'CC-US10-150'),
('100', 'US01', '1900000055', '2026', '002', '0002100500', 'H', 38900.00, NULL),
('100', 'US01', '1900000058', '2026', '001', '0001600900', 'S', 64000.00, 'CC-US10-150'),
('100', 'US01', '1900000058', '2026', '002', '0006200300', 'H', 64000.00, NULL),
('100', 'US01', '1900000059', '2026', '001', '0001200100', 'S', 148000.00, NULL),
('100', 'US01', '1900000059', '2026', '002', '0004000300', 'H', 148000.00, NULL)
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
COMMENT ON TABLE sap_s4hana.swwwihead IS 'Workflow work items of the parked journal approval step (flexible workflow for G/L documents); decision and note flattened from the container.';

INSERT INTO sap_s4hana.swwwihead (wi_id, wi_type, wi_rh_task, wi_text, wi_stat, wi_cd, wi_ct, wi_aed, wi_aet, wi_aagent, wi_result, wi_result_note) VALUES
(4400127, 'W', 'TS78500112', 'Approve parked G/L document 1900000041 (48200.00 USD)', 'COMPLETED', '20260803', '094000', '20260803', '152000', 'HKOWALSKI', 'APPROVE', NULL),
(4400134, 'W', 'TS78500112', 'Approve parked G/L document 1900000047 (86500.00 USD)', 'COMPLETED', '20260901', '160500', '20260902', '100500', 'HKOWALSKI', 'APPROVE', 'Supported by UKG labour distribution report'),
(4400141, 'W', 'TS78500112', 'Approve parked G/L document 1900000055 (38900.00 USD)', 'COMPLETED', '20260928', '103000', '20260928', '164000', 'HKOWALSKI', 'REWORK', 'Attach service entry sheets for the Hill Country work'),
(4400148, 'W', 'TS78500112', 'Approve parked G/L document 1900000055 (38900.00 USD)', 'COMPLETED', '20260928', '103000', '20260929', '111500', 'HKOWALSKI', 'APPROVE', NULL),
(4400155, 'W', 'TS78500112', 'Approve parked G/L document 1900000058 (64000.00 USD)', 'COMPLETED', '20260929', '141000', '20260929', '173000', 'HKOWALSKI', 'REJECT', 'Validation of existing equipment is not capitalisable; expense as incurred'),
(4400162, 'W', 'TS78500112', 'Approve parked G/L document 1900000059 (148000.00 USD)', 'READY', '20260930', '114500', NULL, NULL, NULL, NULL, NULL)
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
(4400127, 'BO', 'FIPP', 'US0119000000412026'),
(4400134, 'BO', 'FIPP', 'US0119000000472026'),
(4400141, 'BO', 'FIPP', 'US0119000000552026'),
(4400148, 'BO', 'FIPP', 'US0119000000552026'),
(4400155, 'BO', 'FIPP', 'US0119000000582026'),
(4400162, 'BO', 'FIPP', 'US0119000000592026')
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
COMMENT ON TABLE sap_s4hana.reguh IS 'Payment run settlement data per payee and payment document (payee bank as used; zz_spl_status = sanctioned-party screening result read on the payment proposal: C clear, R under review, B blocked).';

INSERT INTO sap_s4hana.reguh (mandt, laufd, laufi, xvorl, zbukr, lifnr, vblnr, waers, rbetr, zbnks, zbnky, zbnkn, ziban, ubhkt, zaldt, zz_spl_status) VALUES
('100', '20260716', 'AUS01', '', 'US01', '0000100120', '1500000194', 'USD', -34000.00, 'US', '113000023', '8810023347', NULL, '0001131000', '20260716', 'C'),
('100', '20260724', 'AUS02', '', 'US01', '0000100040', '1500000198', 'USD', -4800.00, 'DE', NULL, NULL, 'DE44500105175407324931', '0001131000', '20260724', 'C'),
('100', '20260724', 'AUS02', '', 'US01', '0000100050', '1500000199', 'USD', -560.00, 'US', '021000021', '4471902233', NULL, '0001131000', '20260724', 'C'),
('100', '20260814', 'AUS03', '', 'US01', '0000100060', '1500000207', 'USD', -3360.00, 'US', '026009593', '0038812765', NULL, '0001131000', '20260814', 'C'),
('100', '20260821', 'AUS04', '', 'US01', '0000100010', '1500000211', 'USD', -77500.00, 'CN', 'BOCH', '7710044581230', NULL, '0001131000', '20260821', 'C'),
('100', '20260911', 'AUS05', '', 'US01', '0000100030', '1500000224', 'USD', -57000.00, 'DE', NULL, NULL, 'DE89370400440532013000', '0001131000', '20260911', 'C'),
('100', '20260911', 'AUS05', '', 'US01', '0000100090', '1500000225', 'USD', -6850.00, 'US', '111000025', '3319002871', NULL, '0001131000', '20260911', 'C'),
('100', '20260917', 'AUS06', '', 'US01', '0000100050', '1500000229', 'USD', -45600.00, 'US', '021000021', '4471902233', NULL, '0001131000', '20260917', 'C'),
('100', '20260925', 'AUS07', '', 'US01', '0000100110', '1500000234', 'USD', -9300.00, 'US', '111000614', '6603391452', NULL, '0001131000', '20260925', 'C'),
('100', '20260925', 'AUS07', '', 'US01', '0000100100', '1500000233', 'USD', -12400.00, 'US', '114000093', '2208847710', NULL, '0001131000', '20260925', 'R')
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
COMMENT ON TABLE sap_s4hana.regup IS 'Items paid by each payment document (belnr = invoice document, xblnr = supplier invoice number).';

INSERT INTO sap_s4hana.regup (mandt, laufd, laufi, xvorl, zbukr, lifnr, vblnr, bukrs, belnr, gjahr, buzei, xblnr, dmbtr) VALUES
('100', '20260716', 'AUS01', '', 'US01', '0000100120', '1500000194', 'US01', '5105600001', '2026', '002', 'GCC-26-0615', 34000.00),
('100', '20260724', 'AUS02', '', 'US01', '0000100040', '1500000198', 'US01', '5105600003', '2026', '002', 'DFE-90412277', 4800.00),
('100', '20260724', 'AUS02', '', 'US01', '0000100050', '1500000199', 'US01', '5105600004', '2026', '002', 'SPC-INV-558812', 560.00),
('100', '20260814', 'AUS03', '', 'US01', '0000100060', '1500000207', 'US01', '5105600006', '2026', '002', 'SCH-US-3310027', 3360.00),
('100', '20260821', 'AUS04', '', 'US01', '0000100010', '1500000211', 'US01', '5105600002', '2026', '002', 'HH-INV-260611', 77500.00),
('100', '20260911', 'AUS05', '', 'US01', '0000100030', '1500000224', 'US01', '5105600005', '2026', '002', 'HPM-2026-07-1188', 57000.00),
('100', '20260911', 'AUS05', '', 'US01', '0000100090', '1500000225', 'US01', '5105600008', '2026', '002', 'LCS-2026-0814', 6850.00),
('100', '20260917', 'AUS06', '', 'US01', '0000100050', '1500000229', 'US01', '5105600009', '2026', '002', 'SPC-INV-561470', 45600.00),
('100', '20260925', 'AUS07', '', 'US01', '0000100110', '1500000234', 'US01', '5105600010', '2026', '002', 'LBL-88213', 9300.00),
('100', '20260925', 'AUS07', '', 'US01', '0000100100', '1500000233', 'US01', '5105600011', '2026', '002', 'HCF-10277', 12400.00)
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
COMMENT ON TABLE sap_s4hana.bnk_batch_header IS 'Bank Communication Management payment batches; status IBC11 = approved and sent, chusr = final approver.';

INSERT INTO sap_s4hana.bnk_batch_header (mandt, batch_no, laufd, laufi, zbukr, status, chusr, chdate, chtime) VALUES
('100', 'B2600001', '20260716', 'AUS01', 'US01', 'IBC11', 'HKOWALSKI', '20260716', '053000'),
('100', 'B2600002', '20260724', 'AUS02', 'US01', 'IBC11', 'HKOWALSKI', '20260724', '052000'),
('100', 'B2600003', '20260814', 'AUS03', 'US01', 'IBC11', 'HKOWALSKI', '20260814', '054000'),
('100', 'B2600004', '20260821', 'AUS04', 'US01', 'IBC11', 'RHERNANDEZ', '20260821', '053000'),
('100', 'B2600005', '20260911', 'AUS05', 'US01', 'IBC11', 'HKOWALSKI', '20260911', '052000'),
('100', 'B2600006', '20260917', 'AUS06', 'US01', 'IBC11', 'HKOWALSKI', '20260917', '054000'),
('100', 'B2600007', '20260925', 'AUS07', 'US01', 'IBC11', 'HKOWALSKI', '20260925', '053000')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/sap_s4hana).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS sap_s4hana.lfa1 (
  mandt            varchar(3) NOT NULL,
  lifnr            varchar(10) NOT NULL,
  name1            varchar(80) NOT NULL,
  land1            varchar(3) NOT NULL,
  ktokk            varchar(4) NOT NULL,
  sperr            varchar(1) NOT NULL,
  loevm            varchar(1) NOT NULL,
  zz_approved_on   varchar(8),
  zz_spl_status    varchar(1),
  zz_spl_date      varchar(8),
  zz_risk_rating   varchar(10),
  zz_screening_ref varchar(40),
  zz_anomaly_ref   varchar(40),
  CONSTRAINT lfa1_pk PRIMARY KEY (mandt, lifnr)
);
COMMENT ON TABLE sap_s4hana.lfa1 IS 'Vendor master general data (ktokk ZMAT material / ZOTH other; sperr posting block; zz_spl_status C clear, R review, B blocked as read by the payment proposal), from Supplier Master Data.';

CREATE TABLE IF NOT EXISTS sap_s4hana.lfbk (
  mandt          varchar(3) NOT NULL,
  lifnr          varchar(10) NOT NULL,
  banks          varchar(3) NOT NULL,
  bvtyp          varchar(4) NOT NULL,
  bankl          varchar(15),
  bankn          varchar(35),
  iban           varchar(34),
  zz_bank_name   varchar(60),
  zz_change_ref  varchar(40) NOT NULL,
  zz_verified_on varchar(8) NOT NULL,
  CONSTRAINT lfbk_pk PRIMARY KEY (mandt, lifnr, bvtyp)
);
COMMENT ON TABLE sap_s4hana.lfbk IS 'Vendor master bank details: the verified remittance account and the change request that set it, from Supplier Master Data.';

CREATE TABLE IF NOT EXISTS sap_s4hana.bapi2017_gm_head_01 (
  mandt      varchar(3) NOT NULL,
  ref_doc_no varchar(40) NOT NULL,
  gm_code    varchar(2) NOT NULL,
  pstng_date varchar(8) NOT NULL,
  doc_date   varchar(8) NOT NULL,
  header_txt varchar(25),
  zz_status  varchar(1) NOT NULL,
  CONSTRAINT bapi2017_gm_head_01_pk PRIMARY KEY (mandt, ref_doc_no)
);
COMMENT ON TABLE sap_s4hana.bapi2017_gm_head_01 IS 'Staged goods movement headers for BAPI_GOODSMVT_CREATE (gm_code 01 goods receipt for purchase order; zz_status R ready, P posted, E error), from Goods Receipts and Purchase Orders And Receipts.';

CREATE TABLE IF NOT EXISTS sap_s4hana.bapi2017_gm_item_create (
  mandt      varchar(3) NOT NULL,
  ref_doc_no varchar(40) NOT NULL,
  line_id    varchar(6) NOT NULL,
  material   varchar(40),
  plant      varchar(4) NOT NULL,
  stge_loc   varchar(4),
  batch      varchar(40),
  move_type  varchar(3) NOT NULL,
  stck_type  varchar(1),
  entry_qnt  numeric(13,3) NOT NULL,
  po_number  varchar(40),
  po_item    varchar(5),
  vendor     varchar(10),
  zz_cert_no varchar(40),
  CONSTRAINT bapi2017_gm_item_create_pk PRIMARY KEY (mandt, ref_doc_no, line_id)
);
COMMENT ON TABLE sap_s4hana.bapi2017_gm_item_create IS 'Staged goods movement items for BAPI_GOODSMVT_CREATE (move_type 101; stck_type Q = quality inspection stock).';

CREATE TABLE IF NOT EXISTS sap_s4hana.bapi2045d2 (
  mandt          varchar(3) NOT NULL,
  insplot        varchar(12) NOT NULL,
  inspoper       varchar(4) NOT NULL,
  inspchar       varchar(40) NOT NULL,
  mean_value     varchar(60) NOT NULL,
  meas_unit      varchar(20),
  evaluation     varchar(1) NOT NULL,
  zz_spec_min    varchar(60),
  zz_spec_max    varchar(60),
  zz_tested_at   timestamptz NOT NULL,
  inspector      varchar(12) NOT NULL,
  zz_lims_result varchar(40) NOT NULL,
  CONSTRAINT bapi2045d2_pk PRIMARY KEY (mandt, insplot, inspoper, inspchar)
);
COMMENT ON TABLE sap_s4hana.bapi2045d2 IS 'Staged characteristic results for BAPI_INSPOPER_RECORDRESULTS (evaluation A accepted, R rejected) against goods receipt inspection lots, from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS sap_s4hana.bapimepoheader (
  mandt           varchar(3) NOT NULL,
  po_number       varchar(40) NOT NULL,
  comp_code       varchar(4) NOT NULL,
  doc_type        varchar(4) NOT NULL,
  vendor          varchar(10) NOT NULL,
  doc_date        varchar(8) NOT NULL,
  currency        varchar(5) NOT NULL,
  zz_total_amount numeric(18,2) NOT NULL,
  zz_approver     varchar(12) NOT NULL,
  zz_status       varchar(20) NOT NULL,
  CONSTRAINT bapimepoheader_pk PRIMARY KEY (mandt, po_number)
);
COMMENT ON TABLE sap_s4hana.bapimepoheader IS 'Staged purchase order headers for BAPI_PO_CREATE1, from Purchase Orders And Receipts.';

CREATE TABLE IF NOT EXISTS sap_s4hana.bapiache09 (
  mandt      varchar(3) NOT NULL,
  obj_type   varchar(5) NOT NULL,
  obj_key    varchar(60) NOT NULL,
  obj_sys    varchar(10) NOT NULL,
  bus_act    varchar(4) NOT NULL,
  username   varchar(12) NOT NULL,
  header_txt varchar(25),
  comp_code  varchar(4) NOT NULL,
  doc_date   varchar(8),
  pstng_date varchar(8),
  fisc_year  varchar(4),
  fis_period varchar(3),
  doc_type   varchar(2) NOT NULL,
  ref_doc_no varchar(16),
  currency   varchar(5) NOT NULL,
  zz_status  varchar(1) NOT NULL,
  CONSTRAINT bapiache09_pk PRIMARY KEY (mandt, obj_type, obj_key)
);
COMMENT ON TABLE sap_s4hana.bapiache09 IS 'Staged accounting document headers for BAPI_ACC_DOCUMENT_POST (obj_type ZEXP expense claim, ZPAY payroll run, ZINV supplier invoice, ZBIL treatment invoice; zz_status R ready, P posted, E error), from Employee Expense Claims, Payroll Results, Supplier Payments and Treatment Invoices.';

CREATE TABLE IF NOT EXISTS sap_s4hana.bapiacgl09 (
  mandt      varchar(3) NOT NULL,
  obj_type   varchar(5) NOT NULL,
  obj_key    varchar(60) NOT NULL,
  itemno_acc varchar(10) NOT NULL,
  gl_account varchar(10),
  item_text  varchar(50),
  costcenter varchar(20),
  vendor_no  varchar(10),
  customer   varchar(10),
  amt_doccur numeric(23,2) NOT NULL,
  alloc_nmbr varchar(18),
  CONSTRAINT bapiacgl09_pk PRIMARY KEY (mandt, obj_type, obj_key, itemno_acc)
);
COMMENT ON TABLE sap_s4hana.bapiacgl09 IS 'Staged accounting document lines for BAPI_ACC_DOCUMENT_POST (amount in document currency from BAPIACCR09, debit positive; G/L account left empty where account determination assigns it).';

CREATE TABLE IF NOT EXISTS sap_s4hana.zpp_pseudonym_link (
  mandt                varchar(3) NOT NULL,
  zz_patient_pseudonym varchar(40) NOT NULL,
  zz_treatment_order   varchar(20) NOT NULL,
  matnr                varchar(40) NOT NULL,
  issued_date          varchar(8) NOT NULL,
  issued_time          varchar(6) NOT NULL,
  zz_patient_params    varchar(255),
  CONSTRAINT zpp_pseudonym_link_pk PRIMARY KEY (mandt, zz_patient_pseudonym)
);
COMMENT ON TABLE sap_s4hana.zpp_pseudonym_link IS 'Patient pseudonym to treatment order links from which planning creates the ZPAT process order, from Patient Pseudonym Register.';

CREATE TABLE IF NOT EXISTS sap_s4hana.zsd_therapy_pod (
  mandt                varchar(3) NOT NULL,
  charg                varchar(40) NOT NULL,
  zz_treatment_order   varchar(20) NOT NULL,
  zz_patient_pseudonym varchar(40) NOT NULL,
  pod_date             varchar(8),
  pod_time             varchar(6),
  pod_location         varchar(60),
  admin_date           varchar(8),
  admin_time           varchar(6),
  admin_npi            varchar(40),
  CONSTRAINT zsd_therapy_pod_pk PRIMARY KEY (mandt, charg)
);
COMMENT ON TABLE sap_s4hana.zsd_therapy_pod IS 'Proof of delivery and of administration per patient therapy batch, releasing the billing due list, from Therapy Delivery Events.';

GRANT USAGE ON SCHEMA sap_s4hana TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA sap_s4hana TO egeria_user, airflow_user;
