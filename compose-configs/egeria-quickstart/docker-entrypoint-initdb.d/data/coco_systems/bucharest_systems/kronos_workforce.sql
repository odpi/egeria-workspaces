-- system-qualified-name: SoftwareServer::SYS-023::Kronos Workforce
-- Kronos Workforce - Bucharest.  Kronos Workforce time and attendance for the EKG shift workers: people, labour
-- accounts, pay codes, timecard totals per pay period and the pay statements calculated for hourly staff and imported
-- into the Workday pay run.  Its tables feed Payroll Results (shift workers' postings).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS kronos_workforce;
COMMENT ON SCHEMA kronos_workforce IS 'Kronos Workforce (EKG): Workforce Central style tables (PERSON, LABORACCT, PAYCODE, WFCTOTAL) and the payroll pay statement export, lower-cased by the replication job.';

CREATE TABLE IF NOT EXISTS kronos_workforce.laboracct (
  laboracctid   integer NOT NULL,
  laboracctname varchar(120) NOT NULL,
  laborlev1nm   varchar(20) NOT NULL,
  laborlev2nm   varchar(20) NOT NULL,
  laborlev3nm   varchar(60),
  CONSTRAINT laboracct_pk PRIMARY KEY (laboracctid)
);
COMMENT ON TABLE kronos_workforce.laboracct IS 'Labour accounts: company / cost centre / department.';

INSERT INTO kronos_workforce.laboracct (laboracctid, laboracctname, laborlev1nm, laborlev2nm, laborlev3nm) VALUES
(3001, 'RO01/RO10-100/Conducere', 'RO01', 'RO10-100', 'Conducere'),
(3002, 'RO01/RO10-110/Producție sterile', 'RO01', 'RO10-110', 'Producție sterile'),
(3003, 'RO01/RO10-115/Laborator ser autolog', 'RO01', 'RO10-115', 'Laborator ser autolog'),
(3004, 'RO01/RO10-120/Asigurarea calității', 'RO01', 'RO10-120', 'Asigurarea calității'),
(3005, 'RO01/RO10-130/Control calitate', 'RO01', 'RO10-130', 'Control calitate'),
(3006, 'RO01/RO10-140/Depozit și logistică', 'RO01', 'RO10-140', 'Depozit și logistică'),
(3007, 'RO01/RO10-150/Mentenanță și inginerie', 'RO01', 'RO10-150', 'Mentenanță și inginerie'),
(3008, 'RO01/RO10-160/Afaceri de reglementare', 'RO01', 'RO10-160', 'Afaceri de reglementare'),
(3009, 'RO01/RO10-170/Vânzări și marketing', 'RO01', 'RO10-170', 'Vânzări și marketing'),
(3010, 'RO01/RO10-210/Financiar-contabilitate', 'RO01', 'RO10-210', 'Financiar-contabilitate'),
(3011, 'RO01/RO10-220/Resurse umane', 'RO01', 'RO10-220', 'Resurse umane'),
(3012, 'RO01/RO10-230/IT', 'RO01', 'RO10-230', 'IT')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS kronos_workforce.person (
  personid            integer NOT NULL,
  personnum           varchar(20) NOT NULL,
  firstnm             varchar(80) NOT NULL,
  lastnm              varchar(80) NOT NULL,
  payrulenm           varchar(60) NOT NULL,
  homelaboracctid     integer NOT NULL,
  hiredtm             date NOT NULL,
  employmentstatus    varchar(20) NOT NULL,
  employmentstatusdtm date NOT NULL,
  CONSTRAINT person_pk PRIMARY KEY (personid)
);
COMMENT ON TABLE kronos_workforce.person IS 'People exported from Workday (personnum = Workday employee ID); salaried staff clock in and out but are paid by Workday.';

INSERT INTO kronos_workforce.person (personid, personnum, firstnm, lastnm, payrulenm, homelaboracctid, hiredtm, employmentstatus, employmentstatusdtm) VALUES
(100201, '20011', 'Andrei', 'Munteanu', 'EKG-Salariat', 3001, '2012-02-01', 'Active', '2012-02-01'),
(100202, '20014', 'Gheorghe', 'Radu', 'EKG-Salariat', 3010, '2013-05-06', 'Active', '2013-05-06'),
(100203, '20017', 'Nicoleta', 'Oprea', 'EKG-Salariat', 3004, '2014-09-01', 'Active', '2014-09-01'),
(100204, '20021', 'Florin', 'Stoica', 'EKG-Salariat', 3002, '2015-03-02', 'Active', '2015-03-02'),
(100205, '20023', 'Adina', 'Petre', 'EKG-Salariat', 3008, '2016-01-11', 'Active', '2016-01-11'),
(100206, '20026', 'Cristian', 'Lungu', 'EKG-Salariat', 3009, '2016-10-03', 'Active', '2016-10-03'),
(100207, '20029', 'Luminița', 'Chiriac', 'EKG-Salariat', 3011, '2017-04-18', 'Active', '2017-04-18'),
(100208, '20031', 'Mihai', 'Constantin', 'EKG-Salariat', 3012, '2017-08-01', 'Active', '2017-08-01'),
(100209, '20033', 'Lucian', 'Preda', 'EKG-Salariat', 3012, '2018-02-12', 'Active', '2018-02-12'),
(100210, '20035', 'Mihaela', 'Apostol', 'EKG-Salariat', 3010, '2018-06-04', 'Active', '2018-06-04'),
(100211, '20038', 'Simona', 'Florescu', 'EKG-Salariat', 3010, '2019-01-14', 'Active', '2019-01-14'),
(100212, '20040', 'Marian', 'Bucur', 'EKG-Salariat', 3007, '2015-11-02', 'Active', '2015-11-02'),
(100213, '20042', 'Ciprian', 'Tudor', 'EKG-Salariat', 3006, '2016-05-16', 'Active', '2016-05-16'),
(100214, '20044', 'Sorin', 'Matei', 'EKG-Salariat', 3012, '2020-03-02', 'Active', '2020-03-02'),
(100215, '20046', 'Roxana', 'Dumitrescu', 'EKG-Salariat', 3009, '2021-06-07', 'Active', '2021-06-07'),
(100216, '20049', 'Sebastian', 'Vasile', 'EKG-Salariat', 3005, '2019-09-02', 'Terminated', '2026-07-31'),
(100217, '20052', 'Elena', 'Popescu', 'EKG-Salariat', 3005, '2018-10-15', 'Active', '2018-10-15'),
(100218, '20055', 'Ioana', 'Stan', 'EKG-Salariat', 3005, '2020-02-17', 'Active', '2020-02-17'),
(100219, '20058', 'Bogdan', 'Ionescu', 'EKG-Tura-3x8', 3002, '2019-04-01', 'Active', '2019-04-01'),
(100220, '20061', 'Alexandru', 'Dinu', 'EKG-Tura-3x8', 3003, '2020-07-06', 'Active', '2020-07-06'),
(100221, '20063', 'Cătălina', 'Marin', 'EKG-Tura-3x8', 3003, '2022-01-10', 'Active', '2022-01-10'),
(100222, '20066', 'Vlad', 'Georgescu', 'EKG-Tura-3x8', 3002, '2016-09-05', 'Active', '2016-09-05'),
(100223, '20069', 'Raluca', 'Enache', 'EKG-Salariat', 3004, '2019-05-13', 'Active', '2019-05-13'),
(100224, '20072', 'Dan', 'Ilie', 'EKG-Tura-3x8', 3006, '2018-03-19', 'Active', '2018-03-19'),
(100225, '20075', 'Oana', 'Nistor', 'EKG-Salariat', 3010, '2021-02-01', 'Active', '2021-02-01'),
(100226, '20078', 'Radu', 'Stoian', 'EKG-Tura-3x8', 3007, '2017-11-20', 'Active', '2017-11-20'),
(100227, '20081', 'Gabriela', 'Toma', 'EKG-Salariat', 3008, '2022-09-12', 'Active', '2022-09-12'),
(100228, '20084', 'Irina', 'Moldovan', 'EKG-Salariat', 3005, '2026-09-01', 'Active', '2026-09-01'),
(100229, '20086', 'Ștefan', 'Pavel', 'EKG-Tura-3x8', 3002, '2023-03-06', 'Active', '2023-03-06')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS kronos_workforce.paycode (
  paycodeid        integer NOT NULL,
  name             varchar(60) NOT NULL,
  abbreviationchar varchar(10) NOT NULL,
  CONSTRAINT paycode_pk PRIMARY KEY (paycodeid)
);
COMMENT ON TABLE kronos_workforce.paycode IS 'Pay codes.';

INSERT INTO kronos_workforce.paycode (paycodeid, name, abbreviationchar) VALUES
(101, 'Ore normale', 'REG'),
(102, 'Spor noapte 25%', 'NIGHT'),
(103, 'Ore suplimentare 75%', 'OT')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS kronos_workforce.wfctotal (
  wfctotalid      bigint NOT NULL,
  employeeid      integer NOT NULL,
  applydtm        date NOT NULL,
  paycodeid       integer NOT NULL,
  laboracctid     integer NOT NULL,
  durationsecsqty integer NOT NULL,
  moneyamt        numeric(18,2) NOT NULL,
  CONSTRAINT wfctotal_pk PRIMARY KEY (wfctotalid)
);
COMMENT ON TABLE kronos_workforce.wfctotal IS 'Timecard totals per person, pay period end, pay code and labour account (money in RON at the person''s base rate).';

INSERT INTO kronos_workforce.wfctotal (wfctotalid, employeeid, applydtm, paycodeid, laboracctid, durationsecsqty, moneyamt) VALUES
(900001, 100219, '2026-07-31', 101, 3002, 604800, 6468.00),
(900002, 100219, '2026-07-31', 102, 3002, 172800, 462.00),
(900003, 100219, '2026-07-31', 103, 3002, 21600, 173.25),
(900004, 100220, '2026-07-31', 101, 3002, 604800, 6720.00),
(900005, 100220, '2026-07-31', 102, 3002, 115200, 320.00),
(900006, 100220, '2026-07-31', 103, 3002, 21600, 180.00),
(900007, 100221, '2026-07-31', 101, 3003, 604800, 6921.60),
(900008, 100221, '2026-07-31', 102, 3003, 172800, 494.40),
(900009, 100222, '2026-07-31', 101, 3002, 604800, 9408.00),
(900010, 100222, '2026-07-31', 102, 3002, 115200, 448.00),
(900011, 100224, '2026-07-31', 101, 3006, 576000, 5696.00),
(900012, 100224, '2026-07-31', 102, 3006, 144000, 356.00),
(900013, 100226, '2026-07-31', 101, 3007, 604800, 7526.40),
(900014, 100226, '2026-07-31', 102, 3007, 172800, 537.60),
(900015, 100229, '2026-07-31', 101, 3002, 604800, 6249.60),
(900016, 100229, '2026-07-31', 102, 3002, 115200, 297.60),
(900017, 100229, '2026-07-31', 103, 3002, 43200, 334.80),
(900018, 100219, '2026-08-31', 101, 3002, 604800, 6468.00),
(900019, 100219, '2026-08-31', 102, 3002, 115200, 308.00),
(900020, 100219, '2026-08-31', 103, 3002, 21600, 173.25),
(900021, 100220, '2026-08-31', 101, 3003, 576000, 6400.00),
(900022, 100220, '2026-08-31', 102, 3003, 201600, 560.00),
(900023, 100220, '2026-08-31', 103, 3003, 21600, 180.00),
(900024, 100221, '2026-08-31', 101, 3003, 604800, 6921.60),
(900025, 100221, '2026-08-31', 102, 3003, 115200, 329.60),
(900026, 100222, '2026-08-31', 101, 3002, 604800, 9408.00),
(900027, 100222, '2026-08-31', 102, 3002, 201600, 784.00),
(900028, 100224, '2026-08-31', 101, 3006, 604800, 5980.80),
(900029, 100224, '2026-08-31', 102, 3006, 86400, 213.60),
(900030, 100226, '2026-08-31', 101, 3007, 604800, 7526.40),
(900031, 100226, '2026-08-31', 102, 3007, 115200, 358.40),
(900032, 100229, '2026-08-31', 101, 3002, 604800, 6249.60),
(900033, 100229, '2026-08-31', 102, 3002, 201600, 520.80),
(900034, 100229, '2026-08-31', 103, 3002, 43200, 334.80)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS kronos_workforce.pay_statement (
  pay_statement_id   varchar(30) NOT NULL,
  personid           integer NOT NULL,
  payroll_reference  varchar(30) NOT NULL,
  pay_period_start   date NOT NULL,
  pay_period_end     date NOT NULL,
  pay_date           date NOT NULL,
  worked_laboracctid integer NOT NULL,
  total_hours        numeric(8,2) NOT NULL,
  gross_wages        numeric(18,2) NOT NULL,
  employer_contrib   numeric(18,2) NOT NULL,
  net_pay            numeric(18,2) NOT NULL,
  gl_account         varchar(20) NOT NULL,
  CONSTRAINT pay_statement_pk PRIMARY KEY (pay_statement_id)
);
COMMENT ON TABLE kronos_workforce.pay_statement IS 'Pay statements of hourly shift workers (payroll_reference = the Workday pay run they are imported into; employer contribution = CAM 2.25%).';

INSERT INTO kronos_workforce.pay_statement (pay_statement_id, personid, payroll_reference, pay_period_start, pay_period_end, pay_date, worked_laboracctid, total_hours, gross_wages, employer_contrib, net_pay, gl_account) VALUES
('PS-202607-100219', 100219, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3002, 174, 7103.25, 159.82, 4155.40, '641000'),
('PS-202607-100220', 100220, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3002, 174, 7220.00, 162.45, 4223.70, '641000'),
('PS-202607-100221', 100221, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3003, 168, 7416.00, 166.86, 4338.36, '641000'),
('PS-202607-100222', 100222, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3002, 168, 9856.00, 221.76, 5765.76, '641000'),
('PS-202607-100224', 100224, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3006, 160, 6052.00, 136.17, 3540.42, '641000'),
('PS-202607-100226', 100226, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3007, 168, 8064.00, 181.44, 4717.44, '641000'),
('PS-202607-100229', 100229, 'PR-RO01-2026-07', '2026-07-01', '2026-07-31', '2026-08-10', 3002, 180, 6882.00, 154.85, 4025.97, '641000'),
('PS-202608-100219', 100219, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3002, 174, 6949.25, 156.36, 4065.31, '641000'),
('PS-202608-100220', 100220, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3003, 166, 7140.00, 160.65, 4176.90, '641000'),
('PS-202608-100221', 100221, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3003, 168, 7251.20, 163.15, 4241.95, '641000'),
('PS-202608-100222', 100222, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3002, 168, 10192.00, 229.32, 5962.32, '641000'),
('PS-202608-100224', 100224, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3006, 168, 6194.40, 139.37, 3623.72, '641000'),
('PS-202608-100226', 100226, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3007, 168, 7884.80, 177.41, 4612.61, '641000'),
('PS-202608-100229', 100229, 'PR-RO01-2026-08', '2026-08-01', '2026-08-31', '2026-09-10', 3002, 180, 7105.20, 159.87, 4156.54, '641000')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA kronos_workforce TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA kronos_workforce TO egeria_user, airflow_user;
