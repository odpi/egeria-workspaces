-- system-qualified-name: System::NL payroll
-- Netherlands payroll - Coco core.  COTS payroll with Dutch tax calculations for Coco Pharmaceuticals B.V. (Amsterdam), Dutch-language configuration; feeds Payroll Results.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS nl_payroll;
COMMENT ON SCHEMA nl_payroll IS 'Netherlands payroll (Coco core): medewerkers, verloningsruns and loonstroken.';

CREATE TABLE IF NOT EXISTS nl_payroll.medewerker (
  personeelsnr varchar(8) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  hr_emp_no varchar(10) NOT NULL,
  voornaam varchar(40) NOT NULL,
  achternaam varchar(40) NOT NULL,
  kostenplaats varchar(10) NOT NULL,
  datum_in_dienst date NOT NULL,
  datum_uit_dienst date,
  CONSTRAINT medewerker_pk PRIMARY KEY (personeelsnr)
);
COMMENT ON TABLE nl_payroll.medewerker IS 'Employees on the Dutch payroll (personeelsnr = payroll number), with the HRIM pseudonym.';

CREATE TABLE IF NOT EXISTS nl_payroll.verloningsrun (
  run_id varchar(12) NOT NULL,
  werkgever varchar(10) NOT NULL,
  periode integer NOT NULL,
  betaaldatum date NOT NULL,
  aantal_medewerkers integer NOT NULL,
  totaal_bruto numeric(14,2) NOT NULL,
  valuta varchar(3) NOT NULL,
  status varchar(12) NOT NULL,
  CONSTRAINT verloningsrun_pk PRIMARY KEY (run_id)
);
COMMENT ON TABLE nl_payroll.verloningsrun IS 'Pay runs; periode is yyyymm; status concept or definitief.';

CREATE TABLE IF NOT EXISTS nl_payroll.loonstrook (
  run_id varchar(12) NOT NULL,
  personeelsnr varchar(8) NOT NULL,
  bruto numeric(12,2) NOT NULL,
  werkgeverslasten numeric(12,2) NOT NULL,
  netto numeric(12,2) NOT NULL,
  kostenplaats varchar(10) NOT NULL,
  grootboekrekening varchar(10) NOT NULL,
  CONSTRAINT loonstrook_pk PRIMARY KEY (run_id, personeelsnr)
);
COMMENT ON TABLE nl_payroll.loonstrook IS 'Payslips: gross, employer charges, net, cost centre and ledger account.';

INSERT INTO nl_payroll.medewerker (personeelsnr, worker_ref, hr_emp_no, voornaam, achternaam, kostenplaats, datum_in_dienst, datum_uit_dienst) VALUES
('7001', 'CW-38FTNV', '439222', 'Steve', 'Starter', '9999', '2010-01-01', NULL),
('7002', 'CW-TC93US', '139870', 'Faith', 'Broker', '2373', '2018-02-01', NULL),
('7003', 'CW-7K8YQG', '199995', 'Gary', 'Geeke', '3082', '2020-05-01', NULL),
('7004', 'CW-FM4E2G', '338575', 'Polly', 'Tasker', '2373', '2022-04-01', NULL),
('7005', 'CW-T3HUQE', '818928', 'Lemmie', 'Stage', '3082', '2019-05-01', NULL),
('7006', 'CW-DLMYL9', '458109', 'Bob', 'Nitter', '3082', '2023-01-09', NULL),
('7007', 'CW-K34WSJ', '549922', 'Maura', 'Zeller', '7432', '2012-01-01', '2026-09-18')
ON CONFLICT DO NOTHING;

INSERT INTO nl_payroll.verloningsrun (run_id, werkgever, periode, betaaldatum, aantal_medewerkers, totaal_bruto, valuta, status) VALUES
('VR-202608', 'COCO-NL', 202608, '2026-08-25', 7, 54320.99, 'EUR', 'definitief'),
('VR-202609', 'COCO-NL', 202609, '2026-09-24', 7, 54495.68, 'EUR', 'definitief')
ON CONFLICT DO NOTHING;

INSERT INTO nl_payroll.loonstrook (run_id, personeelsnr, bruto, werkgeverslasten, netto, kostenplaats, grootboekrekening) VALUES
('VR-202608', '7001', 15817.9, 3321.76, 9965.28, '9999', '6100'),
('VR-202608', '7002', 10956.79, 2300.93, 6902.78, '2373', '6100'),
('VR-202608', '7003', 7407.41, 1555.56, 4666.67, '3082', '6100'),
('VR-202608', '7004', 6481.48, 1361.11, 4083.33, '2373', '6100'),
('VR-202608', '7005', 5478.4, 1150.46, 3451.39, '3082', '6100'),
('VR-202608', '7006', 3240.74, 680.56, 2041.67, '3082', '6100'),
('VR-202608', '7007', 4938.27, 1037.04, 3111.11, '7432', '6100'),
('VR-202609', '7001', 15817.9, 3321.76, 9965.28, '9999', '6100'),
('VR-202609', '7002', 10956.79, 2300.93, 6902.78, '2373', '6100'),
('VR-202609', '7003', 7407.41, 1555.56, 4666.67, '3082', '6100'),
('VR-202609', '7004', 6481.48, 1361.11, 4083.33, '2373', '6100'),
('VR-202609', '7005', 5478.4, 1150.46, 3451.39, '3082', '6100'),
('VR-202609', '7006', 3240.74, 680.56, 2041.67, '3082', '6100'),
('VR-202609', '7007', 5112.96, 1073.72, 3221.16, '7432', '6100')
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS nl_payroll.hr_mutatie (
  worker_ref varchar(20) NOT NULL,
  werkgever varchar(10) NOT NULL,
  vestiging varchar(4) NOT NULL,
  datum_in_dienst date NOT NULL,
  datum_uit_dienst date,
  dienstverband_status varchar(10) NOT NULL,
  functie_code varchar(40),
  functie_naam varchar(120),
  kostenplaats varchar(10),
  leidinggevende_ref varchar(20),
  CONSTRAINT hr_mutatie_pk PRIMARY KEY (worker_ref)
);
COMMENT ON TABLE nl_payroll.hr_mutatie IS 'HR mutaties: the latest worker record for each Dutch payroll employee received from Worker Master Data, for setting up new medewerkers and processing leavers (uit dienst).';

-- End of subscription tables.

GRANT USAGE ON SCHEMA nl_payroll TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA nl_payroll TO egeria_user, airflow_user;
