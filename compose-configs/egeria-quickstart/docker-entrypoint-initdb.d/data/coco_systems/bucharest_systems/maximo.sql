-- system-qualified-name: SoftwareServer::SYS-016::Maximo Asset Management
-- Maximo Asset Management - Bucharest.  IBM Maximo for the Bucharest site (siteid BUCURESTI): equipment assets, their
-- GMP qualification status, and the qualification and calibration PMs and work orders.  Its tables feed Equipment
-- Qualification Status.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS maximo;
COMMENT ON SCHEMA maximo IS 'IBM Maximo Asset Management (EKG): asset, assetspec, pm and workorder as replicated from the Maximo database.';

CREATE TABLE IF NOT EXISTS maximo.asset (
  assetnum    varchar(40) NOT NULL,
  siteid      varchar(10) NOT NULL,
  description varchar(200),
  assettype   varchar(30),
  status      varchar(20) NOT NULL,
  location    varchar(40),
  installdate date,
  changedate  timestamptz NOT NULL,
  CONSTRAINT asset_pk PRIMARY KEY (assetnum, siteid)
);
COMMENT ON TABLE maximo.asset IS 'Equipment assets.';

INSERT INTO maximo.asset (assetnum, siteid, description, assettype, status, location, installdate, changedate) VALUES
('RO10-DSP-01', 'BUCURESTI', 'Cabină de cântărire cu flux laminar', 'DISPENSING BOOTH', 'OPERATING', 'PROD-DSP', '2025-10-06', '2026-05-18 14:00:00+00'),
('RO10-CMX-01', 'BUCURESTI', 'Vas de preparare soluții 300 L', 'COMPOUNDING VESSEL', 'OPERATING', 'PROD-CMX', '2025-04-14', '2026-04-20 14:00:00+00'),
('RO10-FLT-01', 'BUCURESTI', 'Skid filtrare sterilă 0,22 µm', 'FILTRATION SKID', 'OPERATING', 'PROD-FLT', '2025-04-16', '2026-04-21 14:00:00+00'),
('RO10-AMP-01', 'BUCURESTI', 'Linie umplere și sudare fiole', 'AMPOULE FILLING LINE', 'OPERATING', 'PROD-AMP', '2025-06-02', '2026-06-08 14:00:00+00'),
('RO10-VFL-01', 'BUCURESTI', 'Linie umplere pulberi sterile în flacoane', 'POWDER FILLING LINE', 'OPERATING', 'PROD-VFL', '2025-09-15', '2026-06-22 14:00:00+00'),
('RO10-AUT-01', 'BUCURESTI', 'Autoclavă sterilizare cu abur 1', 'STEAM STERILISER', 'OPERATING', 'PROD-AUT', '2026-02-09', '2026-05-25 14:00:00+00'),
('RO10-AUT-02', 'BUCURESTI', 'Autoclavă sterilizare cu abur 2', 'STEAM STERILISER', 'OPERATING', 'PROD-AUT', '2025-08-25', '2026-02-28 14:00:00+00'),
('RO10-VIS-01', 'BUCURESTI', 'Mașină inspecție vizuală automată', 'INSPECTION MACHINE', 'OPERATING', 'PROD-VIS', '2026-01-19', '2026-07-13 14:00:00+00'),
('RO10-PKG-01', 'BUCURESTI', 'Linie ambalare și serializare', 'PACKAGING LINE', 'OPERATING', 'PROD-PKG', '2025-11-03', '2026-08-03 14:00:00+00'),
('RO10-BSC-01', 'BUCURESTI', 'Hotă flux laminar clasa A, laborator ser', 'BIOSAFETY CABINET', 'OPERATING', 'PROD-BSC', '2026-03-02', '2026-06-01 14:00:00+00'),
('RO10-CEN-01', 'BUCURESTI', 'Centrifugă refrigerată', 'CENTRIFUGE', 'OPERATING', 'PROD-CEN', '2025-12-01', '2026-06-01 14:00:00+00'),
('RO10-FRZ-01', 'BUCURESTI', 'Congelator -40 °C', 'FREEZER', 'OPERATING', 'PROD-FRZ', '2025-11-10', '2026-05-11 14:00:00+00'),
('RO10-HPLC-02', 'BUCURESTI', 'Sistem HPLC, laborator CC', 'CHROMATOGRAPH', 'OPERATING', 'LAB-CC', '2025-07-07', '2026-07-06 14:00:00+00'),
('RO10-CRF-01', 'BUCURESTI', 'Cameră frigorifică 2-8 °C', 'COLD ROOM', 'OPERATING', 'DEP-CF', '2026-01-12', '2026-06-01 14:00:00+00'),
('RO10-AUT-00', 'BUCURESTI', 'Autoclavă sterilizare (înlocuită)', 'STEAM STERILISER', 'DECOMMISSIONED', 'PROD-AUT', '2016-05-02', '2023-09-04 14:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS maximo.assetspec (
  assetnum    varchar(40) NOT NULL,
  siteid      varchar(10) NOT NULL,
  assetattrid varchar(40) NOT NULL,
  alnvalue    varchar(60),
  CONSTRAINT assetspec_pk PRIMARY KEY (assetnum, siteid, assetattrid)
);
COMMENT ON TABLE maximo.assetspec IS 'Asset specification attributes (GMP_QUAL_STATUS, GMP_CRITICAL).';

INSERT INTO maximo.assetspec (assetnum, siteid, assetattrid, alnvalue) VALUES
('RO10-DSP-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-CMX-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-FLT-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-AMP-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-VFL-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-AUT-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-AUT-02', 'BUCURESTI', 'GMP_QUAL_STATUS', 'REQUAL DUE'),
('RO10-VIS-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-PKG-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-BSC-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-CEN-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-FRZ-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-HPLC-02', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-CRF-01', 'BUCURESTI', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('RO10-AUT-00', 'BUCURESTI', 'GMP_QUAL_STATUS', 'NOT QUALIFIED'),
('RO10-DSP-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-CMX-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-FLT-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-AMP-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-VFL-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-AUT-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-AUT-02', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-VIS-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-PKG-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-BSC-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-CEN-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-FRZ-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-HPLC-02', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-CRF-01', 'BUCURESTI', 'GMP_CRITICAL', 'Y'),
('RO10-AUT-00', 'BUCURESTI', 'GMP_CRITICAL', 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS maximo.pm (
  pmnum         varchar(20) NOT NULL,
  siteid        varchar(10) NOT NULL,
  assetnum      varchar(40) NOT NULL,
  worktype      varchar(10) NOT NULL,
  frequency     integer NOT NULL,
  frequnit      varchar(10) NOT NULL,
  laststartdate date,
  nextdate      date NOT NULL,
  status        varchar(10) NOT NULL,
  CONSTRAINT pm_pk PRIMARY KEY (pmnum, siteid)
);
COMMENT ON TABLE maximo.pm IS 'Preventive maintenance masters for qualification (QUAL) and calibration (CAL).';

INSERT INTO maximo.pm (pmnum, siteid, assetnum, worktype, frequency, frequnit, laststartdate, nextdate, status) VALUES
('PM5101', 'BUCURESTI', 'RO10-DSP-01', 'QUAL', 24, 'MONTHS', '2025-10-06', '2027-10-06', 'ACTIVE'),
('PM5102', 'BUCURESTI', 'RO10-DSP-01', 'CAL', 6, 'MONTHS', '2026-05-18', '2026-11-18', 'ACTIVE'),
('PM5103', 'BUCURESTI', 'RO10-CMX-01', 'QUAL', 24, 'MONTHS', '2025-04-14', '2027-04-14', 'ACTIVE'),
('PM5104', 'BUCURESTI', 'RO10-CMX-01', 'CAL', 6, 'MONTHS', '2026-04-20', '2026-10-20', 'ACTIVE'),
('PM5105', 'BUCURESTI', 'RO10-FLT-01', 'QUAL', 24, 'MONTHS', '2025-04-16', '2027-04-16', 'ACTIVE'),
('PM5106', 'BUCURESTI', 'RO10-FLT-01', 'CAL', 6, 'MONTHS', '2026-04-21', '2026-10-21', 'ACTIVE'),
('PM5107', 'BUCURESTI', 'RO10-AMP-01', 'QUAL', 24, 'MONTHS', '2025-06-02', '2027-06-02', 'ACTIVE'),
('PM5108', 'BUCURESTI', 'RO10-AMP-01', 'CAL', 6, 'MONTHS', '2026-06-08', '2026-12-08', 'ACTIVE'),
('PM5109', 'BUCURESTI', 'RO10-VFL-01', 'QUAL', 24, 'MONTHS', '2025-09-15', '2027-09-15', 'ACTIVE'),
('PM5110', 'BUCURESTI', 'RO10-VFL-01', 'CAL', 6, 'MONTHS', '2026-06-22', '2026-12-22', 'ACTIVE'),
('PM5111', 'BUCURESTI', 'RO10-AUT-01', 'QUAL', 12, 'MONTHS', '2026-02-09', '2027-02-09', 'ACTIVE'),
('PM5112', 'BUCURESTI', 'RO10-AUT-01', 'CAL', 6, 'MONTHS', '2026-05-25', '2026-11-25', 'ACTIVE'),
('PM5113', 'BUCURESTI', 'RO10-AUT-02', 'QUAL', 12, 'MONTHS', '2025-08-25', '2026-08-25', 'ACTIVE'),
('PM5114', 'BUCURESTI', 'RO10-AUT-02', 'CAL', 6, 'MONTHS', '2026-02-28', '2026-08-28', 'ACTIVE'),
('PM5115', 'BUCURESTI', 'RO10-VIS-01', 'QUAL', 12, 'MONTHS', '2026-01-19', '2027-01-19', 'ACTIVE'),
('PM5116', 'BUCURESTI', 'RO10-VIS-01', 'CAL', 6, 'MONTHS', '2026-07-13', '2027-01-13', 'ACTIVE'),
('PM5117', 'BUCURESTI', 'RO10-PKG-01', 'QUAL', 24, 'MONTHS', '2025-11-03', '2027-11-03', 'ACTIVE'),
('PM5118', 'BUCURESTI', 'RO10-PKG-01', 'CAL', 6, 'MONTHS', '2026-08-03', '2027-02-03', 'ACTIVE'),
('PM5119', 'BUCURESTI', 'RO10-BSC-01', 'QUAL', 12, 'MONTHS', '2026-03-02', '2027-03-02', 'ACTIVE'),
('PM5120', 'BUCURESTI', 'RO10-BSC-01', 'CAL', 6, 'MONTHS', '2026-06-01', '2026-12-01', 'ACTIVE'),
('PM5121', 'BUCURESTI', 'RO10-CEN-01', 'QUAL', 12, 'MONTHS', '2025-12-01', '2026-12-01', 'ACTIVE'),
('PM5122', 'BUCURESTI', 'RO10-CEN-01', 'CAL', 6, 'MONTHS', '2026-06-01', '2026-12-01', 'ACTIVE'),
('PM5123', 'BUCURESTI', 'RO10-FRZ-01', 'QUAL', 12, 'MONTHS', '2025-11-10', '2026-11-10', 'ACTIVE'),
('PM5124', 'BUCURESTI', 'RO10-FRZ-01', 'CAL', 6, 'MONTHS', '2026-05-11', '2026-11-11', 'ACTIVE'),
('PM5125', 'BUCURESTI', 'RO10-HPLC-02', 'QUAL', 24, 'MONTHS', '2025-07-07', '2027-07-07', 'ACTIVE'),
('PM5126', 'BUCURESTI', 'RO10-HPLC-02', 'CAL', 12, 'MONTHS', '2026-07-06', '2027-07-06', 'ACTIVE'),
('PM5127', 'BUCURESTI', 'RO10-CRF-01', 'QUAL', 12, 'MONTHS', '2026-01-12', '2027-01-12', 'ACTIVE'),
('PM5128', 'BUCURESTI', 'RO10-CRF-01', 'CAL', 6, 'MONTHS', '2026-06-01', '2026-12-01', 'ACTIVE')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS maximo.workorder (
  wonum       varchar(20) NOT NULL,
  siteid      varchar(10) NOT NULL,
  assetnum    varchar(40) NOT NULL,
  worktype    varchar(10) NOT NULL,
  description varchar(200),
  status      varchar(10) NOT NULL,
  actfinish   timestamptz,
  pmnum       varchar(20),
  CONSTRAINT workorder_pk PRIMARY KEY (wonum, siteid)
);
COMMENT ON TABLE maximo.workorder IS 'Work orders generated from the PMs (CLOSE = done; WAPPR = waiting approval).';

INSERT INTO maximo.workorder (wonum, siteid, assetnum, worktype, description, status, actfinish, pmnum) VALUES
('WO51010', 'BUCURESTI', 'RO10-DSP-01', 'QUAL', 'Calificare Cabină de cântărire cu flux laminar', 'CLOSE', '2025-10-06 15:30:00+00', 'PM5101'),
('WO51020', 'BUCURESTI', 'RO10-DSP-01', 'CAL', 'Etalonare Cabină de cântărire cu flux laminar', 'CLOSE', '2026-05-18 15:30:00+00', 'PM5102'),
('WO51030', 'BUCURESTI', 'RO10-CMX-01', 'QUAL', 'Calificare Vas de preparare soluții 300 L', 'CLOSE', '2025-04-14 15:30:00+00', 'PM5103'),
('WO51040', 'BUCURESTI', 'RO10-CMX-01', 'CAL', 'Etalonare Vas de preparare soluții 300 L', 'CLOSE', '2026-04-20 15:30:00+00', 'PM5104'),
('WO51050', 'BUCURESTI', 'RO10-FLT-01', 'QUAL', 'Calificare Skid filtrare sterilă 0,22 µm', 'CLOSE', '2025-04-16 15:30:00+00', 'PM5105'),
('WO51060', 'BUCURESTI', 'RO10-FLT-01', 'CAL', 'Etalonare Skid filtrare sterilă 0,22 µm', 'CLOSE', '2026-04-21 15:30:00+00', 'PM5106'),
('WO51070', 'BUCURESTI', 'RO10-AMP-01', 'QUAL', 'Calificare Linie umplere și sudare fiole', 'CLOSE', '2025-06-02 15:30:00+00', 'PM5107'),
('WO51080', 'BUCURESTI', 'RO10-AMP-01', 'CAL', 'Etalonare Linie umplere și sudare fiole', 'CLOSE', '2026-06-08 15:30:00+00', 'PM5108'),
('WO51090', 'BUCURESTI', 'RO10-VFL-01', 'QUAL', 'Calificare Linie umplere pulberi sterile în flacoane', 'CLOSE', '2025-09-15 15:30:00+00', 'PM5109'),
('WO51100', 'BUCURESTI', 'RO10-VFL-01', 'CAL', 'Etalonare Linie umplere pulberi sterile în flacoane', 'CLOSE', '2026-06-22 15:30:00+00', 'PM5110'),
('WO51110', 'BUCURESTI', 'RO10-AUT-01', 'QUAL', 'Calificare Autoclavă sterilizare cu abur 1', 'CLOSE', '2026-02-09 15:30:00+00', 'PM5111'),
('WO51120', 'BUCURESTI', 'RO10-AUT-01', 'CAL', 'Etalonare Autoclavă sterilizare cu abur 1', 'CLOSE', '2026-05-25 15:30:00+00', 'PM5112'),
('WO51130', 'BUCURESTI', 'RO10-AUT-02', 'QUAL', 'Calificare Autoclavă sterilizare cu abur 2', 'CLOSE', '2025-08-25 15:30:00+00', 'PM5113'),
('WO51140', 'BUCURESTI', 'RO10-AUT-02', 'CAL', 'Etalonare Autoclavă sterilizare cu abur 2', 'CLOSE', '2026-02-28 15:30:00+00', 'PM5114'),
('WO51141', 'BUCURESTI', 'RO10-AUT-02', 'CAL', 'Etalonare sonde Autoclavă sterilizare cu abur 2 (scadentă 2026-08-28)', 'WAPPR', NULL, 'PM5114'),
('WO51150', 'BUCURESTI', 'RO10-VIS-01', 'QUAL', 'Calificare Mașină inspecție vizuală automată', 'CLOSE', '2026-01-19 15:30:00+00', 'PM5115'),
('WO51160', 'BUCURESTI', 'RO10-VIS-01', 'CAL', 'Etalonare Mașină inspecție vizuală automată', 'CLOSE', '2026-07-13 15:30:00+00', 'PM5116'),
('WO51170', 'BUCURESTI', 'RO10-PKG-01', 'QUAL', 'Calificare Linie ambalare și serializare', 'CLOSE', '2025-11-03 15:30:00+00', 'PM5117'),
('WO51180', 'BUCURESTI', 'RO10-PKG-01', 'CAL', 'Etalonare Linie ambalare și serializare', 'CLOSE', '2026-08-03 15:30:00+00', 'PM5118'),
('WO51190', 'BUCURESTI', 'RO10-BSC-01', 'QUAL', 'Calificare Hotă flux laminar clasa A, laborator ser', 'CLOSE', '2026-03-02 15:30:00+00', 'PM5119'),
('WO51200', 'BUCURESTI', 'RO10-BSC-01', 'CAL', 'Etalonare Hotă flux laminar clasa A, laborator ser', 'CLOSE', '2026-06-01 15:30:00+00', 'PM5120'),
('WO51210', 'BUCURESTI', 'RO10-CEN-01', 'QUAL', 'Calificare Centrifugă refrigerată', 'CLOSE', '2025-12-01 15:30:00+00', 'PM5121'),
('WO51220', 'BUCURESTI', 'RO10-CEN-01', 'CAL', 'Etalonare Centrifugă refrigerată', 'CLOSE', '2026-06-01 15:30:00+00', 'PM5122'),
('WO51230', 'BUCURESTI', 'RO10-FRZ-01', 'QUAL', 'Calificare Congelator -40 °C', 'CLOSE', '2025-11-10 15:30:00+00', 'PM5123'),
('WO51240', 'BUCURESTI', 'RO10-FRZ-01', 'CAL', 'Etalonare Congelator -40 °C', 'CLOSE', '2026-05-11 15:30:00+00', 'PM5124'),
('WO51250', 'BUCURESTI', 'RO10-HPLC-02', 'QUAL', 'Calificare Sistem HPLC, laborator CC', 'CLOSE', '2025-07-07 15:30:00+00', 'PM5125'),
('WO51260', 'BUCURESTI', 'RO10-HPLC-02', 'CAL', 'Etalonare Sistem HPLC, laborator CC', 'CLOSE', '2026-07-06 15:30:00+00', 'PM5126'),
('WO51270', 'BUCURESTI', 'RO10-CRF-01', 'QUAL', 'Calificare Cameră frigorifică 2-8 °C', 'CLOSE', '2026-01-12 15:30:00+00', 'PM5127'),
('WO51280', 'BUCURESTI', 'RO10-CRF-01', 'CAL', 'Etalonare Cameră frigorifică 2-8 °C', 'CLOSE', '2026-06-01 15:30:00+00', 'PM5128')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA maximo TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA maximo TO egeria_user, airflow_user;
