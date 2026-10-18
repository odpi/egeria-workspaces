-- system-qualified-name: SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601
-- Siemens Opcenter MES - Austin.  Opcenter Execution Pharma for the Austin manufacturing lines: batches (containers),
-- executed steps with electronic signatures, component issues and equipment use.  Its tables feed Batch Execution
-- Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS opcenter_mes;
COMMENT ON SCHEMA opcenter_mes IS 'Siemens Opcenter Execution Pharma (Austin): batch containers, step history, component issue and resource usage history, as landed by the MES reporting database replica.';

CREATE TABLE IF NOT EXISTS opcenter_mes.product (
  productid       varchar(16) NOT NULL,
  productname     varchar(40) NOT NULL,
  productrevision varchar(10) NOT NULL,
  description     varchar(255),
  CONSTRAINT product_pk PRIMARY KEY (productid)
);
COMMENT ON TABLE opcenter_mes.product IS 'Products (product name = product code).';

INSERT INTO opcenter_mes.product (productid, productname, productrevision, description) VALUES
('PRD00001', '2050', '3.1', 'Plavix 75mg film-coated tablets'),
('PRD00002', '3000', '4.2', 'Cozaar 100mg film-coated tablets'),
('PRD00003', '9000', '2.4', 'Cisplatin 50mg/50mL injection'),
('PRD00004', 'AU-4410', '5.0', 'Carboplatin 450mg/45mL injection'),
('PRD00005', 'AU-4630', '3.3', 'Methotrexate 250mg/10mL injection'),
('PRD00006', 'AU-7710', '1.3', 'Dendrivax autologous dendritic cell suspension')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.container (
  containerid   varchar(16) NOT NULL,
  containername varchar(40) NOT NULL,
  productid     varchar(16) NOT NULL,
  mfgordername  varchar(20),
  qty           numeric(12,2) NOT NULL,
  uom           varchar(10) NOT NULL,
  status        varchar(20) NOT NULL,
  startdate     timestamptz NOT NULL,
  enddate       timestamptz,
  CONSTRAINT container_pk PRIMARY KEY (containerid)
);
COMMENT ON TABLE opcenter_mes.container IS 'Batches (containers); the manufacturing order name is the SAP production order.';

INSERT INTO opcenter_mes.container (containerid, containername, productid, mfgordername, qty, uom, status, startdate, enddate) VALUES
('CNT000101', 'A26-3000-0141', 'PRD00002', '1000412', 120000, 'TAB', 'Closed', '2026-08-03 06:00:00+00', '2026-08-05 18:00:00+00'),
('CNT000102', 'A26-2050-0087', 'PRD00001', '1000431', 90000, 'TAB', 'Closed', '2026-08-17 06:00:00+00', '2026-08-19 14:00:00+00'),
('CNT000103', 'A26-9000-0019', 'PRD00003', '1000448', 2500, 'VIA', 'Closed', '2026-09-01 07:00:00+00', '2026-09-02 19:00:00+00'),
('CNT000104', 'A26-3000-0142', 'PRD00002', '1000457', 120000, 'TAB', 'Closed', '2026-09-07 06:00:00+00', '2026-09-09 18:00:00+00'),
('CNT000105', 'A26-2050-0088', 'PRD00001', '1000466', 90000, 'TAB', 'Active', '2026-09-28 06:00:00+00', NULL),
('CNT000106', 'A26-4410-0052', 'PRD00004', '1000402', 3200, 'VIA', 'Closed', '2026-07-20 07:00:00+00', '2026-07-21 17:30:00+00'),
('CNT000107', 'A26-4630-0017', 'PRD00005', '1000452', 4000, 'VIA', 'Closed', '2026-09-14 07:00:00+00', '2026-09-15 16:00:00+00'),
('CNT000108', 'A26-7710-P015', 'PRD00006', '1000481', 1, 'BAG', 'Closed', '2026-07-13 07:00:00+00', '2026-07-24 16:00:00+00'),
('CNT000109', 'A26-7710-P016', 'PRD00006', '1000482', 1, 'BAG', 'Closed', '2026-08-10 07:00:00+00', '2026-08-21 15:30:00+00'),
('CNT000110', 'A26-7710-P017', 'PRD00006', '1000483', 1, 'BAG', 'Closed', '2026-09-01 07:00:00+00', '2026-09-12 14:00:00+00'),
('CNT000111', 'A26-7710-P018', 'PRD00006', '1000484', 1, 'BAG', 'Closed', '2026-09-15 07:00:00+00', '2026-09-26 15:00:00+00')
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
('SPC0001', 'COMPOUND', 'B', 'Compound step'),
('SPC0002', 'COMPRESS', 'B', 'Compress step'),
('SPC0003', 'CRYOPRESERVE', 'B', 'Cryopreserve step'),
('SPC0004', 'CULTURE', 'B', 'Culture step'),
('SPC0005', 'DISPENSE', 'B', 'Dispense step'),
('SPC0006', 'FILL', 'B', 'Fill step'),
('SPC0007', 'GRANULATE', 'B', 'Granulate step'),
('SPC0008', 'HARVEST', 'B', 'Harvest step'),
('SPC0009', 'INSPECT', 'B', 'Inspect step'),
('SPC0010', 'PACKAGE', 'B', 'Package step')
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
('RES0001', 'US10-BSC-03', 'Class II biosafety cabinet, cell suite 3', 'Biosafety cabinet'),
('RES0002', 'US10-CMP-01', 'Rotary tablet press FE55', 'Tablet press'),
('RES0003', 'US10-CMX-01', 'Cytotoxic compounding vessel 200 L', 'Compounding vessel'),
('RES0004', 'US10-CRF-01', 'Controlled-rate freezer', 'Freezer'),
('RES0005', 'US10-DSP-01', 'Downflow dispensing booth 1', 'Dispensing booth'),
('RES0006', 'US10-FBD-01', 'Fluid bed dryer WSG-300', 'Fluid bed dryer'),
('RES0007', 'US10-FIL-01', 'Isolator vial filling line', 'Aseptic filling line'),
('RES0008', 'US10-GRN-01', 'High-shear granulator GMX-600', 'Granulator'),
('RES0009', 'US10-INC-02', 'CO2 incubator, cell suite 2', 'Incubator'),
('RES0010', 'US10-PKG-01', 'Bottle packaging and serialisation line 1', 'Packaging line'),
('RES0011', 'US10-VIS-01', 'Automated visual inspection machine', 'Inspection machine')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.employee (
  employeeid     varchar(16) NOT NULL,
  employeename   varchar(40) NOT NULL,
  fullname       varchar(120),
  employeenumber varchar(20) NOT NULL,
  CONSTRAINT employee_pk PRIMARY KEY (employeeid)
);
COMMENT ON TABLE opcenter_mes.employee IS 'MES users (employee name = AD login, employee number = Workday employee ID).';

INSERT INTO opcenter_mes.employee (employeeid, employeename, fullname, employeenumber) VALUES
('EMP0001', 'bfoster', 'Brian Foster', '100122'),
('EMP0002', 'jmorales', 'Jason Morales', '100142'),
('EMP0003', 'abrooks', 'Aaliyah Brooks', '100149'),
('EMP0004', 'tnguyen', 'Tyler Nguyen', '100153'),
('EMP0005', 'glindqvist', 'Grace Lindqvist', '100158')
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
('HML0000001', 'CNT000101', 'SPC0005', 1, '2026-08-03 06:00:00+00', '2026-08-03 20:40:00+00', 'EMP0001', 'EMP0002', 'Performed and verified', '2026-08-03 20:46:00+00', 'Completed'),
('HML0000002', 'CNT000101', 'SPC0007', 2, '2026-08-03 21:15:00+00', '2026-08-04 11:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-08-04 11:46:00+00', 'Completed'),
('HML0000003', 'CNT000101', 'SPC0002', 3, '2026-08-04 12:15:00+00', '2026-08-05 02:40:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-08-05 02:46:00+00', 'Completed'),
('HML0000004', 'CNT000101', 'SPC0010', 4, '2026-08-05 03:15:00+00', '2026-08-05 18:00:00+00', 'EMP0001', 'EMP0002', 'Performed and verified', '2026-08-05 18:06:00+00', 'Completed'),
('HML0000005', 'CNT000102', 'SPC0005', 1, '2026-08-17 06:00:00+00', '2026-08-17 19:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-08-17 19:46:00+00', 'Completed'),
('HML0000006', 'CNT000102', 'SPC0007', 2, '2026-08-17 20:15:00+00', '2026-08-18 09:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-08-18 09:46:00+00', 'Completed'),
('HML0000007', 'CNT000102', 'SPC0002', 3, '2026-08-18 10:15:00+00', '2026-08-18 23:40:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-08-18 23:46:00+00', 'Completed'),
('HML0000008', 'CNT000102', 'SPC0010', 4, '2026-08-19 00:15:00+00', '2026-08-19 14:00:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-08-19 14:06:00+00', 'Completed'),
('HML0000009', 'CNT000103', 'SPC0005', 1, '2026-09-01 07:00:00+00', '2026-09-01 15:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-01 15:46:00+00', 'Completed'),
('HML0000010', 'CNT000103', 'SPC0001', 2, '2026-09-01 16:15:00+00', '2026-09-02 00:40:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-09-02 00:46:00+00', 'Completed'),
('HML0000011', 'CNT000103', 'SPC0006', 3, '2026-09-02 01:15:00+00', '2026-09-02 09:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-02 09:46:00+00', 'CompletedWithException'),
('HML0000012', 'CNT000103', 'SPC0009', 4, '2026-09-02 10:15:00+00', '2026-09-02 19:00:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-09-02 19:06:00+00', 'Completed'),
('HML0000013', 'CNT000104', 'SPC0005', 1, '2026-09-07 06:00:00+00', '2026-09-07 20:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-07 20:46:00+00', 'Completed'),
('HML0000014', 'CNT000104', 'SPC0007', 2, '2026-09-07 21:15:00+00', '2026-09-08 11:40:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-09-08 11:46:00+00', 'Completed'),
('HML0000015', 'CNT000104', 'SPC0002', 3, '2026-09-08 12:15:00+00', '2026-09-09 02:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-09 02:46:00+00', 'Completed'),
('HML0000016', 'CNT000104', 'SPC0010', 4, '2026-09-09 03:15:00+00', '2026-09-09 18:00:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-09 18:06:00+00', 'Completed'),
('HML0000017', 'CNT000105', 'SPC0005', 1, '2026-09-28 06:00:00+00', '2026-09-28 20:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-28 20:46:00+00', 'Completed'),
('HML0000018', 'CNT000105', 'SPC0007', 2, '2026-09-28 21:15:00+00', '2026-09-29 11:40:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-09-29 11:46:00+00', 'Completed'),
('HML0000019', 'CNT000105', 'SPC0002', 3, '2026-09-29 12:15:00+00', '2026-09-30 02:40:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-30 02:46:00+00', 'Completed'),
('HML0000020', 'CNT000105', 'SPC0010', 4, '2026-09-30 03:15:00+00', NULL, 'EMP0003', NULL, NULL, NULL, 'InProcess'),
('HML0000021', 'CNT000106', 'SPC0005', 1, '2026-07-20 07:00:00+00', '2026-07-20 15:17:30+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-07-20 15:23:30+00', 'Completed'),
('HML0000022', 'CNT000106', 'SPC0001', 2, '2026-07-20 15:52:30+00', '2026-07-20 23:55:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-07-21 00:01:00+00', 'Completed'),
('HML0000023', 'CNT000106', 'SPC0006', 3, '2026-07-21 00:30:00+00', '2026-07-21 08:32:30+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-07-21 08:38:30+00', 'Completed'),
('HML0000024', 'CNT000106', 'SPC0009', 4, '2026-07-21 09:07:30+00', '2026-07-21 17:30:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-07-21 17:36:00+00', 'Completed'),
('HML0000025', 'CNT000107', 'SPC0005', 1, '2026-09-14 07:00:00+00', '2026-09-14 14:55:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-14 15:01:00+00', 'Completed'),
('HML0000026', 'CNT000107', 'SPC0001', 2, '2026-09-14 15:30:00+00', '2026-09-14 23:10:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-09-14 23:16:00+00', 'Completed'),
('HML0000027', 'CNT000107', 'SPC0006', 3, '2026-09-14 23:45:00+00', '2026-09-15 07:25:00+00', 'EMP0003', 'EMP0002', 'Performed and verified', '2026-09-15 07:31:00+00', 'Completed'),
('HML0000028', 'CNT000107', 'SPC0009', 4, '2026-09-15 08:00:00+00', '2026-09-15 16:00:00+00', 'EMP0004', 'EMP0002', 'Performed and verified', '2026-09-15 16:06:00+00', 'Completed'),
('HML0000029', 'CNT000108', 'SPC0004', 1, '2026-07-13 07:00:00+00', '2026-07-17 01:40:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-07-17 01:46:00+00', 'Completed'),
('HML0000030', 'CNT000108', 'SPC0008', 2, '2026-07-17 02:15:00+00', '2026-07-20 20:40:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-07-20 20:46:00+00', 'Completed'),
('HML0000031', 'CNT000108', 'SPC0003', 3, '2026-07-20 21:15:00+00', '2026-07-24 16:00:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-07-24 16:06:00+00', 'Completed'),
('HML0000032', 'CNT000109', 'SPC0004', 1, '2026-08-10 07:00:00+00', '2026-08-14 01:30:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-08-14 01:36:00+00', 'Completed'),
('HML0000033', 'CNT000109', 'SPC0008', 2, '2026-08-14 02:05:00+00', '2026-08-17 20:20:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-08-17 20:26:00+00', 'Completed'),
('HML0000034', 'CNT000109', 'SPC0003', 3, '2026-08-17 20:55:00+00', '2026-08-21 15:30:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-08-21 15:36:00+00', 'Completed'),
('HML0000035', 'CNT000110', 'SPC0004', 1, '2026-09-01 07:00:00+00', '2026-09-05 01:00:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-09-05 01:06:00+00', 'Completed'),
('HML0000036', 'CNT000110', 'SPC0008', 2, '2026-09-05 01:35:00+00', '2026-09-08 19:20:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-09-08 19:26:00+00', 'Completed'),
('HML0000037', 'CNT000110', 'SPC0003', 3, '2026-09-08 19:55:00+00', '2026-09-12 14:00:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-09-12 14:06:00+00', 'Completed'),
('HML0000038', 'CNT000111', 'SPC0004', 1, '2026-09-15 07:00:00+00', '2026-09-19 01:20:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-09-19 01:26:00+00', 'CompletedWithException'),
('HML0000039', 'CNT000111', 'SPC0008', 2, '2026-09-19 01:55:00+00', '2026-09-22 20:00:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-09-22 20:06:00+00', 'Completed'),
('HML0000040', 'CNT000111', 'SPC0003', 3, '2026-09-22 20:35:00+00', '2026-09-26 15:00:00+00', 'EMP0005', 'EMP0002', 'Performed and verified', '2026-09-26 15:06:00+00', 'Completed')
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
COMMENT ON TABLE opcenter_mes.componentissuehistory IS 'Component (raw material lot) issues recorded against a step.';

INSERT INTO opcenter_mes.componentissuehistory (historyid, historymainlineid, issuedproductname, fromlot, qtyissued, uom) VALUES
('CIH000011', 'HML0000001', 'RM-100110', 'RM26-0101', 12.4, 'KG'),
('CIH000012', 'HML0000001', 'RM-200210', 'RM26-0102', 18.0, 'KG'),
('CIH000013', 'HML0000001', 'RM-200220', 'RM26-0103', 0.3, 'KG'),
('CIH000051', 'HML0000005', 'RM-100120', 'RM26-0104', 8.9, 'KG'),
('CIH000052', 'HML0000005', 'RM-200210', 'RM26-0102', 14.0, 'KG'),
('CIH000053', 'HML0000005', 'RM-200220', 'RM26-0103', 0.25, 'KG'),
('CIH000091', 'HML0000009', 'RM-100130', 'RM26-0105', 131.0, 'G'),
('CIH000092', 'HML0000009', 'PK-300310', 'RM26-0106', 2550, 'EA'),
('CIH000131', 'HML0000013', 'RM-100110', 'RM26-0107', 12.4, 'KG'),
('CIH000132', 'HML0000013', 'RM-200210', 'RM26-0102', 18.0, 'KG'),
('CIH000133', 'HML0000013', 'RM-200220', 'RM26-0103', 0.3, 'KG'),
('CIH000171', 'HML0000017', 'RM-100120', 'RM26-0110', 8.9, 'KG'),
('CIH000172', 'HML0000017', 'RM-200210', 'RM26-0102', 14.0, 'KG'),
('CIH000173', 'HML0000017', 'RM-200220', 'RM26-0103', 0.25, 'KG'),
('CIH000211', 'HML0000021', 'RM-100140', 'RM25-0388', 1480.0, 'G'),
('CIH000212', 'HML0000021', 'PK-300310', 'RM25-0412', 3260, 'EA'),
('CIH000251', 'HML0000025', 'RM-100150', 'RM26-0108', 1030.0, 'G'),
('CIH000252', 'HML0000025', 'PK-300310', 'RM26-0106', 4080, 'EA'),
('CIH000291', 'HML0000029', 'RM-400410', 'RM26-0098', 2.5, 'L'),
('CIH000321', 'HML0000032', 'RM-400410', 'RM26-0098', 2.5, 'L'),
('CIH000351', 'HML0000035', 'RM-400410', 'RM26-0098', 2.5, 'L'),
('CIH000381', 'HML0000038', 'RM-400410', 'RM26-0098', 2.5, 'L')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opcenter_mes.resourceusagehistory (
  historyid               varchar(16) NOT NULL,
  historymainlineid       varchar(16) NOT NULL,
  resourceid              varchar(16) NOT NULL,
  qualstatusatuse         varchar(20) NOT NULL,
  calibrationduedateatuse date NOT NULL,
  CONSTRAINT resourceusagehistory_pk PRIMARY KEY (historyid)
);
COMMENT ON TABLE opcenter_mes.resourceusagehistory IS 'Equipment used at a step, with the qualification status and calibration due date read from Maximo at the moment of use.';

INSERT INTO opcenter_mes.resourceusagehistory (historyid, historymainlineid, resourceid, qualstatusatuse, calibrationduedateatuse) VALUES
('RUH000011', 'HML0000001', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000021', 'HML0000002', 'RES0008', 'Qualified', '2026-12-02'),
('RUH000022', 'HML0000002', 'RES0006', 'Qualified', '2026-12-03'),
('RUH000031', 'HML0000003', 'RES0002', 'Qualified', '2026-10-14'),
('RUH000041', 'HML0000004', 'RES0010', 'Qualified', '2026-08-11'),
('RUH000051', 'HML0000005', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000061', 'HML0000006', 'RES0008', 'Qualified', '2026-12-02'),
('RUH000062', 'HML0000006', 'RES0006', 'Qualified', '2026-12-03'),
('RUH000071', 'HML0000007', 'RES0002', 'Qualified', '2026-10-14'),
('RUH000081', 'HML0000008', 'RES0010', 'Qualified', '2027-02-11'),
('RUH000091', 'HML0000009', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000101', 'HML0000010', 'RES0003', 'Qualified', '2026-09-04'),
('RUH000111', 'HML0000011', 'RES0007', 'Qualified', '2026-10-06'),
('RUH000121', 'HML0000012', 'RES0011', 'Qualified', '2027-02-17'),
('RUH000131', 'HML0000013', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000141', 'HML0000014', 'RES0008', 'Qualified', '2026-12-02'),
('RUH000142', 'HML0000014', 'RES0006', 'Qualified', '2026-12-03'),
('RUH000151', 'HML0000015', 'RES0002', 'Qualified', '2026-10-14'),
('RUH000161', 'HML0000016', 'RES0010', 'Qualified', '2027-02-11'),
('RUH000171', 'HML0000017', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000181', 'HML0000018', 'RES0008', 'Qualified', '2026-12-02'),
('RUH000182', 'HML0000018', 'RES0006', 'Qualified', '2026-12-03'),
('RUH000191', 'HML0000019', 'RES0002', 'Qualified', '2026-10-14'),
('RUH000201', 'HML0000020', 'RES0010', 'Qualified', '2027-02-11'),
('RUH000211', 'HML0000021', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000221', 'HML0000022', 'RES0003', 'Qualified', '2026-09-04'),
('RUH000231', 'HML0000023', 'RES0007', 'Qualified', '2026-10-06'),
('RUH000241', 'HML0000024', 'RES0011', 'Qualified', '2026-08-17'),
('RUH000251', 'HML0000025', 'RES0005', 'Qualified', '2026-11-12'),
('RUH000261', 'HML0000026', 'RES0003', 'Qualified', '2027-03-04'),
('RUH000271', 'HML0000027', 'RES0007', 'Qualified', '2026-10-06'),
('RUH000281', 'HML0000028', 'RES0011', 'Qualified', '2027-02-17'),
('RUH000291', 'HML0000029', 'RES0001', 'Qualified', '2026-07-27'),
('RUH000292', 'HML0000029', 'RES0009', 'Qualified', '2026-09-08'),
('RUH000301', 'HML0000030', 'RES0001', 'Qualified', '2026-07-27'),
('RUH000311', 'HML0000031', 'RES0004', 'Qualified', '2026-10-13'),
('RUH000321', 'HML0000032', 'RES0001', 'Qualified', '2027-01-27'),
('RUH000322', 'HML0000032', 'RES0009', 'Qualified', '2026-09-08'),
('RUH000331', 'HML0000033', 'RES0001', 'Qualified', '2027-01-27'),
('RUH000341', 'HML0000034', 'RES0004', 'Qualified', '2026-10-13'),
('RUH000351', 'HML0000035', 'RES0001', 'Qualified', '2027-01-27'),
('RUH000352', 'HML0000035', 'RES0009', 'Qualified', '2026-09-08'),
('RUH000361', 'HML0000036', 'RES0001', 'Qualified', '2027-01-27'),
('RUH000371', 'HML0000037', 'RES0004', 'Qualified', '2026-10-13'),
('RUH000381', 'HML0000038', 'RES0001', 'Qualified', '2027-01-27'),
('RUH000382', 'HML0000038', 'RES0009', 'Qualified', '2026-09-08'),
('RUH000391', 'HML0000039', 'RES0001', 'Qualified', '2027-01-27'),
('RUH000401', 'HML0000040', 'RES0004', 'Qualified', '2026-10-13')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/opcenter_mes).
-- No extract reads them.

ALTER TABLE opcenter_mes.resourcedef ADD COLUMN IF NOT EXISTS assetstatus varchar(20);
ALTER TABLE opcenter_mes.resourcedef ADD COLUMN IF NOT EXISTS qualificationstatus varchar(20);
ALTER TABLE opcenter_mes.resourcedef ADD COLUMN IF NOT EXISTS qualificationdate date;
ALTER TABLE opcenter_mes.resourcedef ADD COLUMN IF NOT EXISTS qualificationexpirydate date;
ALTER TABLE opcenter_mes.resourcedef ADD COLUMN IF NOT EXISTS calibrationdate date;
ALTER TABLE opcenter_mes.resourcedef ADD COLUMN IF NOT EXISTS calibrationduedate date;
COMMENT ON COLUMN opcenter_mes.resourcedef.assetstatus IS 'Maximo asset status, from Equipment Qualification Status.';
COMMENT ON COLUMN opcenter_mes.resourcedef.qualificationstatus IS 'Current qualification status checked before use, from Equipment Qualification Status.';
COMMENT ON COLUMN opcenter_mes.resourcedef.qualificationexpirydate IS 'Qualification valid until, from Equipment Qualification Status.';
COMMENT ON COLUMN opcenter_mes.resourcedef.calibrationduedate IS 'Calibration due date checked before use, from Equipment Qualification Status.';

CREATE TABLE IF NOT EXISTS opcenter_mes.erpinventory (
  productname varchar(40) NOT NULL,
  warehouse   varchar(20) NOT NULL,
  lotname     varchar(40),
  qtyonhand   integer NOT NULL,
  minqty      integer,
  maxqty      integer,
  lastupdated timestamptz NOT NULL,
  CONSTRAINT erpinventory_pk PRIMARY KEY (productname, warehouse)
);
COMMENT ON TABLE opcenter_mes.erpinventory IS 'Plant stores (AUS1) stock positions from Goods Inventory Stock, checked at weigh and dispense.';

CREATE TABLE IF NOT EXISTS opcenter_mes.qualitysample (
  samplename   varchar(40) NOT NULL,
  containerid  varchar(16) NOT NULL,
  sampletype   varchar(20) NOT NULL,
  sampledate   timestamptz NOT NULL,
  samplestatus varchar(20) NOT NULL,
  CONSTRAINT qualitysample_pk PRIMARY KEY (samplename)
);
COMMENT ON TABLE opcenter_mes.qualitysample IS 'LIMS samples taken from MES batches (in-process and finished product), from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS opcenter_mes.qualityresult (
  resultname    varchar(40) NOT NULL,
  samplename    varchar(40) NOT NULL,
  testname      varchar(40) NOT NULL,
  resultvalue   varchar(60) NOT NULL,
  uom           varchar(20),
  lowerlimit    varchar(60),
  upperlimit    varchar(60),
  passfail      varchar(4) NOT NULL,
  completeddate timestamptz NOT NULL,
  analyst       varchar(40) NOT NULL,
  CONSTRAINT qualityresult_pk PRIMARY KEY (resultname)
);
COMMENT ON TABLE opcenter_mes.qualityresult IS 'Laboratory results for MES batch samples, from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS opcenter_mes.employeecertification (
  employeeid               varchar(16) NOT NULL,
  certificationname        varchar(40) NOT NULL,
  certificationdescription varchar(120) NOT NULL,
  effectivedate            date NOT NULL,
  expirydate               date NOT NULL,
  certificationstatus      varchar(20) NOT NULL,
  trainingrecord           varchar(40) NOT NULL,
  certificatenumber        varchar(40),
  rolename                 varchar(40) NOT NULL,
  CONSTRAINT employeecertification_pk PRIMARY KEY (employeeid, certificationname)
);
COMMENT ON TABLE opcenter_mes.employeecertification IS 'Employee certifications checked before an operator performs or signs a step, from Worker Qualifications.';

GRANT USAGE ON SCHEMA opcenter_mes TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA opcenter_mes TO egeria_user, airflow_user;
