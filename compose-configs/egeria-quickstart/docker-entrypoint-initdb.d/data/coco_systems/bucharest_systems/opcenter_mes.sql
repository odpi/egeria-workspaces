-- system-qualified-name: SoftwareServer::SYS-003::Siemens Opcenter MES
-- Siemens Opcenter MES - Bucharest.  Opcenter Execution Pharma for the EKG sterile lines and the autologous serum
-- suite (plant RO10): batches (containers), executed steps with electronic signatures, component issues, equipment
-- use, the electronic batch record and QP release, and the dispatch monitoring of cold chain shipments fed by Proact.
-- Its tables feed Batch Execution Records, Electronic Batch Records, Batch Certification Decisions (review by
-- exception), Cold Chain Transit Records and Carrier Transit Events.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS opcenter_mes;
COMMENT ON SCHEMA opcenter_mes IS 'Siemens Opcenter Execution Pharma (EKG, Bucharest): containers, step history, component issue and resource usage history, EBR header/section references, batch release history and shipment monitoring, as landed by the MES reporting database replica (UTC).';

CREATE TABLE IF NOT EXISTS opcenter_mes.product (
  productid       varchar(16) NOT NULL,
  productname     varchar(40) NOT NULL,
  productrevision varchar(10) NOT NULL,
  description     varchar(255),
  CONSTRAINT product_pk PRIMARY KEY (productid)
);
COMMENT ON TABLE opcenter_mes.product IS 'Products (product name = SAP material number).';

INSERT INTO opcenter_mes.product (productid, productname, productrevision, description) VALUES
('PRD00001', 'PF-1101', 'C', 'Oxitocină EKG 5 UI/ml soluție injectabilă'),
('PRD00002', 'PF-1102', 'A', 'Ceftriaxonă EKG 1 g pulbere pentru soluție injectabilă/perfuzabilă'),
('PRD00003', 'PF-1103', 'B', 'Metoclopramid EKG 10 mg/2 ml soluție injectabilă'),
('PRD00004', 'PF-1104', 'A', 'Ondansetron EKG 4 mg/2 ml soluție injectabilă'),
('PRD00005', 'PF-1105', 'D', 'Octreotidă EKG 0,1 mg/ml soluție injectabilă'),
('PRD00006', 'PF-9101', 'B', 'Ser autolog EKG 20% picături oftalmice (pacient nominal)')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.container (
  containerid      varchar(16) NOT NULL,
  containername    varchar(40) NOT NULL,
  productid        varchar(16) NOT NULL,
  mfgordername     varchar(20),
  qty              numeric(12,2) NOT NULL,
  uom              varchar(10) NOT NULL,
  status           varchar(20) NOT NULL,
  startdate        timestamptz NOT NULL,
  enddate          timestamptz,
  patientpseudonym varchar(40),
  CONSTRAINT container_pk PRIMARY KEY (containerid)
);
COMMENT ON TABLE opcenter_mes.container IS 'Batches (containers); manufacturing order = SAP process order; patient pseudonym only on named-patient serum batches.';

INSERT INTO opcenter_mes.container (containerid, containername, productid, mfgordername, qty, uom, status, startdate, enddate, patientpseudonym) VALUES
('CNT000301', 'EK26-0311', 'PRD00001', '4000311', 24000, 'BUC', 'Closed', '2026-07-06 06:00:00+00', '2026-07-08 16:00:00+00', NULL),
('CNT000302', 'EK26-0318', 'PRD00002', '4000318', 15000, 'BUC', 'Closed', '2026-07-20 06:00:00+00', '2026-07-22 14:00:00+00', NULL),
('CNT000303', 'EK26-0324', 'PRD00005', '4000324', 8000, 'BUC', 'Closed', '2026-08-03 06:00:00+00', '2026-08-05 15:00:00+00', NULL),
('CNT000304', 'EK26-0329', 'PRD00001', '4000329', 30000, 'BUC', 'Closed', '2026-08-17 06:00:00+00', '2026-08-19 16:00:00+00', NULL),
('CNT000305', 'EK26-0335', 'PRD00003', '4000335', 30000, 'BUC', 'Closed', '2026-08-31 06:00:00+00', '2026-09-02 16:00:00+00', NULL),
('CNT000306', 'EK26-0341', 'PRD00004', '4000341', 20000, 'BUC', 'Closed', '2026-09-14 06:00:00+00', '2026-09-16 15:00:00+00', NULL),
('CNT000307', 'EK26-0347', 'PRD00002', '4000347', 15000, 'BUC', 'Active', '2026-09-28 06:00:00+00', NULL, NULL),
('CNT000308', 'SA26-0031', 'PRD00006', '4100031', 56, 'BUC', 'Closed', '2026-07-14 12:00:00+00', '2026-07-15 16:00:00+00', 'PP-993A9A3720FB'),
('CNT000309', 'SA26-0034', 'PRD00006', '4100034', 56, 'BUC', 'Closed', '2026-08-04 13:00:00+00', '2026-08-05 17:00:00+00', 'PP-385F3C95C17E'),
('CNT000310', 'SA26-0037', 'PRD00006', '4100037', 56, 'BUC', 'Closed', '2026-08-26 07:00:00+00', '2026-08-27 12:00:00+00', 'PP-7A15F037482B'),
('CNT000311', 'SA26-0040', 'PRD00006', '4100040', 56, 'BUC', 'Closed', '2026-09-16 07:00:00+00', '2026-09-17 12:00:00+00', 'PP-52094070B986'),
('CNT000312', 'SA26-0042', 'PRD00006', '4100042', 56, 'BUC', 'Active', '2026-09-29 13:00:00+00', NULL, 'PP-22773F9CC79C')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.spec (
  specid       varchar(16) NOT NULL,
  specname     varchar(40) NOT NULL,
  specrevision varchar(10) NOT NULL,
  description  varchar(255),
  CONSTRAINT spec_pk PRIMARY KEY (specid)
);
COMMENT ON TABLE opcenter_mes.spec IS 'Process step specifications.';

INSERT INTO opcenter_mes.spec (specid, specname, specrevision, description) VALUES
('SPC0001', 'DISPENSE', 'A', 'Dispense step'),
('SPC0002', 'COMPOUND', 'A', 'Compound step'),
('SPC0003', 'FILL', 'A', 'Fill step'),
('SPC0004', 'INSPECT_PACK', 'A', 'Inspect pack step'),
('SPC0005', 'STERILISE', 'A', 'Sterilise step'),
('SPC0006', 'SEPARATE', 'A', 'Separate step'),
('SPC0007', 'DILUTE_FILL', 'A', 'Dilute fill step'),
('SPC0008', 'FREEZE', 'A', 'Freeze step')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.resourcedef (
  resourceid   varchar(16) NOT NULL,
  resourcename varchar(40) NOT NULL,
  description  varchar(255),
  resourcetype varchar(40),
  CONSTRAINT resourcedef_pk PRIMARY KEY (resourceid)
);
COMMENT ON TABLE opcenter_mes.resourcedef IS 'Equipment resources (resource name = Maximo asset number).';

INSERT INTO opcenter_mes.resourcedef (resourceid, resourcename, description, resourcetype) VALUES
('RES0001', 'RO10-AMP-01', 'Linie umplere și sudare fiole', 'Ampoule filling line'),
('RES0002', 'RO10-AUT-01', 'Autoclavă sterilizare cu abur 1', 'Steam steriliser'),
('RES0003', 'RO10-AUT-02', 'Autoclavă sterilizare cu abur 2', 'Steam steriliser'),
('RES0004', 'RO10-BSC-01', 'Hotă flux laminar clasa A, laborator ser', 'Biosafety cabinet'),
('RES0005', 'RO10-CEN-01', 'Centrifugă refrigerată', 'Centrifuge'),
('RES0006', 'RO10-CMX-01', 'Vas de preparare soluții 300 L', 'Compounding vessel'),
('RES0007', 'RO10-DSP-01', 'Cabină de cântărire cu flux laminar', 'Dispensing booth'),
('RES0008', 'RO10-FLT-01', 'Skid filtrare sterilă 0,22 µm', 'Filtration skid'),
('RES0009', 'RO10-FRZ-01', 'Congelator -40 °C', 'Freezer'),
('RES0010', 'RO10-PKG-01', 'Linie ambalare și serializare', 'Packaging line'),
('RES0011', 'RO10-VFL-01', 'Linie umplere pulberi sterile în flacoane', 'Powder filling line'),
('RES0012', 'RO10-VIS-01', 'Mașină inspecție vizuală automată', 'Inspection machine')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.employee (
  employeeid     varchar(16) NOT NULL,
  employeename   varchar(40) NOT NULL,
  fullname       varchar(120),
  employeenumber varchar(20) NOT NULL,
  CONSTRAINT employee_pk PRIMARY KEY (employeeid)
);
COMMENT ON TABLE opcenter_mes.employee IS 'MES users (employee name = AD login via LDAP, employee number = Workday employee ID).';

INSERT INTO opcenter_mes.employee (employeeid, employeename, fullname, employeenumber) VALUES
('EMP0001', 'noprea', 'Nicoleta Oprea', '20017'),
('EMP0002', 'bionescu', 'Bogdan Ionescu', '20058'),
('EMP0003', 'adinu', 'Alexandru Dinu', '20061'),
('EMP0004', 'cmarin', 'Cătălina Marin', '20063'),
('EMP0005', 'vgeorgescu', 'Vlad Georgescu', '20066'),
('EMP0006', 'renache', 'Raluca Enache', '20069'),
('EMP0007', 'spavel', 'Ștefan Pavel', '20086')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.historymainline (
  historymainlineid varchar(16) NOT NULL,
  containerid       varchar(16) NOT NULL,
  specid            varchar(16) NOT NULL,
  stepsequence      integer NOT NULL,
  moveindate        timestamptz NOT NULL,
  moveoutdate       timestamptz,
  employeeid        varchar(16) NOT NULL,
  esigemployeeid    varchar(16),
  esigmeaning       varchar(60),
  esigdate          timestamptz,
  txnstatus         varchar(30) NOT NULL,
  CONSTRAINT historymainline_pk PRIMARY KEY (historymainlineid)
);
COMMENT ON TABLE opcenter_mes.historymainline IS 'Step execution history: move-in/move-out per step with the performer and the verifier''s electronic signature.';

INSERT INTO opcenter_mes.historymainline (historymainlineid, containerid, specid, stepsequence, moveindate, moveoutdate, employeeid, esigemployeeid, esigmeaning, esigdate, txnstatus) VALUES
('HML0000001', 'CNT000301', 'SPC0001', 1, '2026-07-06 06:00:00+00', '2026-07-06 20:10:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-07-06 20:16:00+00', 'Completed'),
('HML0000002', 'CNT000301', 'SPC0002', 2, '2026-07-06 20:45:00+00', '2026-07-07 10:40:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-07-07 10:46:00+00', 'Completed'),
('HML0000003', 'CNT000301', 'SPC0003', 3, '2026-07-07 11:15:00+00', '2026-07-08 01:10:00+00', 'EMP0003', 'EMP0005', 'Verificat', '2026-07-08 01:16:00+00', 'Completed'),
('HML0000004', 'CNT000301', 'SPC0004', 4, '2026-07-08 01:45:00+00', '2026-07-08 16:00:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-07-08 16:06:00+00', 'Completed'),
('HML0000005', 'CNT000302', 'SPC0001', 1, '2026-07-20 06:00:00+00', '2026-07-21 00:20:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-07-21 00:26:00+00', 'Completed'),
('HML0000006', 'CNT000302', 'SPC0003', 2, '2026-07-21 00:55:00+00', '2026-07-21 19:00:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-07-21 19:06:00+00', 'Completed'),
('HML0000007', 'CNT000302', 'SPC0004', 3, '2026-07-21 19:35:00+00', '2026-07-22 14:00:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-07-22 14:06:00+00', 'Completed'),
('HML0000008', 'CNT000303', 'SPC0001', 1, '2026-08-03 06:00:00+00', '2026-08-03 19:55:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-08-03 20:01:00+00', 'Completed'),
('HML0000009', 'CNT000303', 'SPC0002', 2, '2026-08-03 20:30:00+00', '2026-08-04 10:10:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-08-04 10:16:00+00', 'Completed'),
('HML0000010', 'CNT000303', 'SPC0003', 3, '2026-08-04 10:45:00+00', '2026-08-05 00:25:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-08-05 00:31:00+00', 'Completed'),
('HML0000011', 'CNT000303', 'SPC0004', 4, '2026-08-05 01:00:00+00', '2026-08-05 15:00:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-08-05 15:06:00+00', 'Completed'),
('HML0000012', 'CNT000304', 'SPC0001', 1, '2026-08-17 06:00:00+00', '2026-08-17 20:10:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-08-17 20:16:00+00', 'Completed'),
('HML0000013', 'CNT000304', 'SPC0002', 2, '2026-08-17 20:45:00+00', '2026-08-18 10:40:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-08-18 10:46:00+00', 'Completed'),
('HML0000014', 'CNT000304', 'SPC0003', 3, '2026-08-18 11:15:00+00', '2026-08-19 01:10:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-08-19 01:16:00+00', 'CompletedWithException'),
('HML0000015', 'CNT000304', 'SPC0004', 4, '2026-08-19 01:45:00+00', '2026-08-19 16:00:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-08-19 16:06:00+00', 'Completed'),
('HML0000016', 'CNT000305', 'SPC0001', 1, '2026-08-31 06:00:00+00', '2026-08-31 17:16:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-08-31 17:22:00+00', 'Completed'),
('HML0000017', 'CNT000305', 'SPC0002', 2, '2026-08-31 17:51:00+00', '2026-09-01 04:52:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-09-01 04:58:00+00', 'Completed'),
('HML0000018', 'CNT000305', 'SPC0003', 3, '2026-09-01 05:27:00+00', '2026-09-01 16:28:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-09-01 16:34:00+00', 'Completed'),
('HML0000019', 'CNT000305', 'SPC0005', 4, '2026-09-01 17:03:00+00', '2026-09-02 04:04:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-09-02 04:10:00+00', 'Completed'),
('HML0000020', 'CNT000305', 'SPC0004', 5, '2026-09-02 04:39:00+00', '2026-09-02 16:00:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-09-02 16:06:00+00', 'Completed'),
('HML0000021', 'CNT000306', 'SPC0001', 1, '2026-09-14 06:00:00+00', '2026-09-14 17:04:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-09-14 17:10:00+00', 'Completed'),
('HML0000022', 'CNT000306', 'SPC0002', 2, '2026-09-14 17:39:00+00', '2026-09-15 04:28:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-09-15 04:34:00+00', 'Completed'),
('HML0000023', 'CNT000306', 'SPC0003', 3, '2026-09-15 05:03:00+00', '2026-09-15 15:52:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-09-15 15:58:00+00', 'Completed'),
('HML0000024', 'CNT000306', 'SPC0005', 4, '2026-09-15 16:27:00+00', '2026-09-16 03:16:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-09-16 03:22:00+00', 'Completed'),
('HML0000025', 'CNT000306', 'SPC0004', 5, '2026-09-16 03:51:00+00', '2026-09-16 15:00:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-09-16 15:06:00+00', 'Completed'),
('HML0000026', 'CNT000307', 'SPC0001', 1, '2026-09-28 06:00:00+00', '2026-09-29 01:00:00+00', 'EMP0007', 'EMP0005', 'Verificat', '2026-09-29 01:06:00+00', 'Completed'),
('HML0000027', 'CNT000307', 'SPC0003', 2, '2026-09-29 01:35:00+00', '2026-09-29 20:20:00+00', 'EMP0002', 'EMP0005', 'Verificat', '2026-09-29 20:26:00+00', 'Completed'),
('HML0000028', 'CNT000307', 'SPC0004', 3, '2026-09-29 20:55:00+00', NULL, 'EMP0007', NULL, NULL, NULL, 'InProcess'),
('HML0000029', 'CNT000308', 'SPC0006', 1, '2026-07-14 12:00:00+00', '2026-07-14 21:00:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-07-14 21:06:00+00', 'Completed'),
('HML0000030', 'CNT000308', 'SPC0007', 2, '2026-07-14 21:35:00+00', '2026-07-15 06:20:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-07-15 06:26:00+00', 'Completed'),
('HML0000031', 'CNT000308', 'SPC0008', 3, '2026-07-15 06:55:00+00', '2026-07-15 16:00:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-07-15 16:06:00+00', 'Completed'),
('HML0000032', 'CNT000309', 'SPC0006', 1, '2026-08-04 13:00:00+00', '2026-08-04 22:00:00+00', 'EMP0003', 'EMP0006', 'Verificat', '2026-08-04 22:06:00+00', 'Completed'),
('HML0000033', 'CNT000309', 'SPC0007', 2, '2026-08-04 22:35:00+00', '2026-08-05 07:20:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-08-05 07:26:00+00', 'Completed'),
('HML0000034', 'CNT000309', 'SPC0008', 3, '2026-08-05 07:55:00+00', '2026-08-05 17:00:00+00', 'EMP0003', 'EMP0006', 'Verificat', '2026-08-05 17:06:00+00', 'Completed'),
('HML0000035', 'CNT000310', 'SPC0006', 1, '2026-08-26 07:00:00+00', '2026-08-26 16:20:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-08-26 16:26:00+00', 'Completed'),
('HML0000036', 'CNT000310', 'SPC0007', 2, '2026-08-26 16:55:00+00', '2026-08-27 02:00:00+00', 'EMP0003', 'EMP0006', 'Verificat', '2026-08-27 02:06:00+00', 'Completed'),
('HML0000037', 'CNT000310', 'SPC0008', 3, '2026-08-27 02:35:00+00', '2026-08-27 12:00:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-08-27 12:06:00+00', 'Completed'),
('HML0000038', 'CNT000311', 'SPC0006', 1, '2026-09-16 07:00:00+00', '2026-09-16 16:20:00+00', 'EMP0003', 'EMP0006', 'Verificat', '2026-09-16 16:26:00+00', 'CompletedWithException'),
('HML0000039', 'CNT000311', 'SPC0007', 2, '2026-09-16 16:55:00+00', '2026-09-17 02:00:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-09-17 02:06:00+00', 'Completed'),
('HML0000040', 'CNT000311', 'SPC0008', 3, '2026-09-17 02:35:00+00', '2026-09-17 12:00:00+00', 'EMP0003', 'EMP0006', 'Verificat', '2026-09-17 12:06:00+00', 'Completed'),
('HML0000041', 'CNT000312', 'SPC0006', 1, '2026-09-29 13:00:00+00', '2026-09-29 22:00:00+00', 'EMP0003', 'EMP0006', 'Verificat', '2026-09-29 22:06:00+00', 'Completed'),
('HML0000042', 'CNT000312', 'SPC0007', 2, '2026-09-29 22:35:00+00', '2026-09-30 07:20:00+00', 'EMP0004', 'EMP0006', 'Verificat', '2026-09-30 07:26:00+00', 'Completed'),
('HML0000043', 'CNT000312', 'SPC0008', 3, '2026-09-30 07:55:00+00', NULL, 'EMP0003', NULL, NULL, NULL, 'InProcess')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.componentissuehistory (
  historyid         varchar(16) NOT NULL,
  historymainlineid varchar(16) NOT NULL,
  issuedproductname varchar(40) NOT NULL,
  fromlot           varchar(40) NOT NULL,
  qtyissued         numeric(12,3) NOT NULL,
  uom               varchar(10) NOT NULL,
  CONSTRAINT componentissuehistory_pk PRIMARY KEY (historyid)
);
COMMENT ON TABLE opcenter_mes.componentissuehistory IS 'Component (raw material lot) issues recorded against a step (SAP units: G, KG, L, ST).';

INSERT INTO opcenter_mes.componentissuehistory (historyid, historymainlineid, issuedproductname, fromlot, qtyissued, uom) VALUES
('CIH000011', 'HML0000001', 'MP-10010', 'MP26-0061', 0.22, 'G'),
('CIH000012', 'HML0000001', 'MP-20010', 'MP26-0063', 0.22, 'KG'),
('CIH000013', 'HML0000001', 'AMB-30010', 'MP26-0064', 24600, 'ST'),
('CIH000051', 'HML0000005', 'MP-10020', 'MP26-0066', 15.3, 'KG'),
('CIH000052', 'HML0000005', 'AMB-30030', 'MP26-0067', 15400, 'ST'),
('CIH000081', 'HML0000008', 'MP-10050', 'MP26-0069', 0.82, 'G'),
('CIH000082', 'HML0000008', 'AMB-30010', 'MP26-0064', 8300, 'ST'),
('CIH000121', 'HML0000012', 'MP-10010', 'MP26-0061', 0.22, 'G'),
('CIH000122', 'HML0000012', 'MP-20010', 'MP26-0063', 0.22, 'KG'),
('CIH000123', 'HML0000012', 'AMB-30010', 'MP26-0064', 24600, 'ST'),
('CIH000161', 'HML0000016', 'MP-10030', 'MP26-0071', 0.31, 'KG'),
('CIH000162', 'HML0000016', 'MP-20010', 'MP26-0063', 0.5, 'KG'),
('CIH000163', 'HML0000016', 'AMB-30020', 'MP26-0072', 30800, 'ST'),
('CIH000211', 'HML0000021', 'MP-10040', 'MP26-0075', 0.08, 'KG'),
('CIH000212', 'HML0000021', 'MP-20010', 'MP26-0063', 0.36, 'KG'),
('CIH000213', 'HML0000021', 'AMB-30020', 'MP26-0072', 20600, 'ST'),
('CIH000261', 'HML0000026', 'MP-10020', 'MP26-0066', 15.3, 'KG'),
('CIH000262', 'HML0000026', 'AMB-30030', 'MP26-0067', 15400, 'ST'),
('CIH000291', 'HML0000029', 'MP-40010', 'MP25-0212', 0.2, 'L'),
('CIH000292', 'HML0000029', 'AMB-30050', 'MP25-0215', 60, 'ST'),
('CIH000321', 'HML0000032', 'MP-40010', 'MP25-0212', 0.2, 'L'),
('CIH000322', 'HML0000032', 'AMB-30050', 'MP25-0215', 60, 'ST'),
('CIH000351', 'HML0000035', 'MP-40010', 'MP25-0212', 0.2, 'L'),
('CIH000352', 'HML0000035', 'AMB-30050', 'MP25-0215', 60, 'ST'),
('CIH000381', 'HML0000038', 'MP-40010', 'MP25-0212', 0.2, 'L'),
('CIH000382', 'HML0000038', 'AMB-30050', 'MP25-0215', 60, 'ST'),
('CIH000411', 'HML0000041', 'MP-40010', 'MP26-0079', 0.2, 'L'),
('CIH000412', 'HML0000041', 'AMB-30050', 'MP25-0215', 60, 'ST')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.resourceusagehistory (
  historyid               varchar(16) NOT NULL,
  historymainlineid       varchar(16) NOT NULL,
  resourceid              varchar(16) NOT NULL,
  qualstatusatuse         varchar(20) NOT NULL,
  calibrationduedateatuse date NOT NULL,
  CONSTRAINT resourceusagehistory_pk PRIMARY KEY (historyid)
);
COMMENT ON TABLE opcenter_mes.resourceusagehistory IS 'Equipment used at a step, with the qualification status and calibration due date read from Maximo at the moment of use (read, not enforced: see RO10-AUT-02 on EK26-0335).';

INSERT INTO opcenter_mes.resourceusagehistory (historyid, historymainlineid, resourceid, qualstatusatuse, calibrationduedateatuse) VALUES
('RUH000011', 'HML0000001', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000021', 'HML0000002', 'RES0006', 'Qualified', '2026-10-20'),
('RUH000022', 'HML0000002', 'RES0008', 'Qualified', '2026-10-21'),
('RUH000031', 'HML0000003', 'RES0001', 'Qualified', '2026-12-08'),
('RUH000041', 'HML0000004', 'RES0012', 'Qualified', '2026-07-13'),
('RUH000042', 'HML0000004', 'RES0010', 'Qualified', '2026-08-03'),
('RUH000051', 'HML0000005', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000061', 'HML0000006', 'RES0011', 'Qualified', '2026-12-22'),
('RUH000071', 'HML0000007', 'RES0012', 'Qualified', '2027-01-13'),
('RUH000072', 'HML0000007', 'RES0010', 'Qualified', '2026-08-03'),
('RUH000081', 'HML0000008', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000091', 'HML0000009', 'RES0006', 'Qualified', '2026-10-20'),
('RUH000092', 'HML0000009', 'RES0008', 'Qualified', '2026-10-21'),
('RUH000101', 'HML0000010', 'RES0001', 'Qualified', '2026-12-08'),
('RUH000111', 'HML0000011', 'RES0012', 'Qualified', '2027-01-13'),
('RUH000112', 'HML0000011', 'RES0010', 'Qualified', '2027-02-03'),
('RUH000121', 'HML0000012', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000131', 'HML0000013', 'RES0006', 'Qualified', '2026-10-20'),
('RUH000132', 'HML0000013', 'RES0008', 'Qualified', '2026-10-21'),
('RUH000141', 'HML0000014', 'RES0001', 'Qualified', '2026-12-08'),
('RUH000151', 'HML0000015', 'RES0012', 'Qualified', '2027-01-13'),
('RUH000152', 'HML0000015', 'RES0010', 'Qualified', '2027-02-03'),
('RUH000161', 'HML0000016', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000171', 'HML0000017', 'RES0006', 'Qualified', '2026-10-20'),
('RUH000172', 'HML0000017', 'RES0008', 'Qualified', '2026-10-21'),
('RUH000181', 'HML0000018', 'RES0001', 'Qualified', '2026-12-08'),
('RUH000191', 'HML0000019', 'RES0003', 'RequalDue', '2026-08-28'),
('RUH000201', 'HML0000020', 'RES0012', 'Qualified', '2027-01-13'),
('RUH000202', 'HML0000020', 'RES0010', 'Qualified', '2027-02-03'),
('RUH000211', 'HML0000021', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000221', 'HML0000022', 'RES0006', 'Qualified', '2026-10-20'),
('RUH000222', 'HML0000022', 'RES0008', 'Qualified', '2026-10-21'),
('RUH000231', 'HML0000023', 'RES0001', 'Qualified', '2026-12-08'),
('RUH000241', 'HML0000024', 'RES0002', 'Qualified', '2026-11-25'),
('RUH000251', 'HML0000025', 'RES0012', 'Qualified', '2027-01-13'),
('RUH000252', 'HML0000025', 'RES0010', 'Qualified', '2027-02-03'),
('RUH000261', 'HML0000026', 'RES0007', 'Qualified', '2026-11-18'),
('RUH000271', 'HML0000027', 'RES0011', 'Qualified', '2026-12-22'),
('RUH000281', 'HML0000028', 'RES0012', 'Qualified', '2027-01-13'),
('RUH000282', 'HML0000028', 'RES0010', 'Qualified', '2027-02-03'),
('RUH000291', 'HML0000029', 'RES0005', 'Qualified', '2026-12-01'),
('RUH000301', 'HML0000030', 'RES0004', 'Qualified', '2026-12-01'),
('RUH000311', 'HML0000031', 'RES0009', 'Qualified', '2026-11-11'),
('RUH000321', 'HML0000032', 'RES0005', 'Qualified', '2026-12-01'),
('RUH000331', 'HML0000033', 'RES0004', 'Qualified', '2026-12-01'),
('RUH000341', 'HML0000034', 'RES0009', 'Qualified', '2026-11-11'),
('RUH000351', 'HML0000035', 'RES0005', 'Qualified', '2026-12-01'),
('RUH000361', 'HML0000036', 'RES0004', 'Qualified', '2026-12-01'),
('RUH000371', 'HML0000037', 'RES0009', 'Qualified', '2026-11-11'),
('RUH000381', 'HML0000038', 'RES0005', 'Qualified', '2026-12-01'),
('RUH000391', 'HML0000039', 'RES0004', 'Qualified', '2026-12-01'),
('RUH000401', 'HML0000040', 'RES0009', 'Qualified', '2026-11-11'),
('RUH000411', 'HML0000041', 'RES0005', 'Qualified', '2026-12-01'),
('RUH000421', 'HML0000042', 'RES0004', 'Qualified', '2026-12-01'),
('RUH000431', 'HML0000043', 'RES0009', 'Qualified', '2026-11-11')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.ebrheader (
  containerid        varchar(16) NOT NULL,
  ebrstatus          varchar(20) NOT NULL,
  reviewcompleteflag integer NOT NULL,
  qpcertstatus       varchar(20) NOT NULL,
  archivedocref      varchar(40),
  CONSTRAINT ebrheader_pk PRIMARY KEY (containerid)
);
COMMENT ON TABLE opcenter_mes.ebrheader IS 'Electronic batch record header per container: review completeness (0/1), QP certification status and the OpenText reference of the signed PDF archived on certification.';

INSERT INTO opcenter_mes.ebrheader (containerid, ebrstatus, reviewcompleteflag, qpcertstatus, archivedocref) VALUES
('CNT000301', 'Certified', 1, 'Certified', 'OTCS-2240017'),
('CNT000302', 'Certified', 1, 'Certified', 'OTCS-2240034'),
('CNT000303', 'Certified', 1, 'Certified', 'OTCS-2240051'),
('CNT000304', 'Certified', 1, 'Certified', 'OTCS-2240068'),
('CNT000305', 'OnHold', 1, 'Deferred', NULL),
('CNT000306', 'ReviewPending', 0, 'Pending', NULL),
('CNT000307', 'Open', 0, 'NotStarted', NULL),
('CNT000308', 'Certified', 1, 'Certified', 'OTCS-2240136'),
('CNT000309', 'Certified', 1, 'Certified', 'OTCS-2240153'),
('CNT000310', 'Certified', 1, 'Certified', 'OTCS-2240170'),
('CNT000311', 'Certified', 1, 'Certified', 'OTCS-2240187'),
('CNT000312', 'Open', 0, 'NotStarted', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.ebrsectionref (
  ebrsectionrefid varchar(16) NOT NULL,
  containerid     varchar(16) NOT NULL,
  sectiontype     varchar(20) NOT NULL,
  sourcesystem    varchar(20) NOT NULL,
  externalref     varchar(40) NOT NULL,
  receiveddate    timestamptz NOT NULL,
  CONSTRAINT ebrsectionref_pk PRIMARY KEY (ebrsectionrefid)
);
COMMENT ON TABLE opcenter_mes.ebrsectionref IS 'Sections assembled into the EBR and the system each came from (interface partner name).';

INSERT INTO opcenter_mes.ebrsectionref (ebrsectionrefid, containerid, sectiontype, sourcesystem, externalref, receiveddate) VALUES
('ESR00001', 'CNT000301', 'EXECUTION', 'OPCENTER', 'MES-EK26-0311-EXE', '2026-07-08 16:30:00+00'),
('ESR00002', 'CNT000301', 'PROCESSDATA', 'FACTORYTALK', 'FTV-EK26-0311', '2026-07-08 17:05:00+00'),
('ESR00003', 'CNT000301', 'LABRESULTS', 'LABWARE', 'CA-26-0311', '2026-07-21 15:30:00+00'),
('ESR00004', 'CNT000301', 'SIGNATURE', 'OPCENTER', 'QP-NOPREA-20260723', '2026-07-23 16:00:00+00'),
('ESR00005', 'CNT000302', 'EXECUTION', 'OPCENTER', 'MES-EK26-0318-EXE', '2026-07-22 14:30:00+00'),
('ESR00006', 'CNT000302', 'PROCESSDATA', 'FACTORYTALK', 'FTV-EK26-0318', '2026-07-22 15:05:00+00'),
('ESR00007', 'CNT000302', 'LABRESULTS', 'LABWARE', 'CA-26-0318', '2026-08-05 15:30:00+00'),
('ESR00008', 'CNT000302', 'SIGNATURE', 'OPCENTER', 'QP-NOPREA-20260806', '2026-08-06 16:00:00+00'),
('ESR00009', 'CNT000303', 'EXECUTION', 'OPCENTER', 'MES-EK26-0324-EXE', '2026-08-05 15:30:00+00'),
('ESR00010', 'CNT000303', 'PROCESSDATA', 'FACTORYTALK', 'FTV-EK26-0324', '2026-08-05 16:05:00+00'),
('ESR00011', 'CNT000303', 'LABRESULTS', 'LABWARE', 'CA-26-0324', '2026-08-19 15:30:00+00'),
('ESR00012', 'CNT000303', 'SIGNATURE', 'OPCENTER', 'QP-NOPREA-20260820', '2026-08-20 16:00:00+00'),
('ESR00013', 'CNT000304', 'EXECUTION', 'OPCENTER', 'MES-EK26-0329-EXE', '2026-08-19 16:30:00+00'),
('ESR00014', 'CNT000304', 'PROCESSDATA', 'FACTORYTALK', 'FTV-EK26-0329', '2026-08-19 17:05:00+00'),
('ESR00015', 'CNT000304', 'LABRESULTS', 'LABWARE', 'CA-26-0329', '2026-09-03 15:30:00+00'),
('ESR00016', 'CNT000304', 'DEVIATION', 'VEEVA_QMS', 'DEV-RO-000231', '2026-08-18 14:17:00+00'),
('ESR00017', 'CNT000304', 'SIGNATURE', 'OPCENTER', 'QP-NOPREA-20260904', '2026-09-04 16:00:00+00'),
('ESR00018', 'CNT000305', 'EXECUTION', 'OPCENTER', 'MES-EK26-0335-EXE', '2026-09-02 16:30:00+00'),
('ESR00019', 'CNT000305', 'PROCESSDATA', 'FACTORYTALK', 'FTV-EK26-0335', '2026-09-02 17:05:00+00'),
('ESR00020', 'CNT000305', 'LABRESULTS', 'LABWARE', 'CA-26-0335', '2026-09-18 15:30:00+00'),
('ESR00021', 'CNT000305', 'DEVIATION', 'VEEVA_QMS', 'DEV-RO-000236', '2026-09-03 09:32:00+00'),
('ESR00022', 'CNT000305', 'SIGNATURE', 'OPCENTER', 'QP-NOPREA-20260925', '2026-09-25 16:00:00+00'),
('ESR00023', 'CNT000306', 'EXECUTION', 'OPCENTER', 'MES-EK26-0341-EXE', '2026-09-16 15:30:00+00'),
('ESR00024', 'CNT000306', 'PROCESSDATA', 'FACTORYTALK', 'FTV-EK26-0341', '2026-09-16 16:05:00+00'),
('ESR00025', 'CNT000308', 'EXECUTION', 'OPCENTER', 'MES-SA26-0031-EXE', '2026-07-15 16:30:00+00'),
('ESR00026', 'CNT000308', 'LABRESULTS', 'LABWARE', 'CA-26-S031', '2026-07-16 15:30:00+00'),
('ESR00027', 'CNT000308', 'SIGNATURE', 'OPCENTER', 'QP-RENACHE-20260716', '2026-07-16 16:00:00+00'),
('ESR00028', 'CNT000309', 'EXECUTION', 'OPCENTER', 'MES-SA26-0034-EXE', '2026-08-05 17:30:00+00'),
('ESR00029', 'CNT000309', 'LABRESULTS', 'LABWARE', 'CA-26-S034', '2026-08-06 15:30:00+00'),
('ESR00030', 'CNT000309', 'SIGNATURE', 'OPCENTER', 'QP-RENACHE-20260806', '2026-08-06 16:00:00+00'),
('ESR00031', 'CNT000310', 'EXECUTION', 'OPCENTER', 'MES-SA26-0037-EXE', '2026-08-27 12:30:00+00'),
('ESR00032', 'CNT000310', 'LABRESULTS', 'LABWARE', 'CA-26-S037', '2026-08-27 15:30:00+00'),
('ESR00033', 'CNT000310', 'SIGNATURE', 'OPCENTER', 'QP-RENACHE-20260827', '2026-08-27 16:00:00+00'),
('ESR00034', 'CNT000311', 'EXECUTION', 'OPCENTER', 'MES-SA26-0040-EXE', '2026-09-17 12:30:00+00'),
('ESR00035', 'CNT000311', 'LABRESULTS', 'LABWARE', 'CA-26-S040', '2026-09-17 15:30:00+00'),
('ESR00036', 'CNT000311', 'DEVIATION', 'VEEVA_QMS', 'DEV-RO-000240', '2026-09-16 11:42:00+00'),
('ESR00037', 'CNT000311', 'SIGNATURE', 'OPCENTER', 'QP-RENACHE-20260917', '2026-09-17 16:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.batchreleasehistory (
  historyid         varchar(16) NOT NULL,
  containerid       varchar(16) NOT NULL,
  marketcode        varchar(8) NOT NULL,
  releasedqty       integer,
  certdate          date NOT NULL,
  qpemployeeid      varchar(16) NOT NULL,
  decision          varchar(20) NOT NULL,
  qmsdispositionref varchar(40),
  comments          text,
  storagecondition  text,
  CONSTRAINT batchreleasehistory_pk PRIMARY KEY (historyid)
);
COMMENT ON TABLE opcenter_mes.batchreleasehistory IS 'QP release per market.  Batches reviewed by exception are certified here; batches with a deviation are certified in Veeva QMS first and the release carries the QMS reference.';

INSERT INTO opcenter_mes.batchreleasehistory (historyid, containerid, marketcode, releasedqty, certdate, qpemployeeid, decision, qmsdispositionref, comments, storagecondition) VALUES
('BRH00001', 'CNT000301', 'RO', 17760, '2026-07-23', 'EMP0001', 'Released', NULL, 'Revizuire prin excepție fără abateri.', 'A se păstra la frigider (2-8 °C). A nu se congela. A se păstra fiola în cutie.'),
('BRH00002', 'CNT000301', 'MD', 6000, '2026-07-23', 'EMP0001', 'Released', NULL, 'Etichetare cu autocolant AMDM verificată.', 'A se păstra la frigider (2-8 °C). A nu se congela. A se păstra fiola în cutie.'),
('BRH00003', 'CNT000302', 'RO', 11800, '2026-08-06', 'EMP0001', 'Released', NULL, 'Revizuire prin excepție fără abateri.', 'A nu se păstra la temperaturi peste 25 °C. A se păstra flaconul în cutie.'),
('BRH00004', 'CNT000302', 'BG', 3000, '2026-08-06', 'EMP0001', 'Released', NULL, 'Ambalaj bilingv BG verificat.', 'A nu se păstra la temperaturi peste 25 °C. A se păstra flaconul în cutie.'),
('BRH00005', 'CNT000303', 'RO', 7900, '2026-08-20', 'EMP0001', 'Released', NULL, 'Revizuire prin excepție fără abateri.', 'A se păstra la frigider (2-8 °C). A nu se congela.'),
('BRH00006', 'CNT000304', 'RO', 17600, '2026-09-04', 'EMP0001', 'Released', 'DEV-RO-000231', 'Oprire linie umplere 47 min; purjare azot reluată; fiolele din intervalul afectat (812 buc.) distruse. Eliberare cu justificare.', 'A se păstra la frigider (2-8 °C). A nu se congela. A se păstra fiola în cutie.'),
('BRH00007', 'CNT000304', 'MD', 5400, '2026-09-04', 'EMP0001', 'Released', 'DEV-RO-000231', 'Idem RO; etichetare AMDM verificată.', 'A se păstra la frigider (2-8 °C). A nu se congela. A se păstra fiola în cutie.'),
('BRH00008', 'CNT000308', 'RO', 56, '2026-07-16', 'EMP0006', 'Released', NULL, 'Pacient nominal; identitate lanț verificată.', 'A se păstra congelat sub -20 °C; flaconul deschis se păstrează la frigider max. 24 ore. Pacient nominal.'),
('BRH00009', 'CNT000309', 'RO', 56, '2026-08-06', 'EMP0006', 'Released', NULL, 'Pacient nominal; identitate lanț verificată.', 'A se păstra congelat sub -20 °C; flaconul deschis se păstrează la frigider max. 24 ore. Pacient nominal.'),
('BRH00010', 'CNT000310', 'RO', 56, '2026-08-27', 'EMP0006', 'Released', NULL, 'Pacient nominal; identitate lanț verificată.', 'A se păstra congelat sub -20 °C; flaconul deschis se păstrează la frigider max. 24 ore. Pacient nominal.'),
('BRH00011', 'CNT000311', 'RO', 56, '2026-09-17', 'EMP0006', 'Released', NULL, 'Pacient nominal; alarmă temperatură centrifugă evaluată (DEV-RO-000240) fără impact.', 'A se păstra congelat sub -20 °C; flaconul deschis se păstrează la frigider max. 24 ore. Pacient nominal.')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.shipmentmonitor (
  shipmentmonitorid varchar(16) NOT NULL,
  shipmentname      varchar(40) NOT NULL,
  containerid       varchar(16) NOT NULL,
  productid         varchar(16) NOT NULL,
  loggerid          varchar(40) NOT NULL,
  departdate        timestamptz NOT NULL,
  arrivedate        timestamptz NOT NULL,
  mintemp           numeric(6,1) NOT NULL,
  maxtemp           numeric(6,1) NOT NULL,
  rangelow          numeric(6,1) NOT NULL,
  rangehigh         numeric(6,1) NOT NULL,
  recordcomplete    integer NOT NULL,
  CONSTRAINT shipmentmonitor_pk PRIMARY KEY (shipmentmonitorid)
);
COMMENT ON TABLE opcenter_mes.shipmentmonitor IS 'Cold chain shipments dispatched from the plant: the batch, the Proact logger travelling with it and the temperature range observed from the logger stream (recordcomplete 0 = gap in the stream).';

INSERT INTO opcenter_mes.shipmentmonitor (shipmentmonitorid, shipmentname, containerid, productid, loggerid, departdate, arrivedate, mintemp, maxtemp, rangelow, rangehigh, recordcomplete) VALUES
('SHM00001', 'EXP-26-0391', 'CNT000308', 'PRD00006', 'PCM-T20-00417', '2026-07-17 08:30:00+00', '2026-07-17 11:05:00+00', -69.3, -67.5, -60.0, -18.0, 1),
('SHM00002', 'EXP-26-0396', 'CNT000301', 'PRD00001', 'PCM-T20-00422', '2026-07-27 07:00:00+00', '2026-07-27 10:40:00+00', 4.3, 6.9, 2.0, 8.0, 1),
('SHM00003', 'EXP-26-0403', 'CNT000309', 'PRD00006', 'PCM-T20-00417', '2026-08-07 08:15:00+00', '2026-08-07 10:50:00+00', -69.9, -66.2, -60.0, -18.0, 1),
('SHM00004', 'EXP-26-0407', 'CNT000301', 'PRD00001', 'PCM-L4G-00031', '2026-08-12 05:30:00+00', '2026-08-13 14:20:00+00', 3.3, 5.4, 2.0, 8.0, 1),
('SHM00005', 'EXP-26-0409', 'CNT000303', 'PRD00005', 'PCM-T20-00422', '2026-08-24 07:10:00+00', '2026-08-24 09:55:00+00', 4.8, 5.4, 2.0, 8.0, 1),
('SHM00006', 'EXP-26-0411', 'CNT000310', 'PRD00006', 'PCM-L4G-00034', '2026-08-28 07:40:00+00', '2026-08-28 17:25:00+00', -69.7, -67.4, -60.0, -18.0, 0),
('SHM00007', 'EXP-26-0420', 'CNT000311', 'PRD00006', 'PCM-L4G-00034', '2026-09-18 07:30:00+00', '2026-09-18 18:40:00+00', -69.7, -66.4, -60.0, -18.0, 1),
('SHM00008', 'EXP-26-0418', 'CNT000304', 'PRD00001', 'PCM-L4G-00031', '2026-09-15 05:30:00+00', '2026-09-16 16:10:00+00', 3.1, 9.4, 2.0, 8.0, 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.shipmenteventhistory (
  historyid     varchar(16) NOT NULL,
  shipmentname  varchar(40) NOT NULL,
  eventtype     varchar(30) NOT NULL,
  eventdate     timestamptz NOT NULL,
  carriervendor varchar(10) NOT NULL,
  location      varchar(120),
  comments      text,
  CONSTRAINT shipmenteventhistory_pk PRIMARY KEY (historyid)
);
COMMENT ON TABLE opcenter_mes.shipmenteventhistory IS 'Dispatch-side shipment events recorded in the MES: handover to the carrier and the carrier''s proof of delivery.';

INSERT INTO opcenter_mes.shipmenteventhistory (historyid, shipmentname, eventtype, eventdate, carriervendor, location, comments) VALUES
('SEH00001', 'EXP-26-0391', 'HandedToCarrier', '2026-07-17 08:30:00+00', '0000700250', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-T20-00417 pornit'),
('SEH00002', 'EXP-26-0391', 'DeliveryConfirmed', '2026-07-17 11:40:00+00', '0000700250', '010464 București', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00003', 'EXP-26-0396', 'HandedToCarrier', '2026-07-27 07:00:00+00', '0000700220', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-T20-00422 pornit'),
('SEH00004', 'EXP-26-0396', 'DeliveryConfirmed', '2026-07-27 11:15:00+00', '0000700220', '032258 București', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00005', 'EXP-26-0403', 'HandedToCarrier', '2026-08-07 08:15:00+00', '0000700250', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-T20-00417 pornit'),
('SEH00006', 'EXP-26-0403', 'DeliveryConfirmed', '2026-08-07 11:25:00+00', '0000700250', '010464 București', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00007', 'EXP-26-0407', 'HandedToCarrier', '2026-08-12 05:30:00+00', '0000700220', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-L4G-00031 pornit'),
('SEH00008', 'EXP-26-0407', 'DeliveryConfirmed', '2026-08-13 14:55:00+00', '0000700220', 'MD-2023 Chișinău', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00009', 'EXP-26-0409', 'HandedToCarrier', '2026-08-24 07:10:00+00', '0000700220', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-T20-00422 pornit'),
('SEH00010', 'EXP-26-0409', 'DeliveryConfirmed', '2026-08-24 10:30:00+00', '0000700220', '032368 București', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00011', 'EXP-26-0411', 'HandedToCarrier', '2026-08-28 07:40:00+00', '0000700250', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-L4G-00034 pornit'),
('SEH00012', 'EXP-26-0411', 'DeliveryConfirmed', '2026-08-28 18:00:00+00', '0000700250', '400006 Cluj-Napoca', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00013', 'EXP-26-0420', 'HandedToCarrier', '2026-09-18 07:30:00+00', '0000700250', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-L4G-00034 pornit'),
('SEH00014', 'EXP-26-0420', 'DeliveryConfirmed', '2026-09-18 19:15:00+00', '0000700250', '700111 Iași', 'Confirmare livrare (POD) primită de la transportator'),
('SEH00015', 'EXP-26-0418', 'HandedToCarrier', '2026-09-15 05:30:00+00', '0000700220', 'EKG Pharmaceuticals, rampa 2, București', 'Predat curierului; logger PCM-L4G-00031 pornit'),
('SEH00016', 'EXP-26-0418', 'DeliveryConfirmed', '2026-09-16 16:45:00+00', '0000700220', 'MD-2023 Chișinău', 'Confirmare livrare (POD) primită de la transportator')
ON CONFLICT DO NOTHING;

-- Integration tables filled from the data sharing hub (subscription apply scripts buc_opcenter_mes__*).
CREATE TABLE IF NOT EXISTS opcenter_mes.mfgorder (
  mfgordername        varchar(20) NOT NULL,
  ordertype           varchar(20) NOT NULL,
  productid           varchar(16),
  plannedcontainer    varchar(40),
  qty                 numeric(12,2),
  uom                 varchar(10),
  plannedstartdate    timestamptz,
  plannedcompletiondate timestamptz,
  patientpseudonym    varchar(40),
  patientparameters   text,
  orderstatus         varchar(20) NOT NULL,
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT mfgorder_pk PRIMARY KEY (mfgordername)
);
COMMENT ON TABLE opcenter_mes.mfgorder IS 'Manufacturing orders downloaded for the MES; named-patient orders (ordertype NamedPatient) carry the treatment order number, the planned batch and the patient parameters until the container is started.';

CREATE TABLE IF NOT EXISTS opcenter_mes.inboundshipment (
  shipmentname        varchar(40) NOT NULL,
  mfgordername        varchar(20),
  patientpseudonym    varchar(40),
  carriervendor       varchar(10),
  collectiondate      timestamptz,
  dispatchdate        timestamptz,
  arrivedate          timestamptz,
  viablehours         integer,
  arrivalcondition    text,
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT inboundshipment_pk PRIMARY KEY (shipmentname)
);
COMMENT ON TABLE opcenter_mes.inboundshipment IS 'Inbound patient material shipments for named-patient orders: collection, arrival and remaining viable hours, checked before the batch is started.';

CREATE TABLE IF NOT EXISTS opcenter_mes.resourcequalification (
  resourceid          varchar(16) NOT NULL,
  equipmentstatus     varchar(20),
  qualstatus          varchar(20),
  qualdate            date,
  qualduedate         date,
  calibrationdate     date,
  calibrationduedate  date,
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT resourcequalification_pk PRIMARY KEY (resourceid)
);
COMMENT ON TABLE opcenter_mes.resourcequalification IS 'Current maintenance status, qualification and calibration of each resource as held by Maximo; checked when a resource is used (the value at use is kept in resourceusagehistory).';

CREATE TABLE IF NOT EXISTS opcenter_mes.employeecertification (
  employeeid          varchar(16) NOT NULL,
  certificationname   varchar(40) NOT NULL,
  description         varchar(120),
  effectivedate       date,
  expirationdate      date,
  certstatus          varchar(20) NOT NULL,
  trainingrecordref   varchar(40),
  rolename            varchar(40),
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT employeecertification_pk PRIMARY KEY (employeeid, certificationname)
);
COMMENT ON TABLE opcenter_mes.employeecertification IS 'Employee certifications: the qualifications that allow an employee to perform or sign a step, checked at execution and e-signature.';

CREATE TABLE IF NOT EXISTS opcenter_mes.materialinventory (
  productname         varchar(40) NOT NULL,
  location            varchar(20) NOT NULL,
  lot                 varchar(40),
  qty                 integer NOT NULL,
  minqty              integer,
  maxqty              integer,
  wmsupdatedate       timestamptz,
  CONSTRAINT materialinventory_pk PRIMARY KEY (productname, location)
);
COMMENT ON TABLE opcenter_mes.materialinventory IS 'Material available for issue by warehouse zone, as reported by the WMS (base units); used to check component availability before a batch is started.';

CREATE TABLE IF NOT EXISTS opcenter_mes.labsample (
  samplename          varchar(40) NOT NULL,
  containerid         varchar(16) NOT NULL,
  sampletype          varchar(20) NOT NULL,
  collectiondate      timestamptz,
  samplestatus        varchar(20),
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT labsample_pk PRIMARY KEY (samplename)
);
COMMENT ON TABLE opcenter_mes.labsample IS 'In-process control samples of a batch logged in LabWare, whose results release the next step.';

CREATE TABLE IF NOT EXISTS opcenter_mes.labresult (
  resultname          varchar(40) NOT NULL,
  samplename          varchar(40) NOT NULL,
  testcode            varchar(40) NOT NULL,
  resultvalue         varchar(60),
  uom                 varchar(20),
  lowerlimit          varchar(60),
  upperlimit          varchar(60),
  passflag            integer NOT NULL,
  completeddate       timestamptz,
  analyst             varchar(40),
  CONSTRAINT labresult_pk PRIMARY KEY (resultname)
);
COMMENT ON TABLE opcenter_mes.labresult IS 'In-process control results (LabWare and Empower) for the samples in labsample; passflag 1/0.';

CREATE TABLE IF NOT EXISTS opcenter_mes.extqualityevent (
  eventname           varchar(40) NOT NULL,
  eventtype           varchar(30) NOT NULL,
  containerid         varchar(16) NOT NULL,
  sourcesystem        varchar(20) NOT NULL,
  raiseddate          timestamptz,
  severity            varchar(20),
  eventstatus         varchar(30),
  dispositionstatus   varchar(40),
  dispositiondate     timestamptz,
  shipmentname        varchar(40),
  description         text,
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT extqualityevent_pk PRIMARY KEY (eventname)
);
COMMENT ON TABLE opcenter_mes.extqualityevent IS 'Quality events raised outside the MES against a batch (Veeva QMS deviations, cold-chain excursion assessments) with their disposition; a batch with an open event cannot be closed and its EBR shows the disposition.';

CREATE TABLE IF NOT EXISTS opcenter_mes.shipmentconsignment (
  shipmentname        varchar(40) NOT NULL,
  carriervendor       varchar(10),
  dispatchdate        date,
  shiptoaddress       text,
  unnumber            varchar(20),
  dgqty               numeric(12,3),
  dguom               varchar(20),
  signatory           varchar(40),
  signeddate          timestamptz,
  signatorycertificate varchar(40),
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT shipmentconsignment_pk PRIMARY KEY (shipmentname)
);
COMMENT ON TABLE opcenter_mes.shipmentconsignment IS 'Dangerous goods consignment declared by the WMS for a monitored shipment (dry ice); the handover to the carrier is recorded against it.';

CREATE TABLE IF NOT EXISTS opcenter_mes.extshipmentevent (
  shipmentname        varchar(40) NOT NULL,
  eventtype           varchar(30) NOT NULL,
  eventdate           timestamptz NOT NULL,
  carriervendor       varchar(10),
  location            varchar(120),
  comments            text,
  sourcesystem        varchar(20) NOT NULL,
  CONSTRAINT extshipmentevent_pk PRIMARY KEY (shipmentname, eventtype, eventdate)
);
COMMENT ON TABLE opcenter_mes.extshipmentevent IS 'Journey events of monitored shipments reported by the cold chain monitor (departed, arrived, logger started/stopped, delays); the MES records only the handover and delivery itself (shipmenteventhistory).';

CREATE TABLE IF NOT EXISTS opcenter_mes.shipmenttemperature (
  loggerid            varchar(40) NOT NULL,
  readingdate         timestamptz NOT NULL,
  shipmentname        varchar(40) NOT NULL,
  temperature         numeric(6,1) NOT NULL,
  location            varchar(120),
  devicetype          varchar(20),
  CONSTRAINT shipmenttemperature_pk PRIMARY KEY (loggerid, readingdate)
);
COMMENT ON TABLE opcenter_mes.shipmenttemperature IS 'Logger readings of monitored shipments, from which the transit record (shipmentmonitor) is reviewed.';

CREATE TABLE IF NOT EXISTS opcenter_mes.productmarket (
  productid           varchar(16) NOT NULL,
  marketcode          varchar(8) NOT NULL,
  authorisationref    varchar(40),
  effectivedate       date,
  expirationdate      date,
  lastchangedate      timestamptz NOT NULL,
  CONSTRAINT productmarket_pk PRIMARY KEY (productid, marketcode)
);
COMMENT ON TABLE opcenter_mes.productmarket IS 'Markets each product is authorised for; a batch can be released only to an authorised market (batchreleasehistory.marketcode).';

GRANT USAGE ON SCHEMA opcenter_mes TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA opcenter_mes TO egeria_user, airflow_user;
