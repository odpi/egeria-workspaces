-- system-qualified-name: System::procurement01
-- Coco Pharmaceuticals Procurement - Coco core.  COTS purchasing system at Amsterdam, the global one of Coco's five purchasing systems; feeds Supplier Master Data and Third Party Onboarding Cases.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS procurement01;
COMMENT ON SCHEMA procurement01 IS 'Coco Pharmaceuticals Procurement procurement01 (Coco core): vendors, bank details, anomalies, onboarding cases and screening.';

CREATE TABLE IF NOT EXISTS procurement01.vendor (
  vendor_no integer NOT NULL,
  vendor_name varchar(80) NOT NULL,
  vendor_class varchar(3) NOT NULL,
  inc_country varchar(20) NOT NULL,
  approved_ind char(1) NOT NULL,
  approved_on date,
  vendor_status char(1) NOT NULL,
  CONSTRAINT vendor_pk PRIMARY KEY (vendor_no)
);
COMMENT ON TABLE procurement01.vendor IS 'Approved vendors (vendor_no is the Coco supplier id). vendor_class MAT material, SVC service, HCO healthcare organisation, OTH other; vendor_status A active, S suspended, C closed.';

CREATE TABLE IF NOT EXISTS procurement01.vendor_bank (
  vendor_no integer NOT NULL,
  seq smallint NOT NULL,
  acct_masked varchar(30) NOT NULL,
  bank_name varchar(80) NOT NULL,
  bank_country varchar(20) NOT NULL,
  change_ref varchar(20) NOT NULL,
  verified_on date NOT NULL,
  active_ind char(1) NOT NULL,
  CONSTRAINT vendor_bank_pk PRIMARY KEY (vendor_no, seq)
);
COMMENT ON TABLE procurement01.vendor_bank IS 'Vendor bank account history; active_ind Y marks the account payments go to; change_ref is the verified payment-detail change.';

CREATE TABLE IF NOT EXISTS procurement01.vendor_anomaly (
  anomaly_ref varchar(20) NOT NULL,
  vendor_no integer NOT NULL,
  raised_on date NOT NULL,
  anomaly_text text NOT NULL,
  anomaly_status varchar(6) NOT NULL,
  CONSTRAINT vendor_anomaly_pk PRIMARY KEY (anomaly_ref)
);
COMMENT ON TABLE procurement01.vendor_anomaly IS 'Concerns raised by transaction monitoring against a vendor.';

CREATE TABLE IF NOT EXISTS procurement01.onboard_case (
  case_no varchar(12) NOT NULL,
  prop_name varchar(80) NOT NULL,
  prop_country varchar(20) NOT NULL,
  ubo_decl text,
  requested_by varchar(20) NOT NULL,
  opened_on date NOT NULL,
  case_status varchar(4) NOT NULL,
  vendor_no integer,
  CONSTRAINT onboard_case_pk PRIMARY KEY (case_no)
);
COMMENT ON TABLE procurement01.onboard_case IS 'Third-party onboarding cases. case_status SCR screening, RISK risk assessment, APPR approved, REJ rejected; requested_by is the requester''s worker pseudonym.';

CREATE TABLE IF NOT EXISTS procurement01.vendor_screening (
  screen_ref varchar(16) NOT NULL,
  vendor_no integer,
  case_no varchar(12),
  screen_type varchar(4) NOT NULL,
  requested_ts timestamptz NOT NULL,
  result varchar(6),
  result_dt date,
  risk_rating varchar(4),
  CONSTRAINT vendor_screening_pk PRIMARY KEY (screen_ref)
);
COMMENT ON TABLE procurement01.vendor_screening IS 'Screening requests to the external service, from onboarding cases and from the periodic re-screen. screen_type SANC, PEP, ADVM, ALL; result CLEAR, REVIEW, BLOCK.';

INSERT INTO procurement01.vendor (vendor_no, vendor_name, vendor_class, inc_country, approved_ind, approved_on, vendor_status) VALUES
(1000, 'Generic Medicines Ltd', 'MAT', 'UK', 'Y', '2012-03-01', 'A'),
(2000, 'Texas Tablets', 'MAT', 'USA', 'Y', '2012-03-01', 'A'),
(3000, 'Groote Generics', 'MAT', 'Netherland', 'Y', '2013-06-10', 'A'),
(4000, 'Worldwide Fleet Supplies', 'SVC', 'USA', 'Y', '2014-09-15', 'A'),
(5000, 'Amazon Botanicals', 'MAT', 'Brazil', 'Y', '2016-02-01', 'S'),
(6000, 'Southern Gas and Electric', 'SVC', 'UK', 'Y', '2015-01-05', 'A'),
(6001, 'NLE', 'SVC', 'Netherland', 'Y', '2015-01-05', 'A'),
(6002, 'Austin Energy', 'SVC', 'USA', 'Y', '2015-01-05', 'A'),
(7000, 'BASE', 'MAT', 'Germany', 'Y', '2021-04-12', 'A'),
(8000, 'Lushplanet', 'MAT', 'USA', 'Y', '2022-02-03', 'A'),
(9000, 'Worldwide Excipients', 'MAT', 'India', 'Y', '2022-03-21', 'A'),
(10000, 'Petes Office Supplies', 'OTH', 'Sweden', 'Y', '2022-07-11', 'C'),
(11000, 'Helix Vector Sciences Ltd', 'MAT', 'UK', 'Y', '2026-08-28', 'A')
ON CONFLICT DO NOTHING;

INSERT INTO procurement01.vendor_bank (vendor_no, seq, acct_masked, bank_name, bank_country, change_ref, verified_on, active_ind) VALUES
(1000, 1, 'GB33BUKB****2201', 'Barclays Bank UK PLC', 'UK', 'PDC-2012-0004', '2025-11-03', 'Y'),
(2000, 1, 'US-****4471', 'Frost Bank', 'USA', 'PDC-2012-0005', '2025-11-04', 'Y'),
(3000, 1, 'NL91ABNA****7732', 'ABN AMRO Bank N.V.', 'Netherland', 'PDC-2013-0011', '2025-11-04', 'Y'),
(4000, 1, 'US-****9920', 'JPMorgan Chase Bank N.A.', 'USA', 'PDC-2014-0020', '2025-11-05', 'N'),
(4000, 2, 'MT84MALT****3050', 'Bank of Valletta p.l.c.', 'Malta', 'PDC-2026-0041', '2026-09-04', 'Y'),
(5000, 1, 'BR15****0001', 'Banco do Brasil S.A.', 'Brazil', 'PDC-2016-0002', '2024-06-12', 'Y'),
(6000, 1, 'GB82LOYD****5521', 'Lloyds Bank plc', 'UK', 'PDC-2015-0001', '2025-11-03', 'Y'),
(6001, 1, 'NL02RABO****4410', 'Rabobank', 'Netherland', 'PDC-2015-0002', '2025-11-04', 'Y'),
(6002, 1, 'US-****7263', 'Wells Fargo Bank N.A.', 'USA', 'PDC-2015-0003', '2025-11-05', 'Y'),
(7000, 1, 'DE89COBA****3000', 'Commerzbank AG', 'Germany', 'PDC-2021-0007', '2025-11-06', 'Y'),
(8000, 1, 'US-****1180', 'Regions Bank', 'USA', 'PDC-2022-0003', '2025-11-06', 'Y'),
(9000, 1, 'IN-****6620', 'State Bank of India', 'India', 'PDC-2022-0004', '2025-11-07', 'Y'),
(10000, 1, 'SE45HAND****1211', 'Svenska Handelsbanken AB', 'Sweden', 'PDC-2022-0009', '2024-07-01', 'Y'),
(11000, 1, 'GB60NWBK****5519', 'National Westminster Bank plc', 'UK', 'PDC-2026-0038', '2026-08-27', 'Y')
ON CONFLICT DO NOTHING;

INSERT INTO procurement01.vendor_anomaly (anomaly_ref, vendor_no, raised_on, anomaly_text, anomaly_status) VALUES
('ANOM-26-0007', 4000, '2026-09-12', 'Bank details changed to an overseas account days before an unmatched invoice was paid.', 'OPEN'),
('ANOM-26-0003', 9000, '2026-04-18', 'Duplicate invoice number submitted twice.', 'CLOSED')
ON CONFLICT DO NOTHING;

INSERT INTO procurement01.onboard_case (case_no, prop_name, prop_country, ubo_decl, requested_by, opened_on, case_status, vendor_no) VALUES
('OB-21-0002', 'BASE', 'Germany', 'Listed company; no beneficial owner above 25%.', 'CW-E82P52', '2021-03-01', 'APPR', 7000),
('OB-22-0001', 'Lushplanet', 'USA', 'Owned by F. Flower (100%).', 'CW-RMRC8S', '2022-01-10', 'APPR', 8000),
('OB-22-0003', 'Worldwide Excipients', 'India', 'Owned by Fuller Holdings Pvt Ltd (P. Fuller 60%).', 'CW-SFRGJQ', '2022-02-14', 'APPR', 9000),
('OB-22-0008', 'Petes Office Supplies', 'Sweden', 'Owned by P. Piper (100%).', 'CW-7K8YQG', '2022-06-20', 'APPR', 10000),
('OB-26-0011', 'Helix Vector Sciences Ltd', 'UK', 'Venture-backed; largest holder Bio Ventures Fund III LP (38%).', 'CW-SFRGJQ', '2026-07-06', 'APPR', 11000),
('OB-26-0014', 'Cryo Logistics BV', 'Netherland', 'Owned by Koude Keten Holding BV (100%).', 'CW-7G8SM2', '2026-09-08', 'SCR', NULL),
('OB-26-0017', 'Pinnacle Pharma Consulting Ltd', 'UK', 'Director and 100% owner is a serving member of a hospital procurement board.', 'CW-5V7T2Y', '2026-07-22', 'REJ', NULL),
('OB-26-0019', 'Nordic Excipients AB', 'Sweden', 'Owned by Nordic Chem Group AB (100%).', 'CW-G32FNJ', '2026-08-31', 'RISK', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO procurement01.vendor_screening (screen_ref, vendor_no, case_no, screen_type, requested_ts, result, result_dt, risk_rating) VALUES
('SCR-21-0031', 7000, 'OB-21-0002', 'ALL', '2021-03-02 09:10+00', 'CLEAR', '2021-03-03', 'LOW'),
('SCR-22-0004', 8000, 'OB-22-0001', 'ALL', '2022-01-11 14:00+00', 'CLEAR', '2022-01-12', 'LOW'),
('SCR-22-0009', 9000, 'OB-22-0003', 'SANC', '2022-02-15 10:30+00', 'CLEAR', '2022-02-15', 'MED'),
('SCR-22-0010', 9000, 'OB-22-0003', 'PEP', '2022-02-15 10:31+00', 'CLEAR', '2022-02-16', 'MED'),
('SCR-22-0027', 10000, 'OB-22-0008', 'ALL', '2022-06-21 08:45+00', 'CLEAR', '2022-06-21', 'LOW'),
('SCR-26-0102', 11000, 'OB-26-0011', 'ALL', '2026-07-07 09:00+00', 'CLEAR', '2026-07-08', 'LOW'),
('SCR-26-0103', 11000, 'OB-26-0011', 'ADVM', '2026-07-07 09:02+00', 'CLEAR', '2026-07-09', 'LOW'),
('SCR-26-0131', NULL, 'OB-26-0017', 'PEP', '2026-07-23 11:15+00', 'REVIEW', '2026-07-24', 'HIGH'),
('SCR-26-0132', NULL, 'OB-26-0017', 'ADVM', '2026-07-23 11:16+00', 'CLEAR', '2026-07-24', 'HIGH'),
('SCR-26-0158', NULL, 'OB-26-0019', 'ALL', '2026-09-01 08:20+00', 'CLEAR', '2026-09-02', NULL),
('SCR-26-0171', NULL, 'OB-26-0014', 'ALL', '2026-09-29 15:40+00', NULL, NULL, NULL),
('SCR-26-Q2-001', 1000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-002', 2000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-003', 3000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q3-004', 4000, NULL, 'ALL', '2026-09-05 06:00+00', 'REVIEW', '2026-09-05', 'HIGH'),
('SCR-26-Q2-005', 5000, NULL, 'SANC', '2026-05-04 06:00+00', 'BLOCK', '2026-05-04', 'MED'),
('SCR-26-Q2-006', 6000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-007', 6001, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-008', 6002, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-009', 7000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-010', 8000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW'),
('SCR-26-Q2-011', 9000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'MED'),
('SCR-26-Q2-012', 10000, NULL, 'SANC', '2026-05-04 06:00+00', 'CLEAR', '2026-05-04', 'LOW')
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS procurement01.anomaly_alert (
  alert_ref varchar(40) NOT NULL,
  detected_ts timestamptz NOT NULL,
  alert_type varchar(40) NOT NULL,
  vendor_no integer,
  worker_ref varchar(40),
  alert_text text NOT NULL,
  severity varchar(20) NOT NULL,
  alert_status varchar(20) NOT NULL,
  CONSTRAINT anomaly_alert_pk PRIMARY KEY (alert_ref)
);
COMMENT ON TABLE procurement01.anomaly_alert IS 'Alerts from transaction monitoring (Payment Anomaly Findings) for buyers to review; a confirmed concern is raised against the vendor in vendor_anomaly.';

CREATE TABLE IF NOT EXISTS procurement01.anomaly_alert_txn (
  alert_ref varchar(40) NOT NULL,
  txn_ref varchar(40) NOT NULL,
  txn_type varchar(20) NOT NULL,
  txn_amount numeric(18,2) NOT NULL,
  txn_date date NOT NULL,
  CONSTRAINT anomaly_alert_txn_pk PRIMARY KEY (alert_ref, txn_ref)
);
COMMENT ON TABLE procurement01.anomaly_alert_txn IS 'The transactions behind each anomaly alert.';

CREATE TABLE IF NOT EXISTS procurement01.bank_chg_req (
  change_ref varchar(40) NOT NULL,
  vendor_no integer NOT NULL,
  requested_ts timestamptz NOT NULL,
  requested_by varchar(80) NOT NULL,
  acct_prev varchar(40),
  acct_new varchar(40) NOT NULL,
  chg_status varchar(20) NOT NULL,
  verified_ts timestamptz,
  verified_by varchar(40),
  verify_channel varchar(40),
  verify_notes text,
  CONSTRAINT bank_chg_req_pk PRIMARY KEY (change_ref)
);
COMMENT ON TABLE procurement01.bank_chg_req IS 'Vendor bank detail change requests with their call-back verification (Supplier Payment Detail Changes); only a verified change becomes a new vendor_bank row.';

CREATE TABLE IF NOT EXISTS procurement01.screen_result (
  screen_ref varchar(16) NOT NULL,
  party_name varchar(200) NOT NULL,
  result_dt date NOT NULL,
  result_status varchar(20) NOT NULL,
  match_cnt integer NOT NULL,
  rating varchar(20),
  CONSTRAINT screen_result_pk PRIMARY KEY (screen_ref)
);
COMMENT ON TABLE procurement01.screen_result IS 'Results returned by the external screening service (Third Party Screening Results) for screenings requested in vendor_screening, waiting for the buyer to record the outcome.';

CREATE TABLE IF NOT EXISTS procurement01.screen_hit (
  screen_ref varchar(16) NOT NULL,
  list_name varchar(120) NOT NULL,
  hit_name varchar(200) NOT NULL,
  hit_rating varchar(20) NOT NULL,
  hit_text text,
  CONSTRAINT screen_hit_pk PRIMARY KEY (screen_ref, list_name, hit_name)
);
COMMENT ON TABLE procurement01.screen_hit IS 'Watch-list matches behind each screening result.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA procurement01 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA procurement01 TO egeria_user, airflow_user;
