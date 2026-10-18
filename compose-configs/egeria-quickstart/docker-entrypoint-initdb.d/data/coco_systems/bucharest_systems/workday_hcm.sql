-- system-qualified-name: SoftwareServer::SYS-013::Workday HCM
-- Workday HCM - Bucharest.  Workday HCM for EKG Pharmaceuticals S.R.L. (company RO01): workers and contingent workers,
-- positions, job profiles, business process events with their outbound integrations (Microsoft 365 via Graph and
-- Kronos), and the Romanian monthly pay runs.  Its tables feed Worker Master Data, Worker Lifecycle Events and Payroll
-- Results (runs, and results of salaried staff).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS workday_hcm;
COMMENT ON SCHEMA workday_hcm IS 'Workday HCM (EKG): report-as-a-service extracts landed as tables (Workday field names in snake case).';

CREATE TABLE IF NOT EXISTS workday_hcm.job_profile (
  job_profile_id              varchar(40) NOT NULL,
  job_profile_name            varchar(120) NOT NULL,
  job_family                  varchar(60),
  work_hazards                text,
  approval_authority_amount   numeric(18,2),
  approval_authority_currency varchar(3),
  inactive                    boolean NOT NULL,
  CONSTRAINT job_profile_pk PRIMARY KEY (job_profile_id)
);
COMMENT ON TABLE workday_hcm.job_profile IS 'Job profiles (Romanian names) with hazards and approval authority.';

INSERT INTO workday_hcm.job_profile (job_profile_id, job_profile_name, job_family, work_hazards, approval_authority_amount, approval_authority_currency, inactive) VALUES
('JP-RO-DG', 'Director General', 'Conducere', NULL, 500000, 'RON', FALSE),
('JP-RO-DFIN', 'Director Financiar', 'Financiar', NULL, 250000, 'RON', FALSE),
('JP-RO-QP', 'Director Calitate și Persoană Calificată', 'Calitate', NULL, 100000, 'RON', FALSE),
('JP-RO-DPROD', 'Director Producție', 'Producție', 'Zone sterile clasa A/B; abur sub presiune', 100000, 'RON', FALSE),
('JP-RO-REG', 'Manager Afaceri de Reglementare și Juridic', 'Reglementare', NULL, 50000, 'RON', FALSE),
('JP-RO-SALES', 'Manager Vânzări', 'Vânzări', NULL, 30000, 'RON', FALSE),
('JP-RO-HR', 'Director Resurse Umane', 'Resurse umane', NULL, 50000, 'RON', FALSE),
('JP-RO-ITM', 'Manager IT', 'IT', NULL, 50000, 'RON', FALSE),
('JP-RO-ITINF', 'Inginer Infrastructură IT', 'IT', NULL, NULL, NULL, FALSE),
('JP-RO-CONT', 'Contabil Șef', 'Financiar', NULL, 50000, 'RON', FALSE),
('JP-RO-CTRL', 'Controller Financiar', 'Financiar', NULL, 20000, 'RON', FALSE),
('JP-RO-ENG', 'Manager Mentenanță și Utilități', 'Inginerie', 'Lucru la înălțime; izolare electrică; abur', 40000, 'RON', FALSE),
('JP-RO-SCM', 'Manager Lanț de Aprovizionare', 'Logistică', 'Stivuitor; cameră frigorifică', 40000, 'RON', FALSE),
('JP-RO-SEC', 'Specialist Securitate IT', 'IT', NULL, NULL, NULL, FALSE),
('JP-RO-MKT', 'Specialist Marketing', 'Vânzări', NULL, 5000, 'RON', FALSE),
('JP-RO-QCA', 'Analist Control Calitate', 'Calitate', 'Solvenți de laborator (acetonitril, metanol)', NULL, NULL, FALSE),
('JP-RO-QCM', 'Analist Microbiologie', 'Calitate', 'Agenți biologici grupa 2; autoclavă', NULL, NULL, FALSE),
('JP-RO-OP', 'Operator Producție Sterile', 'Producție', 'Zone sterile clasa A/B; abur sub presiune; zgomot', NULL, NULL, FALSE),
('JP-RO-SERUM', 'Specialist Laborator Ser Autolog', 'Producție', 'Material biologic uman; gheață carbonică', NULL, NULL, FALSE),
('JP-RO-SUP', 'Șef de Tură Producție', 'Producție', 'Zone sterile clasa A/B; abur sub presiune; zgomot', 10000, 'RON', FALSE),
('JP-RO-QAS', 'Specialist Asigurarea Calității', 'Calitate', NULL, NULL, NULL, FALSE),
('JP-RO-DG-WH', 'Operator Depozit și Expediții ADR', 'Logistică', 'Gheață carbonică (UN1845); stivuitor; cameră frigorifică', NULL, NULL, FALSE),
('JP-RO-AP', 'Contabil Furnizori', 'Financiar', NULL, NULL, NULL, FALSE),
('JP-RO-MTECH', 'Tehnician Mentenanță și Metrologie', 'Inginerie', 'Izolare electrică; abur sub presiune', 5000, 'RON', FALSE),
('JP-RO-PV', 'Responsabil Farmacovigilență', 'Reglementare', NULL, NULL, NULL, FALSE),
('JP-RO-VAL', 'Consultant Validare', 'Inginerie', 'Acces în zone sterile', NULL, NULL, FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.worker (
  employee_id           varchar(20) NOT NULL,
  worker_type           varchar(30) NOT NULL,
  legal_name_first_name varchar(80) NOT NULL,
  legal_name_last_name  varchar(80) NOT NULL,
  company_id            varchar(10) NOT NULL,
  location_id           varchar(30) NOT NULL,
  hire_date             date NOT NULL,
  termination_date      date,
  active                boolean NOT NULL,
  on_leave              boolean NOT NULL,
  pay_rate_type         varchar(20),
  work_email            varchar(120),
  last_updated          timestamptz NOT NULL,
  CONSTRAINT worker_pk PRIMARY KEY (employee_id)
);
COMMENT ON TABLE workday_hcm.worker IS 'Workers (employee ID = the identifier SAP, Kronos, AD, MES and Concur carry).';

INSERT INTO workday_hcm.worker (employee_id, worker_type, legal_name_first_name, legal_name_last_name, company_id, location_id, hire_date, termination_date, active, on_leave, pay_rate_type, work_email, last_updated) VALUES
('20011', 'Employee', 'Andrei', 'Munteanu', 'RO01', 'LOC-RO-BUC-FABRICA', '2012-02-01', NULL, TRUE, FALSE, 'Salary', 'andrei.munteanu@ekgpharma.ro', '2012-02-01 18:00:00+00'),
('20014', 'Employee', 'Gheorghe', 'Radu', 'RO01', 'LOC-RO-BUC-FABRICA', '2013-05-06', NULL, TRUE, FALSE, 'Salary', 'gheorghe.radu@ekgpharma.ro', '2013-05-06 18:00:00+00'),
('20017', 'Employee', 'Nicoleta', 'Oprea', 'RO01', 'LOC-RO-BUC-FABRICA', '2014-09-01', NULL, TRUE, FALSE, 'Salary', 'nicoleta.oprea@ekgpharma.ro', '2014-09-01 18:00:00+00'),
('20021', 'Employee', 'Florin', 'Stoica', 'RO01', 'LOC-RO-BUC-FABRICA', '2015-03-02', NULL, TRUE, FALSE, 'Salary', 'florin.stoica@ekgpharma.ro', '2015-03-02 18:00:00+00'),
('20023', 'Employee', 'Adina', 'Petre', 'RO01', 'LOC-RO-BUC-FABRICA', '2016-01-11', NULL, TRUE, FALSE, 'Salary', 'adina.petre@ekgpharma.ro', '2016-01-11 18:00:00+00'),
('20026', 'Employee', 'Cristian', 'Lungu', 'RO01', 'LOC-RO-BUC-FABRICA', '2016-10-03', NULL, TRUE, FALSE, 'Salary', 'cristian.lungu@ekgpharma.ro', '2016-10-03 18:00:00+00'),
('20029', 'Employee', 'Luminița', 'Chiriac', 'RO01', 'LOC-RO-BUC-FABRICA', '2017-04-18', NULL, TRUE, FALSE, 'Salary', 'luminita.chiriac@ekgpharma.ro', '2017-04-18 18:00:00+00'),
('20031', 'Employee', 'Mihai', 'Constantin', 'RO01', 'LOC-RO-BUC-FABRICA', '2017-08-01', NULL, TRUE, FALSE, 'Salary', 'mihai.constantin@ekgpharma.ro', '2017-08-01 18:00:00+00'),
('20033', 'Employee', 'Lucian', 'Preda', 'RO01', 'LOC-RO-BUC-FABRICA', '2018-02-12', NULL, TRUE, FALSE, 'Salary', 'lucian.preda@ekgpharma.ro', '2018-02-12 18:00:00+00'),
('20035', 'Employee', 'Mihaela', 'Apostol', 'RO01', 'LOC-RO-BUC-FABRICA', '2018-06-04', NULL, TRUE, FALSE, 'Salary', 'mihaela.apostol@ekgpharma.ro', '2018-06-04 18:00:00+00'),
('20038', 'Employee', 'Simona', 'Florescu', 'RO01', 'LOC-RO-BUC-FABRICA', '2019-01-14', NULL, TRUE, FALSE, 'Salary', 'simona.florescu@ekgpharma.ro', '2019-01-14 18:00:00+00'),
('20040', 'Employee', 'Marian', 'Bucur', 'RO01', 'LOC-RO-BUC-FABRICA', '2015-11-02', NULL, TRUE, FALSE, 'Salary', 'marian.bucur@ekgpharma.ro', '2015-11-02 18:00:00+00'),
('20042', 'Employee', 'Ciprian', 'Tudor', 'RO01', 'LOC-RO-BUC-FABRICA', '2016-05-16', NULL, TRUE, FALSE, 'Salary', 'ciprian.tudor@ekgpharma.ro', '2016-05-16 18:00:00+00'),
('20044', 'Employee', 'Sorin', 'Matei', 'RO01', 'LOC-RO-BUC-FABRICA', '2020-03-02', NULL, TRUE, FALSE, 'Salary', 'sorin.matei@ekgpharma.ro', '2020-03-02 18:00:00+00'),
('20046', 'Employee', 'Roxana', 'Dumitrescu', 'RO01', 'LOC-RO-BUC-FABRICA', '2021-06-07', NULL, TRUE, TRUE, 'Salary', 'roxana.dumitrescu@ekgpharma.ro', '2021-06-07 18:00:00+00'),
('20049', 'Employee', 'Sebastian', 'Vasile', 'RO01', 'LOC-RO-BUC-FABRICA', '2019-09-02', '2026-07-31', FALSE, FALSE, 'Salary', 'sebastian.vasile@ekgpharma.ro', '2026-07-31 18:00:00+00'),
('20052', 'Employee', 'Elena', 'Popescu', 'RO01', 'LOC-RO-BUC-FABRICA', '2018-10-15', NULL, TRUE, FALSE, 'Salary', 'elena.popescu@ekgpharma.ro', '2018-10-15 18:00:00+00'),
('20055', 'Employee', 'Ioana', 'Stan', 'RO01', 'LOC-RO-BUC-FABRICA', '2020-02-17', NULL, TRUE, FALSE, 'Salary', 'ioana.stan@ekgpharma.ro', '2020-02-17 18:00:00+00'),
('20058', 'Employee', 'Bogdan', 'Ionescu', 'RO01', 'LOC-RO-BUC-FABRICA', '2019-04-01', NULL, TRUE, FALSE, 'Hourly', NULL, '2019-04-01 18:00:00+00'),
('20061', 'Employee', 'Alexandru', 'Dinu', 'RO01', 'LOC-RO-BUC-FABRICA', '2020-07-06', NULL, TRUE, FALSE, 'Hourly', NULL, '2020-07-06 18:00:00+00'),
('20063', 'Employee', 'Cătălina', 'Marin', 'RO01', 'LOC-RO-BUC-FABRICA', '2022-01-10', NULL, TRUE, FALSE, 'Hourly', NULL, '2022-01-10 18:00:00+00'),
('20066', 'Employee', 'Vlad', 'Georgescu', 'RO01', 'LOC-RO-BUC-FABRICA', '2016-09-05', NULL, TRUE, FALSE, 'Hourly', 'vlad.georgescu@ekgpharma.ro', '2016-09-05 18:00:00+00'),
('20069', 'Employee', 'Raluca', 'Enache', 'RO01', 'LOC-RO-BUC-FABRICA', '2019-05-13', NULL, TRUE, FALSE, 'Salary', 'raluca.enache@ekgpharma.ro', '2019-05-13 18:00:00+00'),
('20072', 'Employee', 'Dan', 'Ilie', 'RO01', 'LOC-RO-BUC-FABRICA', '2018-03-19', NULL, TRUE, FALSE, 'Hourly', NULL, '2018-03-19 18:00:00+00'),
('20075', 'Employee', 'Oana', 'Nistor', 'RO01', 'LOC-RO-BUC-FABRICA', '2021-02-01', NULL, TRUE, FALSE, 'Salary', 'oana.nistor@ekgpharma.ro', '2021-02-01 18:00:00+00'),
('20078', 'Employee', 'Radu', 'Stoian', 'RO01', 'LOC-RO-BUC-FABRICA', '2017-11-20', NULL, TRUE, FALSE, 'Hourly', NULL, '2017-11-20 18:00:00+00'),
('20081', 'Employee', 'Gabriela', 'Toma', 'RO01', 'LOC-RO-BUC-FABRICA', '2022-09-12', NULL, TRUE, FALSE, 'Salary', 'gabriela.toma@ekgpharma.ro', '2022-09-12 18:00:00+00'),
('20084', 'Employee', 'Irina', 'Moldovan', 'RO01', 'LOC-RO-BUC-FABRICA', '2026-09-01', NULL, TRUE, FALSE, 'Salary', 'irina.moldovan@ekgpharma.ro', '2026-09-01 18:00:00+00'),
('20086', 'Employee', 'Ștefan', 'Pavel', 'RO01', 'LOC-RO-BUC-FABRICA', '2023-03-06', NULL, TRUE, FALSE, 'Hourly', NULL, '2023-03-06 18:00:00+00'),
('C0012', 'Contingent Worker', 'Paul', 'Neagu', 'RO01', 'LOC-RO-BUC-FABRICA', '2026-06-15', NULL, TRUE, FALSE, NULL, 'paul.neagu.ext@ekgpharma.ro', '2026-06-15 18:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.worker_position (
  position_id         varchar(20) NOT NULL,
  effective_date      date NOT NULL,
  employee_id         varchar(20) NOT NULL,
  job_profile_id      varchar(40) NOT NULL,
  business_title      varchar(120),
  cost_center_id      varchar(20) NOT NULL,
  manager_employee_id varchar(20),
  end_date            date,
  primary_job         boolean NOT NULL,
  CONSTRAINT worker_position_pk PRIMARY KEY (position_id, effective_date)
);
COMMENT ON TABLE workday_hcm.worker_position IS 'Position assignment history (effective dated).';

INSERT INTO workday_hcm.worker_position (position_id, effective_date, employee_id, job_profile_id, business_title, cost_center_id, manager_employee_id, end_date, primary_job) VALUES
('P-RO-0001', '2012-02-01', '20011', 'JP-RO-DG', 'Director General', 'RO10-100', NULL, NULL, TRUE),
('P-RO-0002', '2013-05-06', '20014', 'JP-RO-DFIN', 'Director Financiar', 'RO10-210', '20011', NULL, TRUE),
('P-RO-0003', '2014-09-01', '20017', 'JP-RO-QP', 'Director Calitate și Persoană Calificată', 'RO10-120', '20011', NULL, TRUE),
('P-RO-0004', '2015-03-02', '20021', 'JP-RO-DPROD', 'Director Producție', 'RO10-110', '20011', NULL, TRUE),
('P-RO-0005', '2016-01-11', '20023', 'JP-RO-REG', 'Manager Afaceri de Reglementare și Juridic', 'RO10-160', '20011', NULL, TRUE),
('P-RO-0006', '2016-10-03', '20026', 'JP-RO-SALES', 'Manager Vânzări', 'RO10-170', '20011', NULL, TRUE),
('P-RO-0007', '2017-04-18', '20029', 'JP-RO-HR', 'Director Resurse Umane', 'RO10-220', '20011', NULL, TRUE),
('P-RO-0008', '2017-08-01', '20031', 'JP-RO-ITM', 'Manager IT', 'RO10-230', '20014', NULL, TRUE),
('P-RO-0009', '2018-02-12', '20033', 'JP-RO-ITINF', 'Inginer Infrastructură IT', 'RO10-230', '20031', NULL, TRUE),
('P-RO-0010', '2018-06-04', '20035', 'JP-RO-CONT', 'Contabil Șef', 'RO10-210', '20014', NULL, TRUE),
('P-RO-0011', '2019-01-14', '20038', 'JP-RO-CTRL', 'Controller Financiar', 'RO10-210', '20014', NULL, TRUE),
('P-RO-0012', '2015-11-02', '20040', 'JP-RO-ENG', 'Manager Mentenanță și Utilități', 'RO10-150', '20021', NULL, TRUE),
('P-RO-0013', '2016-05-16', '20042', 'JP-RO-SCM', 'Manager Lanț de Aprovizionare', 'RO10-140', '20014', NULL, TRUE),
('P-RO-0014', '2020-03-02', '20044', 'JP-RO-SEC', 'Specialist Securitate IT', 'RO10-230', '20031', NULL, TRUE),
('P-RO-0015', '2021-06-07', '20046', 'JP-RO-MKT', 'Specialist Marketing', 'RO10-170', '20026', NULL, TRUE),
('P-RO-0016', '2019-09-02', '20049', 'JP-RO-QCA', 'Analist Control Calitate', 'RO10-130', '20017', '2026-07-31', TRUE),
('P-RO-0017', '2018-10-15', '20052', 'JP-RO-QCA', 'Analist Control Calitate', 'RO10-130', '20017', NULL, TRUE),
('P-RO-0018', '2020-02-17', '20055', 'JP-RO-QCM', 'Analist Microbiologie', 'RO10-130', '20017', NULL, TRUE),
('P-RO-0019', '2019-04-01', '20058', 'JP-RO-OP', 'Operator Producție Sterile', 'RO10-110', '20066', NULL, TRUE),
('P-RO-0020', '2020-07-06', '20061', 'JP-RO-OP', 'Operator Producție Sterile', 'RO10-110', '20066', '2026-07-31', TRUE),
('P-RO-0020', '2026-08-01', '20061', 'JP-RO-SERUM', 'Specialist Laborator Ser Autolog', 'RO10-115', '20021', NULL, TRUE),
('P-RO-0021', '2022-01-10', '20063', 'JP-RO-SERUM', 'Specialist Laborator Ser Autolog', 'RO10-115', '20021', NULL, TRUE),
('P-RO-0022', '2016-09-05', '20066', 'JP-RO-SUP', 'Șef de Tură Producție', 'RO10-110', '20021', NULL, TRUE),
('P-RO-0023', '2019-05-13', '20069', 'JP-RO-QAS', 'Specialist Asigurarea Calității', 'RO10-120', '20017', NULL, TRUE),
('P-RO-0024', '2018-03-19', '20072', 'JP-RO-DG-WH', 'Operator Depozit și Expediții ADR', 'RO10-140', '20042', NULL, TRUE),
('P-RO-0025', '2021-02-01', '20075', 'JP-RO-AP', 'Contabil Furnizori', 'RO10-210', '20035', NULL, TRUE),
('P-RO-0026', '2017-11-20', '20078', 'JP-RO-MTECH', 'Tehnician Mentenanță și Metrologie', 'RO10-150', '20040', NULL, TRUE),
('P-RO-0027', '2022-09-12', '20081', 'JP-RO-PV', 'Responsabil Farmacovigilență', 'RO10-160', '20023', NULL, TRUE),
('P-RO-0028', '2026-09-01', '20084', 'JP-RO-QCA', 'Analist Control Calitate', 'RO10-130', '20017', NULL, TRUE),
('P-RO-0029', '2023-03-06', '20086', 'JP-RO-OP', 'Operator Producție Sterile', 'RO10-110', '20066', NULL, TRUE),
('P-RO-0030', '2026-06-15', 'C0012', 'JP-RO-VAL', 'Consultant Validare', 'RO10-150', '20040', NULL, TRUE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.business_process_event (
  event_id                varchar(30) NOT NULL,
  business_process_type   varchar(60) NOT NULL,
  employee_id             varchar(20) NOT NULL,
  effective_date          date NOT NULL,
  initiated_moment        timestamptz NOT NULL,
  proposed_job_profile_id varchar(40),
  status                  varchar(30) NOT NULL,
  comment                 text,
  CONSTRAINT business_process_event_pk PRIMARY KEY (event_id)
);
COMMENT ON TABLE workday_hcm.business_process_event IS 'Staffing business process events (hires before the 2024 Workday go-live were migrated with their original dates).';

INSERT INTO workday_hcm.business_process_event (event_id, business_process_type, employee_id, effective_date, initiated_moment, proposed_job_profile_id, status, comment) VALUES
('EVT-RO-2012-0001', 'Hire', '20011', '2012-02-01', '2012-01-18 09:00:00+00', 'JP-RO-DG', 'Successfully Completed', 'Angajare: Director General, Conducere'),
('EVT-RO-2013-0002', 'Hire', '20014', '2013-05-06', '2013-04-22 09:00:00+00', 'JP-RO-DFIN', 'Successfully Completed', 'Angajare: Director Financiar, Financiar-contabilitate'),
('EVT-RO-2014-0003', 'Hire', '20017', '2014-09-01', '2014-08-18 09:00:00+00', 'JP-RO-QP', 'Successfully Completed', 'Angajare: Director Calitate și Persoană Calificată, Asigurarea calității'),
('EVT-RO-2015-0004', 'Hire', '20021', '2015-03-02', '2015-02-16 09:00:00+00', 'JP-RO-DPROD', 'Successfully Completed', 'Angajare: Director Producție, Producție sterile'),
('EVT-RO-2015-0005', 'Hire', '20040', '2015-11-02', '2015-10-19 09:00:00+00', 'JP-RO-ENG', 'Successfully Completed', 'Angajare: Manager Mentenanță și Utilități, Mentenanță și inginerie'),
('EVT-RO-2016-0006', 'Hire', '20023', '2016-01-11', '2015-12-28 09:00:00+00', 'JP-RO-REG', 'Successfully Completed', 'Angajare: Manager Afaceri de Reglementare și Juridic, Afaceri de reglementare'),
('EVT-RO-2016-0007', 'Hire', '20042', '2016-05-16', '2016-05-02 09:00:00+00', 'JP-RO-SCM', 'Successfully Completed', 'Angajare: Manager Lanț de Aprovizionare, Depozit și logistică'),
('EVT-RO-2016-0008', 'Hire', '20066', '2016-09-05', '2016-08-22 09:00:00+00', 'JP-RO-SUP', 'Successfully Completed', 'Angajare: Șef de Tură Producție, Producție sterile'),
('EVT-RO-2016-0009', 'Hire', '20026', '2016-10-03', '2016-09-19 09:00:00+00', 'JP-RO-SALES', 'Successfully Completed', 'Angajare: Manager Vânzări, Vânzări și marketing'),
('EVT-RO-2017-0010', 'Hire', '20029', '2017-04-18', '2017-04-04 09:00:00+00', 'JP-RO-HR', 'Successfully Completed', 'Angajare: Director Resurse Umane, Resurse umane'),
('EVT-RO-2017-0011', 'Hire', '20031', '2017-08-01', '2017-07-18 09:00:00+00', 'JP-RO-ITM', 'Successfully Completed', 'Angajare: Manager IT, IT'),
('EVT-RO-2017-0012', 'Hire', '20078', '2017-11-20', '2017-11-06 09:00:00+00', 'JP-RO-MTECH', 'Successfully Completed', 'Angajare: Tehnician Mentenanță și Metrologie, Mentenanță și inginerie'),
('EVT-RO-2018-0013', 'Hire', '20033', '2018-02-12', '2018-01-29 09:00:00+00', 'JP-RO-ITINF', 'Successfully Completed', 'Angajare: Inginer Infrastructură IT, IT'),
('EVT-RO-2018-0014', 'Hire', '20072', '2018-03-19', '2018-03-05 09:00:00+00', 'JP-RO-DG-WH', 'Successfully Completed', 'Angajare: Operator Depozit și Expediții ADR, Depozit și logistică'),
('EVT-RO-2018-0015', 'Hire', '20035', '2018-06-04', '2018-05-21 09:00:00+00', 'JP-RO-CONT', 'Successfully Completed', 'Angajare: Contabil Șef, Financiar-contabilitate'),
('EVT-RO-2018-0016', 'Hire', '20052', '2018-10-15', '2018-10-01 09:00:00+00', 'JP-RO-QCA', 'Successfully Completed', 'Angajare: Analist Control Calitate, Control calitate'),
('EVT-RO-2019-0017', 'Hire', '20038', '2019-01-14', '2018-12-31 09:00:00+00', 'JP-RO-CTRL', 'Successfully Completed', 'Angajare: Controller Financiar, Financiar-contabilitate'),
('EVT-RO-2019-0018', 'Hire', '20058', '2019-04-01', '2019-03-18 09:00:00+00', 'JP-RO-OP', 'Successfully Completed', 'Angajare: Operator Producție Sterile, Producție sterile'),
('EVT-RO-2019-0019', 'Hire', '20069', '2019-05-13', '2019-04-29 09:00:00+00', 'JP-RO-QAS', 'Successfully Completed', 'Angajare: Specialist Asigurarea Calității, Asigurarea calității'),
('EVT-RO-2019-0020', 'Hire', '20049', '2019-09-02', '2019-08-19 09:00:00+00', 'JP-RO-QCA', 'Successfully Completed', 'Angajare: Analist Control Calitate, Control calitate'),
('EVT-RO-2020-0021', 'Hire', '20055', '2020-02-17', '2020-02-03 09:00:00+00', 'JP-RO-QCM', 'Successfully Completed', 'Angajare: Analist Microbiologie, Control calitate'),
('EVT-RO-2020-0022', 'Hire', '20044', '2020-03-02', '2020-02-17 09:00:00+00', 'JP-RO-SEC', 'Successfully Completed', 'Angajare: Specialist Securitate IT, IT'),
('EVT-RO-2020-0023', 'Hire', '20061', '2020-07-06', '2020-06-22 09:00:00+00', 'JP-RO-OP', 'Successfully Completed', 'Angajare: Operator Producție Sterile, Producție sterile'),
('EVT-RO-2021-0024', 'Hire', '20075', '2021-02-01', '2021-01-18 09:00:00+00', 'JP-RO-AP', 'Successfully Completed', 'Angajare: Contabil Furnizori, Financiar-contabilitate'),
('EVT-RO-2021-0025', 'Hire', '20046', '2021-06-07', '2021-05-24 09:00:00+00', 'JP-RO-MKT', 'Successfully Completed', 'Angajare: Specialist Marketing, Vânzări și marketing'),
('EVT-RO-2022-0026', 'Hire', '20063', '2022-01-10', '2021-12-27 09:00:00+00', 'JP-RO-SERUM', 'Successfully Completed', 'Angajare: Specialist Laborator Ser Autolog, Laborator ser autolog'),
('EVT-RO-2022-0027', 'Hire', '20081', '2022-09-12', '2022-08-29 09:00:00+00', 'JP-RO-PV', 'Successfully Completed', 'Angajare: Responsabil Farmacovigilență, Afaceri de reglementare'),
('EVT-RO-2023-0028', 'Hire', '20086', '2023-03-06', '2023-02-20 09:00:00+00', 'JP-RO-OP', 'Successfully Completed', 'Angajare: Operator Producție Sterile, Producție sterile'),
('EVT-RO-2026-0029', 'Contract Contingent Worker', 'C0012', '2026-06-15', '2026-06-01 09:00:00+00', 'JP-RO-VAL', 'Successfully Completed', 'Angajare: Consultant Validare, Mentenanță și inginerie'),
('EVT-RO-2026-0030', 'Hire', '20084', '2026-09-01', '2026-08-18 09:00:00+00', 'JP-RO-QCA', 'Successfully Completed', 'Angajare: Analist Control Calitate, Control calitate'),
('EVT-RO-2026-0041', 'Terminate', '20049', '2026-07-31', '2026-07-10 09:25:00+00', NULL, 'Successfully Completed', 'Demisie: Analist Control Calitate, Control calitate; ultima zi 2026-07-31'),
('EVT-RO-2026-0044', 'Change Job', '20061', '2026-08-01', '2026-07-20 13:40:00+00', 'JP-RO-SERUM', 'Successfully Completed', 'Transfer: Operator Producție Sterile -> Specialist Laborator Ser Autolog')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.integration_event (
  integration_event_id      varchar(20) NOT NULL,
  business_process_event_id varchar(30) NOT NULL,
  integration_system_id     varchar(60) NOT NULL,
  initiated_moment          timestamptz NOT NULL,
  completed_moment          timestamptz,
  status                    varchar(20) NOT NULL,
  message                   text,
  CONSTRAINT integration_event_pk PRIMARY KEY (integration_event_id)
);
COMMENT ON TABLE workday_hcm.integration_event IS 'Outbound integration runs per business process event (Microsoft 365 over Graph, Kronos employee export).  There is no integration to on-premises Active Directory: AD accounts are created and disabled from IT helpdesk tickets.';

INSERT INTO workday_hcm.integration_event (integration_event_id, business_process_event_id, integration_system_id, initiated_moment, completed_moment, status, message) VALUES
('IE-006003', 'EVT-RO-2026-0029', 'INT_RO01_M365_Graph_Provisioning', '2026-06-01 09:12:00+00', '2026-06-01 09:15:00+00', 'Completed', NULL),
('IE-006006', 'EVT-RO-2026-0030', 'INT_RO01_M365_Graph_Provisioning', '2026-08-18 09:12:00+00', '2026-08-18 09:15:00+00', 'Completed', NULL),
('IE-006009', 'EVT-RO-2026-0030', 'INT_RO02_Kronos_Employee_Export', '2026-08-19 02:00:00+00', NULL, 'Error', 'Kronos: labour account RO01/RO10-130 not found for pay rule EKG-Salariat'),
('IE-006012', 'EVT-RO-2026-0030', 'INT_RO02_Kronos_Employee_Export', '2026-08-21 02:00:00+00', '2026-08-21 02:04:00+00', 'Completed', NULL),
('IE-006015', 'EVT-RO-2026-0041', 'INT_RO01_M365_Graph_Provisioning', '2026-07-31 17:57:00+00', '2026-07-31 18:00:00+00', 'Completed', NULL),
('IE-006018', 'EVT-RO-2026-0041', 'INT_RO02_Kronos_Employee_Export', '2026-08-01 10:45:00+00', '2026-08-01 10:48:00+00', 'Completed', NULL),
('IE-006021', 'EVT-RO-2026-0044', 'INT_RO01_M365_Graph_Provisioning', '2026-07-31 17:57:00+00', '2026-07-31 18:00:00+00', 'Completed', NULL),
('IE-006024', 'EVT-RO-2026-0044', 'INT_RO02_Kronos_Employee_Export', '2026-08-01 10:45:00+00', '2026-08-01 10:48:00+00', 'Completed', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.pay_run (
  pay_run_id         varchar(30) NOT NULL,
  pay_group          varchar(60) NOT NULL,
  company_id         varchar(10) NOT NULL,
  period_start_date  date NOT NULL,
  period_end_date    date NOT NULL,
  payment_date       date NOT NULL,
  worker_count       integer NOT NULL,
  total_gross_amount numeric(18,2) NOT NULL,
  currency           varchar(3) NOT NULL,
  status             varchar(20) NOT NULL,
  completed_moment   timestamptz,
  CONSTRAINT pay_run_pk PRIMARY KEY (pay_run_id)
);
COMMENT ON TABLE workday_hcm.pay_run IS 'Monthly pay runs (totals include the shift workers'' pay imported from Kronos).';

INSERT INTO workday_hcm.pay_run (pay_run_id, pay_group, company_id, period_start_date, period_end_date, payment_date, worker_count, total_gross_amount, currency, status, completed_moment) VALUES
('PR-RO01-2026-07', 'EKG Lunar RO', 'RO01', '2026-07-01', '2026-07-31', '2026-08-10', 27, 406493.25, 'RON', 'Complete', '2026-08-08 06:30:00+00'),
('PR-RO01-2026-08', 'EKG Lunar RO', 'RO01', '2026-08-01', '2026-08-31', '2026-09-10', 26, 398416.85, 'RON', 'Complete', '2026-09-08 06:30:00+00'),
('PR-RO01-2026-09', 'EKG Lunar RO', 'RO01', '2026-09-01', '2026-09-30', '2026-10-09', 0, 0.00, 'RON', 'In Progress', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.payroll_result (
  pay_run_id                    varchar(30) NOT NULL,
  employee_id                   varchar(20) NOT NULL,
  gross_amount                  numeric(18,2) NOT NULL,
  employer_contributions_amount numeric(18,2) NOT NULL,
  net_amount                    numeric(18,2) NOT NULL,
  cost_center_id                varchar(20) NOT NULL,
  ledger_account                varchar(20) NOT NULL,
  currency                      varchar(3) NOT NULL,
  CONSTRAINT payroll_result_pk PRIMARY KEY (pay_run_id, employee_id)
);
COMMENT ON TABLE workday_hcm.payroll_result IS 'Payroll results per worker (employer amount = CAM 2.25%).';

INSERT INTO workday_hcm.payroll_result (pay_run_id, employee_id, gross_amount, employer_contributions_amount, net_amount, cost_center_id, ledger_account, currency) VALUES
('PR-RO01-2026-07', '20011', 42000.00, 945.00, 24570.00, 'RO10-100', '641000', 'RON'),
('PR-RO01-2026-07', '20014', 32000.00, 720.00, 18720.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-07', '20017', 30000.00, 675.00, 17550.00, 'RO10-120', '641000', 'RON'),
('PR-RO01-2026-07', '20021', 28000.00, 630.00, 16380.00, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-07', '20023', 21000.00, 472.50, 12285.00, 'RO10-160', '641000', 'RON'),
('PR-RO01-2026-07', '20026', 19000.00, 427.50, 11115.00, 'RO10-170', '641000', 'RON'),
('PR-RO01-2026-07', '20029', 20000.00, 450.00, 11700.00, 'RO10-220', '641000', 'RON'),
('PR-RO01-2026-07', '20031', 20000.00, 450.00, 11700.00, 'RO10-230', '641000', 'RON'),
('PR-RO01-2026-07', '20033', 12500.00, 281.25, 7312.50, 'RO10-230', '641000', 'RON'),
('PR-RO01-2026-07', '20035', 16000.00, 360.00, 9360.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-07', '20038', 14000.00, 315.00, 8190.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-07', '20040', 17000.00, 382.50, 9945.00, 'RO10-150', '641000', 'RON'),
('PR-RO01-2026-07', '20042', 15500.00, 348.75, 9067.50, 'RO10-140', '641000', 'RON'),
('PR-RO01-2026-07', '20044', 12000.00, 270.00, 7020.00, 'RO10-230', '641000', 'RON'),
('PR-RO01-2026-07', '20049', 8200.00, 184.50, 4797.00, 'RO10-130', '641000', 'RON'),
('PR-RO01-2026-07', '20052', 9400.00, 211.50, 5499.00, 'RO10-130', '641000', 'RON'),
('PR-RO01-2026-07', '20055', 8800.00, 198.00, 5148.00, 'RO10-130', '641000', 'RON'),
('PR-RO01-2026-07', '20058', 7103.25, 159.82, 4155.40, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-07', '20061', 7220.00, 162.45, 4223.70, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-07', '20063', 7416.00, 166.86, 4338.36, 'RO10-115', '641000', 'RON'),
('PR-RO01-2026-07', '20066', 9856.00, 221.76, 5765.76, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-07', '20069', 11500.00, 258.75, 6727.50, 'RO10-120', '641000', 'RON'),
('PR-RO01-2026-07', '20072', 6052.00, 136.17, 3540.42, 'RO10-140', '641000', 'RON'),
('PR-RO01-2026-07', '20075', 7200.00, 162.00, 4212.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-07', '20078', 8064.00, 181.44, 4717.44, 'RO10-150', '641000', 'RON'),
('PR-RO01-2026-07', '20081', 9800.00, 220.50, 5733.00, 'RO10-160', '641000', 'RON'),
('PR-RO01-2026-07', '20086', 6882.00, 154.85, 4025.97, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-08', '20011', 42000.00, 945.00, 24570.00, 'RO10-100', '641000', 'RON'),
('PR-RO01-2026-08', '20014', 32000.00, 720.00, 18720.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-08', '20017', 30000.00, 675.00, 17550.00, 'RO10-120', '641000', 'RON'),
('PR-RO01-2026-08', '20021', 28000.00, 630.00, 16380.00, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-08', '20023', 21000.00, 472.50, 12285.00, 'RO10-160', '641000', 'RON'),
('PR-RO01-2026-08', '20026', 19000.00, 427.50, 11115.00, 'RO10-170', '641000', 'RON'),
('PR-RO01-2026-08', '20029', 20000.00, 450.00, 11700.00, 'RO10-220', '641000', 'RON'),
('PR-RO01-2026-08', '20031', 20000.00, 450.00, 11700.00, 'RO10-230', '641000', 'RON'),
('PR-RO01-2026-08', '20033', 12500.00, 281.25, 7312.50, 'RO10-230', '641000', 'RON'),
('PR-RO01-2026-08', '20035', 16000.00, 360.00, 9360.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-08', '20038', 14000.00, 315.00, 8190.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-08', '20040', 17000.00, 382.50, 9945.00, 'RO10-150', '641000', 'RON'),
('PR-RO01-2026-08', '20042', 15500.00, 348.75, 9067.50, 'RO10-140', '641000', 'RON'),
('PR-RO01-2026-08', '20044', 12000.00, 270.00, 7020.00, 'RO10-230', '641000', 'RON'),
('PR-RO01-2026-08', '20052', 9400.00, 211.50, 5499.00, 'RO10-130', '641000', 'RON'),
('PR-RO01-2026-08', '20055', 8800.00, 198.00, 5148.00, 'RO10-130', '641000', 'RON'),
('PR-RO01-2026-08', '20058', 6949.25, 156.36, 4065.31, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-08', '20061', 7140.00, 160.65, 4176.90, 'RO10-115', '641000', 'RON'),
('PR-RO01-2026-08', '20063', 7251.20, 163.15, 4241.95, 'RO10-115', '641000', 'RON'),
('PR-RO01-2026-08', '20066', 10192.00, 229.32, 5962.32, 'RO10-110', '641000', 'RON'),
('PR-RO01-2026-08', '20069', 11500.00, 258.75, 6727.50, 'RO10-120', '641000', 'RON'),
('PR-RO01-2026-08', '20072', 6194.40, 139.37, 3623.72, 'RO10-140', '641000', 'RON'),
('PR-RO01-2026-08', '20075', 7200.00, 162.00, 4212.00, 'RO10-210', '641000', 'RON'),
('PR-RO01-2026-08', '20078', 7884.80, 177.41, 4612.61, 'RO10-150', '641000', 'RON'),
('PR-RO01-2026-08', '20081', 9800.00, 220.50, 5733.00, 'RO10-160', '641000', 'RON'),
('PR-RO01-2026-08', '20086', 7105.20, 159.87, 4156.54, 'RO10-110', '641000', 'RON')
ON CONFLICT DO NOTHING;

-- Data subject requests received from the privacy rights process (subscription apply script buc_workday_hcm__rights_fulfilment_actions).
CREATE TABLE IF NOT EXISTS workday_hcm.data_privacy_request (
  request_id           varchar(40) NOT NULL,
  employee_id          varchar(20) NOT NULL,
  request_type         varchar(20) NOT NULL,
  received_moment      timestamptz,
  request_status       varchar(20),
  task_id              varchar(40),
  task_type            varchar(20),
  task_status          varchar(20),
  task_completed_moment timestamptz,
  last_updated         timestamptz NOT NULL,
  CONSTRAINT data_privacy_request_pk PRIMARY KEY (request_id)
);
COMMENT ON TABLE workday_hcm.data_privacy_request IS 'Data subject requests about EKG workers and the task Workday must perform for each (locate, disclose, rectify, erase, restrict).';

GRANT USAGE ON SCHEMA workday_hcm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA workday_hcm TO egeria_user, airflow_user;
