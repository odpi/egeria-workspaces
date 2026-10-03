-- system-qualified-name: SoftwareServer::AUS-SYS-029::SN-CMM-AU-20190401
-- IBM Maximo CMMS - Austin.  Maximo Asset Management for the Austin site: GMP equipment, qualification attributes,
-- preventive maintenance schedules and calibration/qualification work orders.  Its tables feed Equipment Qualification
-- Status.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS ibm_maximo;
COMMENT ON SCHEMA ibm_maximo IS 'IBM Maximo (Austin, site AUSTIN): asset, assetspec, pm and workorder.';

CREATE TABLE IF NOT EXISTS ibm_maximo.asset (
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
COMMENT ON TABLE ibm_maximo.asset IS 'Assets (GMP equipment).';

INSERT INTO ibm_maximo.asset (assetnum, siteid, description, assettype, status, location, installdate, changedate) VALUES
('US10-DSP-01', 'AUSTIN', 'Downflow dispensing booth 1', 'DISPENSING BOOTH', 'OPERATING', 'US10-DIS', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-GRN-01', 'AUSTIN', 'High-shear granulator GMX-600', 'GRANULATOR', 'OPERATING', 'US10-GRA', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-FBD-01', 'AUSTIN', 'Fluid bed dryer WSG-300', 'FLUID BED DRYER', 'OPERATING', 'US10-FLU', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-CMP-01', 'AUSTIN', 'Rotary tablet press FE55', 'TABLET PRESS', 'OPERATING', 'US10-TAB', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-CMP-02', 'AUSTIN', 'Rotary tablet press FE35', 'TABLET PRESS', 'BROKEN', 'US10-TAB', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-COT-01', 'AUSTIN', 'Perforated pan coater BFC-200', 'COATER', 'OPERATING', 'US10-COA', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-PKG-01', 'AUSTIN', 'Bottle packaging and serialisation line 1', 'PACKAGING LINE', 'OPERATING', 'US10-PAC', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-CMX-01', 'AUSTIN', 'Cytotoxic compounding vessel 200 L', 'COMPOUNDING VESSEL', 'OPERATING', 'US10-COM', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-FIL-01', 'AUSTIN', 'Isolator vial filling line', 'ASEPTIC FILLING LINE', 'OPERATING', 'US10-ASE', '2019-06-01', '2026-09-29 02:00:00+00'),
('US10-VIS-01', 'AUSTIN', 'Automated visual inspection machine', 'INSPECTION MACHINE', 'OPERATING', 'US10-INS', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-BSC-03', 'AUSTIN', 'Class II biosafety cabinet, cell suite 3', 'BIOSAFETY CABINET', 'OPERATING', 'US10-BIO', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-INC-02', 'AUSTIN', 'CO2 incubator, cell suite 2', 'INCUBATOR', 'OPERATING', 'US10-INC', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-CRF-01', 'AUSTIN', 'Controlled-rate freezer', 'FREEZER', 'OPERATING', 'US10-FRE', '2019-06-01', '2026-08-31 02:00:00+00'),
('US10-HPLC-04', 'AUSTIN', 'UPLC system, QC lab bench 4', 'CHROMATOGRAPH', 'OPERATING', 'US10-CHR', '2021-03-15', '2026-08-31 02:00:00+00'),
('US10-GRN-00', 'AUSTIN', 'High-shear granulator GMX-300 (replaced)', 'GRANULATOR', 'DECOMMISSIONED', 'US10-GRA', '2019-06-01', '2026-08-31 02:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ibm_maximo.assetspec (
  assetnum    varchar(40) NOT NULL,
  siteid      varchar(10) NOT NULL,
  assetattrid varchar(40) NOT NULL,
  alnvalue    varchar(60),
  CONSTRAINT assetspec_pk PRIMARY KEY (assetnum, siteid, assetattrid)
);
COMMENT ON TABLE ibm_maximo.assetspec IS 'Classification attributes; GMP_QUAL_STATUS holds the qualification status.';

INSERT INTO ibm_maximo.assetspec (assetnum, siteid, assetattrid, alnvalue) VALUES
('US10-DSP-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-DSP-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-GRN-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-GRN-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-FBD-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-FBD-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-CMP-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-CMP-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-CMP-02', 'AUSTIN', 'GMP_QUAL_STATUS', 'NOT QUALIFIED'),
('US10-CMP-02', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-COT-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-COT-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-PKG-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-PKG-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-CMX-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-CMX-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-FIL-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'REQUAL DUE'),
('US10-FIL-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-VIS-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-VIS-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-BSC-03', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-BSC-03', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-INC-02', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-INC-02', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-CRF-01', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-CRF-01', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-HPLC-04', 'AUSTIN', 'GMP_QUAL_STATUS', 'QUALIFIED'),
('US10-HPLC-04', 'AUSTIN', 'GMP_CRITICAL', 'Y'),
('US10-GRN-00', 'AUSTIN', 'GMP_QUAL_STATUS', 'NOT QUALIFIED'),
('US10-GRN-00', 'AUSTIN', 'GMP_CRITICAL', 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ibm_maximo.pm (
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
COMMENT ON TABLE ibm_maximo.pm IS 'Preventive maintenance masters for calibration (CAL) and requalification (QUAL).';

INSERT INTO ibm_maximo.pm (pmnum, siteid, assetnum, worktype, frequency, frequnit, laststartdate, nextdate, status) VALUES
('PM-DSP-01-Q', 'AUSTIN', 'US10-DSP-01', 'QUAL', 24, 'MONTHS', '2025-11-18', '2027-11-18', 'ACTIVE'),
('PM-DSP-01-C', 'AUSTIN', 'US10-DSP-01', 'CAL', 6, 'MONTHS', '2026-05-12', '2026-11-12', 'ACTIVE'),
('PM-GRN-01-Q', 'AUSTIN', 'US10-GRN-01', 'QUAL', 24, 'MONTHS', '2025-03-10', '2027-03-10', 'ACTIVE'),
('PM-GRN-01-C', 'AUSTIN', 'US10-GRN-01', 'CAL', 6, 'MONTHS', '2026-06-02', '2026-12-02', 'ACTIVE'),
('PM-FBD-01-Q', 'AUSTIN', 'US10-FBD-01', 'QUAL', 24, 'MONTHS', '2025-03-12', '2027-03-12', 'ACTIVE'),
('PM-FBD-01-C', 'AUSTIN', 'US10-FBD-01', 'CAL', 6, 'MONTHS', '2026-06-03', '2026-12-03', 'ACTIVE'),
('PM-CMP-01-Q', 'AUSTIN', 'US10-CMP-01', 'QUAL', 24, 'MONTHS', '2024-10-21', '2026-10-21', 'ACTIVE'),
('PM-CMP-01-C', 'AUSTIN', 'US10-CMP-01', 'CAL', 6, 'MONTHS', '2026-04-14', '2026-10-14', 'ACTIVE'),
('PM-CMP-02-Q', 'AUSTIN', 'US10-CMP-02', 'QUAL', 24, 'MONTHS', '2024-02-05', '2026-02-05', 'ACTIVE'),
('PM-CMP-02-C', 'AUSTIN', 'US10-CMP-02', 'CAL', 6, 'MONTHS', '2026-01-20', '2026-07-20', 'ACTIVE'),
('PM-COT-01-Q', 'AUSTIN', 'US10-COT-01', 'QUAL', 24, 'MONTHS', '2025-06-30', '2027-06-30', 'ACTIVE'),
('PM-COT-01-C', 'AUSTIN', 'US10-COT-01', 'CAL', 6, 'MONTHS', '2026-06-18', '2026-12-18', 'ACTIVE'),
('PM-PKG-01-Q', 'AUSTIN', 'US10-PKG-01', 'QUAL', 24, 'MONTHS', '2025-08-25', '2027-08-25', 'ACTIVE'),
('PM-PKG-01-C', 'AUSTIN', 'US10-PKG-01', 'CAL', 6, 'MONTHS', '2026-08-11', '2027-02-11', 'ACTIVE'),
('PM-CMX-01-Q', 'AUSTIN', 'US10-CMX-01', 'QUAL', 12, 'MONTHS', '2026-09-04', '2027-09-04', 'ACTIVE'),
('PM-CMX-01-C', 'AUSTIN', 'US10-CMX-01', 'CAL', 6, 'MONTHS', '2026-09-04', '2027-03-04', 'ACTIVE'),
('PM-FIL-01-Q', 'AUSTIN', 'US10-FIL-01', 'QUAL', 12, 'MONTHS', '2025-09-29', '2026-09-29', 'ACTIVE'),
('PM-FIL-01-C', 'AUSTIN', 'US10-FIL-01', 'CAL', 3, 'MONTHS', '2026-07-06', '2026-10-06', 'ACTIVE'),
('PM-VIS-01-Q', 'AUSTIN', 'US10-VIS-01', 'QUAL', 12, 'MONTHS', '2026-02-16', '2027-02-16', 'ACTIVE'),
('PM-VIS-01-C', 'AUSTIN', 'US10-VIS-01', 'CAL', 6, 'MONTHS', '2026-08-17', '2027-02-17', 'ACTIVE'),
('PM-BSC-03-Q', 'AUSTIN', 'US10-BSC-03', 'QUAL', 12, 'MONTHS', '2026-01-26', '2027-01-26', 'ACTIVE'),
('PM-BSC-03-C', 'AUSTIN', 'US10-BSC-03', 'CAL', 6, 'MONTHS', '2026-07-27', '2027-01-27', 'ACTIVE'),
('PM-INC-02-Q', 'AUSTIN', 'US10-INC-02', 'QUAL', 12, 'MONTHS', '2025-12-08', '2026-12-08', 'ACTIVE'),
('PM-INC-02-C', 'AUSTIN', 'US10-INC-02', 'CAL', 3, 'MONTHS', '2026-06-08', '2026-09-08', 'ACTIVE'),
('PM-CRF-01-Q', 'AUSTIN', 'US10-CRF-01', 'QUAL', 12, 'MONTHS', '2025-10-13', '2026-10-13', 'ACTIVE'),
('PM-CRF-01-C', 'AUSTIN', 'US10-CRF-01', 'CAL', 6, 'MONTHS', '2026-04-13', '2026-10-13', 'ACTIVE'),
('PM-HPLC-04-Q', 'AUSTIN', 'US10-HPLC-04', 'QUAL', 24, 'MONTHS', '2025-07-14', '2027-07-14', 'ACTIVE'),
('PM-HPLC-04-C', 'AUSTIN', 'US10-HPLC-04', 'CAL', 12, 'MONTHS', '2026-07-14', '2027-07-14', 'ACTIVE'),
('PM-GRN-00-Q', 'AUSTIN', 'US10-GRN-00', 'QUAL', 24, 'MONTHS', '2019-05-06', '2021-05-06', 'INACTIVE'),
('PM-GRN-00-C', 'AUSTIN', 'US10-GRN-00', 'CAL', 6, 'MONTHS', '2023-11-06', '2024-05-06', 'INACTIVE')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ibm_maximo.workorder (
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
COMMENT ON TABLE ibm_maximo.workorder IS 'Work orders; completed (CLOSE/COMP) CAL and QUAL work orders are the calibration and qualification evidence.';

INSERT INTO ibm_maximo.workorder (wonum, siteid, assetnum, worktype, description, status, actfinish, pmnum) VALUES
('41213', 'AUSTIN', 'US10-DSP-01', 'QUAL', 'Periodic requalification Downflow dispensing booth 1', 'CLOSE', '2025-11-18 16:00:00+00', 'PM-DSP-01-Q'),
('41226', 'AUSTIN', 'US10-DSP-01', 'CAL', 'Calibration Downflow dispensing booth 1', 'CLOSE', '2026-05-12 15:30:00+00', 'PM-DSP-01-C'),
('41239', 'AUSTIN', 'US10-GRN-01', 'QUAL', 'Periodic requalification High-shear granulator GMX-600', 'CLOSE', '2025-03-10 16:00:00+00', 'PM-GRN-01-Q'),
('41252', 'AUSTIN', 'US10-GRN-01', 'CAL', 'Calibration High-shear granulator GMX-600', 'CLOSE', '2026-06-02 15:30:00+00', 'PM-GRN-01-C'),
('41265', 'AUSTIN', 'US10-FBD-01', 'QUAL', 'Periodic requalification Fluid bed dryer WSG-300', 'CLOSE', '2025-03-12 16:00:00+00', 'PM-FBD-01-Q'),
('41278', 'AUSTIN', 'US10-FBD-01', 'CAL', 'Calibration Fluid bed dryer WSG-300', 'CLOSE', '2026-06-03 15:30:00+00', 'PM-FBD-01-C'),
('41291', 'AUSTIN', 'US10-CMP-01', 'QUAL', 'Periodic requalification Rotary tablet press FE55', 'CLOSE', '2024-10-21 16:00:00+00', 'PM-CMP-01-Q'),
('41304', 'AUSTIN', 'US10-CMP-01', 'CAL', 'Calibration Rotary tablet press FE55', 'CLOSE', '2026-04-14 15:30:00+00', 'PM-CMP-01-C'),
('41317', 'AUSTIN', 'US10-CMP-01', 'CAL', 'Calibration Rotary tablet press FE55', 'WSCH', NULL, 'PM-CMP-01-C'),
('41330', 'AUSTIN', 'US10-CMP-01', 'QUAL', 'Periodic requalification Rotary tablet press FE55', 'WAPPR', NULL, 'PM-CMP-01-Q'),
('41343', 'AUSTIN', 'US10-CMP-02', 'QUAL', 'Periodic requalification Rotary tablet press FE35', 'CLOSE', '2024-02-05 16:00:00+00', 'PM-CMP-02-Q'),
('41356', 'AUSTIN', 'US10-CMP-02', 'CAL', 'Calibration Rotary tablet press FE35', 'CLOSE', '2026-01-20 15:30:00+00', 'PM-CMP-02-C'),
('41369', 'AUSTIN', 'US10-CMP-02', 'CAL', 'Calibration Rotary tablet press FE35', 'WSCH', NULL, 'PM-CMP-02-C'),
('41382', 'AUSTIN', 'US10-CMP-02', 'QUAL', 'Periodic requalification Rotary tablet press FE35', 'WAPPR', NULL, 'PM-CMP-02-Q'),
('41395', 'AUSTIN', 'US10-COT-01', 'QUAL', 'Periodic requalification Perforated pan coater BFC-200', 'CLOSE', '2025-06-30 16:00:00+00', 'PM-COT-01-Q'),
('41408', 'AUSTIN', 'US10-COT-01', 'CAL', 'Calibration Perforated pan coater BFC-200', 'CLOSE', '2026-06-18 15:30:00+00', 'PM-COT-01-C'),
('41421', 'AUSTIN', 'US10-PKG-01', 'QUAL', 'Periodic requalification Bottle packaging and serialisation line 1', 'CLOSE', '2025-08-25 16:00:00+00', 'PM-PKG-01-Q'),
('41434', 'AUSTIN', 'US10-PKG-01', 'CAL', 'Calibration Bottle packaging and serialisation line 1', 'CLOSE', '2026-08-11 15:30:00+00', 'PM-PKG-01-C'),
('41447', 'AUSTIN', 'US10-CMX-01', 'QUAL', 'Periodic requalification Cytotoxic compounding vessel 200 L', 'CLOSE', '2026-09-04 16:00:00+00', 'PM-CMX-01-Q'),
('41460', 'AUSTIN', 'US10-CMX-01', 'CAL', 'Calibration Cytotoxic compounding vessel 200 L', 'CLOSE', '2026-09-04 15:30:00+00', 'PM-CMX-01-C'),
('41473', 'AUSTIN', 'US10-FIL-01', 'QUAL', 'Periodic requalification Isolator vial filling line', 'CLOSE', '2025-09-29 16:00:00+00', 'PM-FIL-01-Q'),
('41486', 'AUSTIN', 'US10-FIL-01', 'CAL', 'Calibration Isolator vial filling line', 'CLOSE', '2026-07-06 15:30:00+00', 'PM-FIL-01-C'),
('41499', 'AUSTIN', 'US10-FIL-01', 'CAL', 'Calibration Isolator vial filling line', 'WSCH', NULL, 'PM-FIL-01-C'),
('41512', 'AUSTIN', 'US10-FIL-01', 'QUAL', 'Periodic requalification Isolator vial filling line', 'WAPPR', NULL, 'PM-FIL-01-Q'),
('41525', 'AUSTIN', 'US10-VIS-01', 'QUAL', 'Periodic requalification Automated visual inspection machine', 'CLOSE', '2026-02-16 16:00:00+00', 'PM-VIS-01-Q'),
('41538', 'AUSTIN', 'US10-VIS-01', 'CAL', 'Calibration Automated visual inspection machine', 'CLOSE', '2026-08-17 15:30:00+00', 'PM-VIS-01-C'),
('41551', 'AUSTIN', 'US10-BSC-03', 'QUAL', 'Periodic requalification Class II biosafety cabinet, cell suite 3', 'CLOSE', '2026-01-26 16:00:00+00', 'PM-BSC-03-Q'),
('41564', 'AUSTIN', 'US10-BSC-03', 'CAL', 'Calibration Class II biosafety cabinet, cell suite 3', 'CLOSE', '2026-07-27 15:30:00+00', 'PM-BSC-03-C'),
('41577', 'AUSTIN', 'US10-INC-02', 'QUAL', 'Periodic requalification CO2 incubator, cell suite 2', 'CLOSE', '2025-12-08 16:00:00+00', 'PM-INC-02-Q'),
('41590', 'AUSTIN', 'US10-INC-02', 'CAL', 'Calibration CO2 incubator, cell suite 2', 'CLOSE', '2026-06-08 15:30:00+00', 'PM-INC-02-C'),
('41603', 'AUSTIN', 'US10-INC-02', 'CAL', 'Calibration CO2 incubator, cell suite 2', 'WSCH', NULL, 'PM-INC-02-C'),
('41616', 'AUSTIN', 'US10-CRF-01', 'QUAL', 'Periodic requalification Controlled-rate freezer', 'CLOSE', '2025-10-13 16:00:00+00', 'PM-CRF-01-Q'),
('41629', 'AUSTIN', 'US10-CRF-01', 'CAL', 'Calibration Controlled-rate freezer', 'CLOSE', '2026-04-13 15:30:00+00', 'PM-CRF-01-C'),
('41642', 'AUSTIN', 'US10-CRF-01', 'CAL', 'Calibration Controlled-rate freezer', 'WSCH', NULL, 'PM-CRF-01-C'),
('41655', 'AUSTIN', 'US10-CRF-01', 'QUAL', 'Periodic requalification Controlled-rate freezer', 'WAPPR', NULL, 'PM-CRF-01-Q'),
('41668', 'AUSTIN', 'US10-HPLC-04', 'QUAL', 'Periodic requalification UPLC system, QC lab bench 4', 'CLOSE', '2025-07-14 16:00:00+00', 'PM-HPLC-04-Q'),
('41681', 'AUSTIN', 'US10-HPLC-04', 'CAL', 'Calibration UPLC system, QC lab bench 4', 'CLOSE', '2026-07-14 15:30:00+00', 'PM-HPLC-04-C'),
('41694', 'AUSTIN', 'US10-GRN-00', 'QUAL', 'Periodic requalification High-shear granulator GMX-300 (replaced)', 'CLOSE', '2019-05-06 16:00:00+00', 'PM-GRN-00-Q'),
('41707', 'AUSTIN', 'US10-GRN-00', 'CAL', 'Calibration High-shear granulator GMX-300 (replaced)', 'CLOSE', '2023-11-06 15:30:00+00', 'PM-GRN-00-C')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA ibm_maximo TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ibm_maximo TO egeria_user, airflow_user;
