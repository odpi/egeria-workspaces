-- system-qualified-name: System::coco-hrim
-- Human Resources Information Manager (HRIM) - Coco core.  COTS central HR application for hiring, skills management and all reasons for termination; feeds Worker Master Data, Worker Lifecycle Events, Role Competency Requirements and Worker Qualifications.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS coco_hrim;
COMMENT ON SCHEMA coco_hrim IS 'Human Resources Information Manager coco-hrim (Coco core): workers, assignments, jobs, competencies and HR events.';

CREATE TABLE IF NOT EXISTS coco_hrim.job (
  job_code varchar(12) NOT NULL,
  job_title varchar(80) NOT NULL,
  haz_profile text,
  CONSTRAINT job_pk PRIMARY KEY (job_code)
);
COMMENT ON TABLE coco_hrim.job IS 'Jobs, with the hazard exposure profile of the role.';

CREATE TABLE IF NOT EXISTS coco_hrim.person (
  emp_no varchar(10) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  given_name varchar(40) NOT NULL,
  family_name varchar(40) NOT NULL,
  worker_cat varchar(3) NOT NULL,
  company varchar(10) NOT NULL,
  location varchar(4) NOT NULL,
  hire_date date NOT NULL,
  term_date date,
  emp_status char(1) NOT NULL,
  CONSTRAINT person_pk PRIMARY KEY (emp_no)
);
COMMENT ON TABLE coco_hrim.person IS 'Every worker. worker_ref is the pseudonym HRIM issues to other systems; worker_cat EMP/CTR; emp_status A active, L leave, T terminated.';

CREATE TABLE IF NOT EXISTS coco_hrim.job_assignment (
  emp_no varchar(10) NOT NULL,
  eff_date date NOT NULL,
  job_code varchar(12) NOT NULL,
  cost_center varchar(10) NOT NULL,
  mgr_emp_no varchar(10),
  spend_auth numeric(12,2) NOT NULL,
  CONSTRAINT job_assignment_pk PRIMARY KEY (emp_no, eff_date)
);
COMMENT ON TABLE coco_hrim.job_assignment IS 'Effective-dated job assignments (cost centre = Coco department number); spend_auth 0 means none.';

CREATE TABLE IF NOT EXISTS coco_hrim.competency (
  comp_cd varchar(10) NOT NULL,
  comp_name varchar(80) NOT NULL,
  comp_desc text NOT NULL,
  refresh_mths smallint NOT NULL,
  regulated_yn char(1) NOT NULL,
  CONSTRAINT competency_pk PRIMARY KEY (comp_cd)
);
COMMENT ON TABLE coco_hrim.competency IS 'Competencies managed in skills management.';

CREATE TABLE IF NOT EXISTS coco_hrim.job_competency (
  job_code varchar(12) NOT NULL,
  comp_cd varchar(10) NOT NULL,
  eff_date date NOT NULL,
  CONSTRAINT job_competency_pk PRIMARY KEY (job_code, comp_cd)
);
COMMENT ON TABLE coco_hrim.job_competency IS 'Competencies each job requires, from the date the requirement took effect.';

CREATE TABLE IF NOT EXISTS coco_hrim.emp_competency (
  emp_no varchar(10) NOT NULL,
  comp_cd varchar(10) NOT NULL,
  achieved_dt date NOT NULL,
  expiry_dt date NOT NULL,
  training_ref varchar(20) NOT NULL,
  cert_no varchar(30),
  CONSTRAINT emp_competency_pk PRIMARY KEY (emp_no, comp_cd)
);
COMMENT ON TABLE coco_hrim.emp_competency IS 'Competencies held by each worker with the training completion and any external certificate.';

CREATE TABLE IF NOT EXISTS coco_hrim.hr_event (
  event_id varchar(16) NOT NULL,
  emp_no varchar(10) NOT NULL,
  event_type varchar(3) NOT NULL,
  eff_date date NOT NULL,
  raised_at timestamptz NOT NULL,
  new_job_code varchar(12),
  event_text text NOT NULL,
  CONSTRAINT hr_event_pk PRIMARY KEY (event_id)
);
COMMENT ON TABLE coco_hrim.hr_event IS 'HR events: HIR hire, XFR transfer/promotion, TER termination.';

CREATE TABLE IF NOT EXISTS coco_hrim.hr_event_dist (
  event_id varchar(16) NOT NULL,
  target_sys varchar(30) NOT NULL,
  sent_at timestamptz NOT NULL,
  ack_yn char(1) NOT NULL,
  ack_at timestamptz,
  CONSTRAINT hr_event_dist_pk PRIMARY KEY (event_id, target_sys)
);
COMMENT ON TABLE coco_hrim.hr_event_dist IS 'Notification of events to downstream systems and their acknowledgement (distribution tracking began with V5.2 in 2025).';

INSERT INTO coco_hrim.job (job_code, job_title, haz_profile) VALUES
('EXEC-FDR', 'Founder and Site Head', NULL),
('EXEC-CFO', 'Chief Finance Officer', NULL),
('EXEC-CDO', 'Chief Data Officer', NULL),
('EXEC-HRD', 'HR Director and Chief Privacy Officer', NULL),
('EXEC-CISO', 'Chief Information Security Officer', NULL),
('EXEC-MFG', 'Head of Manufacturing', 'Site visits to manufacturing areas; OEB3 areas with escort.'),
('FIN-ACM', 'Accounts Manager, Finance HQ', NULL),
('FIN-PAY', 'Payments Clerk', NULL),
('PRC-MGR', 'Procurement Manager', NULL),
('SAL-LDR', 'Sales Leader', NULL),
('SAL-REP', 'Sales Representative', NULL),
('IT-INFRA', 'IT Infrastructure Lead', NULL),
('IT-PM', 'IT Project Leader', NULL),
('IT-INT', 'Integration Architect and Developer', NULL),
('IT-ETL', 'DataStage Specialist', NULL),
('DAT-ARC', 'Information Architect', NULL),
('DAT-ANL', 'Information Analyst', NULL),
('DAT-SCI', 'Data Scientist', NULL),
('RES-LEAD', 'Lead Researcher', 'Laboratory work with cell lines and viral vectors (biological agents group 2).'),
('CLN-REC', 'Clinical Records Clerk', NULL),
('MFG-OPR', 'Manufacturing Operator', 'API powders up to OEB3 (rosuvastatin, amlodipine, metoprolol); ethanol and IPA cleaning agents.'),
('MFG-SUP', 'Manufacturing Supervisor', 'API powders up to OEB3; sodium hydroxide cleaning solution.'),
('MFG-CTO', 'Cell Therapy Operator', 'Autologous patient material, lentiviral vector (GMO contained use class 1-2), liquid nitrogen, DMSO.'),
('MFG-QP', 'Qualified Person', 'Occasional entry to production and QC areas.'),
('DEP-DGS', 'Depot Dangerous Goods Supervisor', 'Packed dangerous goods in transport packaging; dry ice; liquid nitrogen dry shippers.'),
('SEC-CON', 'Security Consultant', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.person (emp_no, worker_ref, given_name, family_name, worker_cat, company, location, hire_date, term_date, emp_status) VALUES
('371803', 'CW-KTVC4J', 'Terri', 'Daring', 'EMP', 'COCO-UK', 'LON', '2010-01-01', NULL, 'A'),
('188888', 'CW-T8FK9X', 'Reggie', 'Mint', 'EMP', 'COCO-UK', 'LON', '2018-01-01', NULL, 'A'),
('896419', 'CW-EZMUNR', 'Tom', 'Tally', 'EMP', 'COCO-UK', 'LON', '2020-07-10', NULL, 'A'),
('457911', 'CW-GMCZHC', 'Sally', 'Counter', 'EMP', 'COCO-UK', 'LON', '2012-05-01', NULL, 'A'),
('296776', 'CW-SNZYHU', 'Jules', 'Keeper', 'EMP', 'COCO-UK', 'LON', '2022-03-01', NULL, 'A'),
('324713', 'CW-VYNNPZ', 'Erin', 'Overview', 'EMP', 'COCO-UK', 'LON', '2019-05-01', NULL, 'A'),
('986419', 'CW-CR43HM', 'Peter', 'Profile', 'EMP', 'COCO-UK', 'LON', '2015-05-01', NULL, 'A'),
('254678', 'CW-JPKHTU', 'Hugo', 'Salle', 'EMP', 'COCO-UK', 'LON', '2013-02-01', NULL, 'A'),
('483942', 'CW-SFRGJQ', 'Stew', 'Faster', 'EMP', 'COCO-UK', 'LON', '2016-03-01', NULL, 'A'),
('921848', 'CW-E82P52', 'Reddy', 'Leftie', 'EMP', 'COCO-UK', 'LON', '2021-01-01', '2021-05-15', 'T'),
('610240', 'CW-B76CPN', 'Helen', 'Barlow', 'EMP', 'COCO-UK', 'WIN', '2014-06-02', NULL, 'A'),
('610231', 'CW-F53CJR', 'Martin', 'Grange', 'EMP', 'COCO-UK', 'WIN', '2017-09-04', NULL, 'A'),
('610244', 'CW-XE6DBG', 'Aisha', 'Rahman', 'EMP', 'COCO-UK', 'WIN', '2025-11-03', NULL, 'A'),
('610263', 'CW-K7H7ZQ', 'Owen', 'Tate', 'EMP', 'COCO-UK', 'WIN', '2026-08-03', NULL, 'A'),
('610252', 'CW-7G8SM2', 'Dave', 'Pearce', 'EMP', 'COCO-UK', 'WIN', '2019-02-11', NULL, 'A'),
('C-70021', 'CW-KDVCEA', 'Sidney', 'Seeker', 'CTR', 'COCO-UK', 'LON', '2026-06-01', NULL, 'A'),
('439222', 'CW-38FTNV', 'Steve', 'Starter', 'EMP', 'COCO-NL', 'AMS', '2010-01-01', NULL, 'A'),
('139870', 'CW-TC93US', 'Faith', 'Broker', 'EMP', 'COCO-NL', 'AMS', '2018-02-01', NULL, 'A'),
('199995', 'CW-7K8YQG', 'Gary', 'Geeke', 'EMP', 'COCO-NL', 'AMS', '2020-05-01', NULL, 'A'),
('338575', 'CW-FM4E2G', 'Polly', 'Tasker', 'EMP', 'COCO-NL', 'AMS', '2022-04-01', NULL, 'A'),
('818928', 'CW-T3HUQE', 'Lemmie', 'Stage', 'EMP', 'COCO-NL', 'AMS', '2019-05-01', NULL, 'A'),
('458109', 'CW-DLMYL9', 'Bob', 'Nitter', 'EMP', 'COCO-NL', 'AMS', '2023-01-09', NULL, 'A'),
('549922', 'CW-K34WSJ', 'Maura', 'Zeller', 'EMP', 'COCO-NL', 'AMS', '2012-01-01', '2026-09-18', 'T'),
('133777', 'CW-U5PPXA', 'Zach', 'Now', 'EMP', 'COCO-US', 'NYC', '2010-01-01', NULL, 'A'),
('144994', 'CW-5V7T2Y', 'Harry', 'Hopeful', 'EMP', 'COCO-US', 'NYC', '2012-05-01', NULL, 'A'),
('549032', 'CW-W9JFK6', 'Margo', 'Deal', 'EMP', 'COCO-US', 'NYC', '2016-01-01', NULL, 'A'),
('302145', 'CW-RMRC8S', 'Tessa', 'Tube', 'EMP', 'COCO-US', 'NYC', '2010-10-10', NULL, 'A'),
('328080', 'CW-X2F75Q', 'Callie', 'Quartile', 'EMP', 'COCO-US', 'NYC', '2012-03-01', NULL, 'A'),
('209482', 'CW-T3WZE8', 'Tanya', 'Tidie', 'EMP', 'COCO-US', 'NYC', '2015-04-01', NULL, 'A'),
('499888', 'CW-3NSATA', 'Ivor', 'Padlock', 'EMP', 'COCO-US', 'NYC', '2019-08-01', NULL, 'A'),
('710118', 'CW-PLYYBU', 'Luis', 'Ortega', 'EMP', 'COCO-US', 'KCY', '2020-04-06', NULL, 'A'),
('810045', 'CW-G32FNJ', 'Chantal', 'Roy', 'EMP', 'COCO-CA', 'EDM', '2015-08-17', NULL, 'A'),
('810052', 'CW-HFD9LG', 'Ben', 'Kowalski', 'EMP', 'COCO-CA', 'EDM', '2018-01-15', NULL, 'A'),
('810067', 'CW-JS5LWU', 'Priya', 'Singh', 'EMP', 'COCO-CA', 'EDM', '2024-05-06', NULL, 'A'),
('810071', 'CW-GBAX2A', 'Tom', 'Whitehorse', 'EMP', 'COCO-CA', 'EDM', '2021-10-04', NULL, 'A')
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.job_assignment (emp_no, eff_date, job_code, cost_center, mgr_emp_no, spend_auth) VALUES
('371803', '2010-01-01', 'EXEC-FDR', '9999', NULL, 250000),
('188888', '2018-01-01', 'EXEC-CFO', '5656', '371803', 250000),
('896419', '2020-07-10', 'FIN-ACM', '6788', '188888', 25000),
('457911', '2012-05-01', 'FIN-PAY', '6877', '896419', 0),
('296776', '2022-03-01', 'EXEC-CDO', '5656', '371803', 0),
('324713', '2019-05-01', 'DAT-ARC', '7432', '296776', 0),
('986419', '2015-05-01', 'DAT-ANL', '7432', '324713', 0),
('254678', '2013-02-01', 'SAL-REP', '7432', '144994', 0),
('483942', '2016-03-01', 'EXEC-MFG', '8400', '371803', 100000),
('921848', '2021-01-01', 'PRC-MGR', '6877', '188888', 0),
('610240', '2014-06-02', 'MFG-QP', '8110', '483942', 5000),
('610231', '2017-09-04', 'MFG-OPR', '8100', '610240', 0),
('610244', '2025-11-03', 'MFG-CTO', '8100', '610240', 0),
('610263', '2026-08-03', 'MFG-CTO', '8100', '610240', 0),
('610252', '2019-02-11', 'DEP-DGS', '8120', '483942', 1000),
('C-70021', '2026-06-01', 'SEC-CON', '7700', '499888', 0),
('439222', '2010-01-01', 'EXEC-FDR', '9999', NULL, 250000),
('139870', '2018-02-01', 'EXEC-HRD', '2373', '439222', 50000),
('199995', '2020-05-01', 'IT-INFRA', '3082', '439222', 0),
('338575', '2022-04-01', 'IT-PM', '2373', '439222', 0),
('818928', '2019-05-01', 'IT-ETL', '3082', '199995', 0),
('458109', '2023-01-09', 'IT-INT', '3082', '199995', 0),
('549922', '2012-01-01', 'SAL-REP', '7432', '144994', 0),
('133777', '2010-01-01', 'EXEC-FDR', '9999', NULL, 250000),
('144994', '2012-05-01', 'SAL-LDR', '2343', '133777', 10000),
('549032', '2016-01-01', 'SAL-REP', '7432', '144994', 0),
('302145', '2010-10-10', 'RES-LEAD', '2343', '133777', 0),
('328080', '2012-03-01', 'DAT-SCI', '4051', '302145', 0),
('209482', '2015-04-01', 'CLN-REC', '4051', '302145', 0),
('499888', '2019-08-01', 'EXEC-CISO', '7700', '133777', 50000),
('710118', '2020-04-06', 'DEP-DGS', '8300', '483942', 1000),
('810045', '2015-08-17', 'MFG-QP', '8210', '483942', 5000),
('810052', '2018-01-15', 'MFG-OPR', '8200', '810045', 0),
('810067', '2024-05-06', 'MFG-OPR', '8200', '810045', 0),
('810067', '2026-07-01', 'MFG-SUP', '8200', '810045', 2500),
('810071', '2021-10-04', 'DEP-DGS', '8220', '483942', 1000)
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.competency (comp_cd, comp_name, comp_desc, refresh_mths, regulated_yn) VALUES
('GMP-BAS', 'GMP fundamentals', 'Good manufacturing practice principles, documentation and data integrity basics.', 12, 'Y'),
('GMP-ASEP', 'Aseptic technique and gowning', 'Aseptic processing, grade A/B gowning qualification and media fill participation.', 6, 'Y'),
('BIO-CU', 'GMO contained use', 'Handling genetically modified organisms and viral vectors under contained use class 2.', 12, 'Y'),
('OEB-HP', 'High potency compound handling', 'Working in OEB3 and OEB4 areas, containment equipment and decontamination.', 12, 'Y'),
('EBR-SIG', 'Electronic records and signatures', 'Signing electronic batch records under 21 CFR Part 11 and EU GMP Annex 11.', 24, 'Y'),
('QP-CPD', 'Qualified Person continuing development', 'Annual continuing professional development required to act as Qualified Person.', 12, 'Y'),
('DG-AIR', 'Dangerous goods by air (IATA DGR)', 'Preparing and signing shipper''s declarations for air transport.', 24, 'Y'),
('DG-ROAD', 'Dangerous goods by road (ADR/TDG/DOT)', 'Preparing and signing road transport documents under the national regime.', 36, 'Y'),
('GCP-REC', 'GCP clinical records', 'Good clinical practice for trial records, transcription and source data.', 24, 'Y'),
('DP-HLTH', 'Health data protection', 'Handling pseudonymised patient data; chain of identity; logging re-identification requests.', 12, 'N')
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.job_competency (job_code, comp_cd, eff_date) VALUES
('MFG-OPR', 'GMP-BAS', '2018-01-01'),
('MFG-OPR', 'OEB-HP', '2023-03-01'),
('MFG-OPR', 'EBR-SIG', '2019-06-01'),
('MFG-SUP', 'GMP-BAS', '2018-01-01'),
('MFG-SUP', 'OEB-HP', '2023-03-01'),
('MFG-SUP', 'EBR-SIG', '2019-06-01'),
('MFG-CTO', 'GMP-BAS', '2025-09-01'),
('MFG-CTO', 'GMP-ASEP', '2025-09-01'),
('MFG-CTO', 'BIO-CU', '2025-09-01'),
('MFG-CTO', 'EBR-SIG', '2025-09-01'),
('MFG-CTO', 'DP-HLTH', '2026-04-01'),
('MFG-QP', 'GMP-BAS', '2018-01-01'),
('MFG-QP', 'QP-CPD', '2018-01-01'),
('MFG-QP', 'EBR-SIG', '2019-06-01'),
('DEP-DGS', 'DG-AIR', '2019-01-01'),
('DEP-DGS', 'DG-ROAD', '2019-01-01'),
('CLN-REC', 'GCP-REC', '2016-01-01'),
('CLN-REC', 'DP-HLTH', '2026-04-01')
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.emp_competency (emp_no, comp_cd, achieved_dt, expiry_dt, training_ref, cert_no) VALUES
('610231', 'GMP-BAS', '2026-02-10', '2027-02-10', 'TRN-26-0107', NULL),
('610231', 'OEB-HP', '2025-10-14', '2026-10-14', 'TRN-25-0833', NULL),
('610231', 'EBR-SIG', '2025-01-20', '2027-01-20', 'TRN-25-0061', NULL),
('610244', 'GMP-BAS', '2025-11-05', '2026-11-05', 'TRN-25-0911', NULL),
('610244', 'GMP-ASEP', '2026-05-12', '2026-11-12', 'TRN-26-0388', 'MF-WIN-26-014'),
('610244', 'BIO-CU', '2025-11-12', '2026-11-12', 'TRN-25-0925', NULL),
('610244', 'EBR-SIG', '2025-11-06', '2027-11-06', 'TRN-25-0912', NULL),
('610244', 'DP-HLTH', '2026-04-20', '2027-04-20', 'TRN-26-0301', NULL),
('610263', 'GMP-BAS', '2026-08-05', '2027-08-05', 'TRN-26-0602', NULL),
('610263', 'GMP-ASEP', '2026-08-21', '2027-02-21', 'TRN-26-0641', 'MF-WIN-26-022'),
('610263', 'BIO-CU', '2026-08-12', '2027-08-12', 'TRN-26-0617', NULL),
('610263', 'EBR-SIG', '2026-08-06', '2028-08-06', 'TRN-26-0605', NULL),
('610240', 'GMP-BAS', '2026-01-15', '2027-01-15', 'TRN-26-0022', NULL),
('610240', 'QP-CPD', '2026-03-31', '2027-03-31', 'TRN-26-0240', 'RSC-QP-11872'),
('610240', 'EBR-SIG', '2025-02-03', '2027-02-03', 'TRN-25-0090', NULL),
('610252', 'DG-AIR', '2025-03-18', '2027-03-18', 'TRN-25-0212', 'IATA-DGR-UK-44871'),
('610252', 'DG-ROAD', '2024-06-04', '2027-06-04', 'TRN-24-0420', 'DGSA-UK-20931'),
('810052', 'GMP-BAS', '2025-10-20', '2026-10-20', 'TRN-25-0851', NULL),
('810052', 'OEB-HP', '2025-09-15', '2026-09-15', 'TRN-25-0770', NULL),
('810052', 'EBR-SIG', '2025-04-02', '2027-04-02', 'TRN-25-0266', NULL),
('810067', 'GMP-BAS', '2026-05-08', '2027-05-08', 'TRN-26-0355', NULL),
('810067', 'OEB-HP', '2026-05-09', '2027-05-09', 'TRN-26-0356', NULL),
('810067', 'EBR-SIG', '2024-05-10', '2026-05-10', 'TRN-24-0371', NULL),
('810045', 'GMP-BAS', '2026-01-12', '2027-01-12', 'TRN-26-0015', NULL),
('810045', 'QP-CPD', '2025-06-30', '2026-06-30', 'TRN-25-0514', 'CA-QP-2291'),
('810045', 'EBR-SIG', '2025-03-03', '2027-03-03', 'TRN-25-0150', NULL),
('810071', 'DG-ROAD', '2024-10-03', '2027-10-03', 'TRN-24-0802', 'TDG-AB-77120'),
('710118', 'DG-ROAD', '2025-04-18', '2028-04-18', 'TRN-25-0305', 'DOT-HM-KC-0418'),
('710118', 'DG-AIR', '2025-04-25', '2027-04-25', 'TRN-25-0311', 'IATA-DGR-US-30812'),
('209482', 'GCP-REC', '2025-02-11', '2027-02-11', 'TRN-25-0101', NULL),
('209482', 'DP-HLTH', '2026-04-22', '2027-04-22', 'TRN-26-0305', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.hr_event (event_id, emp_no, event_type, eff_date, raised_at, new_job_code, event_text) VALUES
('HRE-2012-0014', '457911', 'HIR', '2012-05-01', '2012-04-20 09:00+00', 'FIN-PAY', 'Joined as Payments Clerk, Finance Operations London'),
('HRE-2012-0021', '549922', 'HIR', '2012-01-01', '2011-12-12 09:00+00', 'SAL-REP', 'Joined as Sales Representative, Amsterdam'),
('HRE-2013-0006', '254678', 'HIR', '2013-02-01', '2013-01-21 09:00+00', 'SAL-REP', 'Joined as Sales Representative, London'),
('HRE-2014-0019', '610240', 'HIR', '2014-06-02', '2014-05-12 09:00+00', 'MFG-QP', 'Joined as Qualified Person, Winchester'),
('HRE-2015-0012', '209482', 'HIR', '2015-04-01', '2015-03-16 09:00+00', 'CLN-REC', 'Joined as Clinical Records Clerk, New York'),
('HRE-2015-0031', '810045', 'HIR', '2015-08-17', '2015-07-27 09:00+00', 'MFG-QP', 'Joined as Qualified Person, Edmonton'),
('HRE-2017-0027', '610231', 'HIR', '2017-09-04', '2017-08-14 09:00+00', 'MFG-OPR', 'Joined as Manufacturing Operator, Winchester'),
('HRE-2018-0003', '188888', 'HIR', '2018-01-01', '2017-12-04 09:00+00', 'EXEC-CFO', 'Joined as Chief Finance Officer'),
('HRE-2018-0004', '810052', 'HIR', '2018-01-15', '2018-01-02 09:00+00', 'MFG-OPR', 'Joined as Manufacturing Operator, Edmonton'),
('HRE-2018-0008', '139870', 'HIR', '2018-02-01', '2018-01-15 09:00+00', 'EXEC-HRD', 'Joined as HR Director and Chief Privacy Officer'),
('HRE-2019-0015', '324713', 'HIR', '2019-05-01', '2019-04-15 09:00+00', 'DAT-ARC', 'Joined as Information Architect, Data Office'),
('HRE-2020-0011', '199995', 'HIR', '2020-05-01', '2020-04-14 09:00+00', 'IT-INFRA', 'Joined as IT Infrastructure Lead'),
('HRE-2020-0016', '896419', 'HIR', '2020-07-10', '2020-06-26 09:00+00', 'FIN-ACM', 'Joined as Accounts Manager, Finance HQ'),
('HRE-2021-0001', '921848', 'HIR', '2021-01-01', '2020-12-10 09:00+00', 'PRC-MGR', 'Joined as Procurement Manager'),
('HRE-2021-0013', '921848', 'TER', '2021-05-15', '2021-05-14 16:30+00', NULL, 'Left: dismissed following procurement investigation'),
('HRE-2024-0009', '810067', 'HIR', '2024-05-06', '2024-04-15 09:00+00', 'MFG-OPR', 'Joined as Manufacturing Operator, Edmonton'),
('HRE-2025-0044', '610244', 'HIR', '2025-11-03', '2025-10-13 09:00+00', 'MFG-CTO', 'Joined as Cell Therapy Operator, Winchester'),
('HRE-2026-0022', 'C-70021', 'HIR', '2026-06-01', '2026-05-26 10:00+00', 'SEC-CON', 'Contractor engaged as Security Consultant (fraud investigation support)'),
('HRE-2026-0029', '810067', 'XFR', '2026-07-01', '2026-06-17 13:20+00', 'MFG-SUP', 'Promoted to Manufacturing Supervisor, Edmonton'),
('HRE-2026-0034', '610263', 'HIR', '2026-08-03', '2026-07-14 08:45+00', 'MFG-CTO', 'Joined as Cell Therapy Operator, Winchester'),
('HRE-2026-0041', '549922', 'TER', '2026-09-18', '2026-09-04 15:10+00', NULL, 'Resigned; last working day 18 September 2026')
ON CONFLICT DO NOTHING;

INSERT INTO coco_hrim.hr_event_dist (event_id, target_sys, sent_at, ack_yn, ack_at) VALUES
('HRE-2025-0044', 'sec-admin', '2025-10-13 09:05+00', 'Y', '2025-10-30 14:10+00'),
('HRE-2025-0044', 'cocopages', '2025-10-13 09:05+00', 'Y', '2025-11-03 06:00+00'),
('HRE-2025-0044', 'UK payroll', '2025-10-13 09:05+00', 'Y', '2025-10-20 11:00+00'),
('HRE-2026-0022', 'sec-admin', '2026-05-26 10:05+00', 'Y', '2026-05-29 15:30+00'),
('HRE-2026-0022', 'cocopages', '2026-05-26 10:05+00', 'Y', '2026-06-01 06:00+00'),
('HRE-2026-0029', 'sec-admin', '2026-06-17 13:25+00', 'Y', '2026-06-30 16:00+00'),
('HRE-2026-0029', 'cocopages', '2026-06-17 13:25+00', 'Y', '2026-07-01 06:00+00'),
('HRE-2026-0029', 'CA payroll', '2026-06-17 13:25+00', 'Y', '2026-06-19 10:00+00'),
('HRE-2026-0034', 'sec-admin', '2026-07-14 08:50+00', 'Y', '2026-08-03 12:40+00'),
('HRE-2026-0034', 'cocopages', '2026-07-14 08:50+00', 'Y', '2026-08-03 06:00+00'),
('HRE-2026-0034', 'UK payroll', '2026-07-14 08:50+00', 'Y', '2026-07-20 09:30+00'),
('HRE-2026-0034', 'coco-expenses', '2026-07-14 08:50+00', 'N', NULL),
('HRE-2026-0041', 'sec-admin', '2026-09-04 15:15+00', 'N', NULL),
('HRE-2026-0041', 'cocopages', '2026-09-04 15:15+00', 'N', NULL),
('HRE-2026-0041', 'NL payroll', '2026-09-04 15:15+00', 'Y', '2026-09-08 10:20+00'),
('HRE-2026-0041', 'coco-expenses', '2026-09-04 15:15+00', 'N', NULL)
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS coco_hrim.lms_completion (
  completion_ref varchar(40) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  course_cd varchar(40) NOT NULL,
  comp_cd varchar(40) NOT NULL,
  completed_dt date NOT NULL,
  expiry_dt date,
  assess_dt date,
  assess_score numeric(6,2),
  pass_mark numeric(6,2),
  passed_yn char(1),
  CONSTRAINT lms_completion_pk PRIMARY KEY (completion_ref)
);
COMMENT ON TABLE coco_hrim.lms_completion IS 'Training completions and assessment results received from the learning system (Training Completions), waiting for the skills administrator to record the competency in emp_competency.';

CREATE TABLE IF NOT EXISTS coco_hrim.dsr_action (
  action_ref varchar(40) NOT NULL,
  request_ref varchar(40) NOT NULL,
  subject_ref varchar(40),
  request_typ varchar(20),
  action_typ varchar(20) NOT NULL,
  requested_at timestamptz NOT NULL,
  completed_at timestamptz,
  action_sts varchar(20) NOT NULL,
  retention_ref varchar(40),
  CONSTRAINT dsr_action_pk PRIMARY KEY (action_ref)
);
COMMENT ON TABLE coco_hrim.dsr_action IS 'Data subject rights actions HRIM must carry out (Rights Fulfilment Actions): locate, export, rectify or erase a worker''s data, with any retention obligation that blocks erasure.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA coco_hrim TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA coco_hrim TO egeria_user, airflow_user;
