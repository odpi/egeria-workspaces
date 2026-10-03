-- system-qualified-name: System::cocopages
-- CocoPages - Coco core.  Homegrown employee directory including business partners; its worker entries feed Corporate Directory Entries.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS cocopages;
COMMENT ON SCHEMA cocopages IS 'CocoPages (Coco core): the corporate directory of workers and business partners.';

CREATE TABLE IF NOT EXISTS cocopages.dir_person (
  uid varchar(30) NOT NULL,
  worker_ref varchar(20),
  fname varchar(40) NOT NULL,
  lname varchar(40) NOT NULL,
  title varchar(80) NOT NULL,
  dept varchar(80) NOT NULL,
  loc varchar(40) NOT NULL,
  mgr_uid varchar(30),
  phone varchar(30),
  entry_typ varchar(3) NOT NULL,
  last_sync timestamptz NOT NULL,
  CONSTRAINT dir_person_pk PRIMARY KEY (uid)
);
COMMENT ON TABLE cocopages.dir_person IS 'Directory entries keyed by login uid. entry_typ EMP employee, CTR contractor, PTN business partner (no worker_ref); last_sync is when the entry was last refreshed from HRIM.';

INSERT INTO cocopages.dir_person (uid, worker_ref, fname, lname, title, dept, loc, mgr_uid, phone, entry_typ, last_sync) VALUES
('terridaring', 'CW-KTVC4J', 'Terri', 'Daring', 'Founder and Site Head', 'Executive Office', 'London', NULL, '+44 20 7946 0101', 'EMP', '2026-03-02 06:00+00'),
('reggiemint', 'CW-T8FK9X', 'Reggie', 'Mint', 'Chief Finance Officer', 'Finance', 'London', 'terridaring', '+44 20 7946 0110', 'EMP', '2026-03-02 06:00+00'),
('tomtally', 'CW-EZMUNR', 'Tom', 'Tally', 'Accounts Manager, Finance HQ', 'Finance HQ', 'London', 'reggiemint', '+44 20 7946 0114', 'EMP', '2026-03-02 06:00+00'),
('sallycounter', 'CW-GMCZHC', 'Sally', 'Counter', 'Payments Clerk', 'Finance Operations', 'London', 'tomtally', '+44 20 7946 0117', 'EMP', '2026-03-02 06:00+00'),
('juleskeeper', 'CW-SNZYHU', 'Jules', 'Keeper', 'Chief Data Officer', 'Data Office', 'London', 'terridaring', '+44 20 7946 0120', 'EMP', '2026-03-02 06:00+00'),
('erinoverview', 'CW-VYNNPZ', 'Erin', 'Overview', 'Information Architect', 'Data Office', 'London', 'juleskeeper', '+44 20 7946 0123', 'EMP', '2026-03-02 06:00+00'),
('peterprofile', 'CW-CR43HM', 'Peter', 'Profile', 'Information Analyst', 'Data Office', 'London', 'erinoverview', '+44 20 7946 0124', 'EMP', '2026-03-02 06:00+00'),
('hugosalle', 'CW-JPKHTU', 'Hugo', 'Salle', 'Sales Representative', 'Sales', 'London', 'harryhopeful', '+44 20 7946 0131', 'EMP', '2026-03-02 06:00+00'),
('stewfaster', 'CW-SFRGJQ', 'Stew', 'Faster', 'Head of Manufacturing', 'Manufacturing', 'London', 'terridaring', '+44 20 7946 0140', 'EMP', '2026-03-02 06:00+00'),
('helenbarlow', 'CW-B76CPN', 'Helen', 'Barlow', 'Qualified Person', 'Winchester Quality Assurance', 'Winchester', 'stewfaster', '+44 1962 555 210', 'EMP', '2026-03-02 06:00+00'),
('martingrange', 'CW-F53CJR', 'Martin', 'Grange', 'Manufacturing Operator', 'Winchester Manufacturing', 'Winchester', 'helenbarlow', '+44 1962 555 231', 'EMP', '2026-03-02 06:00+00'),
('aisharahman', 'CW-XE6DBG', 'Aisha', 'Rahman', 'Cell Therapy Operator', 'Winchester Cell Therapy', 'Winchester', 'helenbarlow', '+44 1962 555 244', 'EMP', '2025-11-03 06:00+00'),
('owentate', 'CW-K7H7ZQ', 'Owen', 'Tate', 'Cell Therapy Operator', 'Winchester Cell Therapy', 'Winchester', 'helenbarlow', '+44 1962 555 263', 'EMP', '2026-08-03 06:00+00'),
('davepearce', 'CW-7G8SM2', 'Dave', 'Pearce', 'Depot Dangerous Goods Supervisor', 'Winchester Depot', 'Winchester', 'stewfaster', '+44 1962 555 252', 'EMP', '2026-03-02 06:00+00'),
('sidneyseeker', 'CW-KDVCEA', 'Sidney', 'Seeker', 'Security Consultant', 'Information Security', 'London', 'ivorpadlock', '+44 20 7946 0177', 'CTR', '2026-06-01 06:00+00'),
('stevestarter', 'CW-38FTNV', 'Steve', 'Starter', 'Founder and Site Head', 'Executive Office', 'Amsterdam', NULL, '+31 20 555 0101', 'EMP', '2026-03-02 06:00+00'),
('faithbroker', 'CW-TC93US', 'Faith', 'Broker', 'HR Director and Chief Privacy Officer', 'Human Resources', 'Amsterdam', 'stevestarter', '+31 20 555 0110', 'EMP', '2026-03-02 06:00+00'),
('garygeeke', 'CW-7K8YQG', 'Gary', 'Geeke', 'IT Infrastructure Lead', 'IT Infrastructure', 'Amsterdam', 'stevestarter', '+31 20 555 0120', 'EMP', '2026-03-02 06:00+00'),
('pollytasker', 'CW-FM4E2G', 'Polly', 'Tasker', 'IT Project Leader', 'IT Projects', 'Amsterdam', 'stevestarter', '+31 20 555 0123', 'EMP', '2026-03-02 06:00+00'),
('lemmiestage', 'CW-T3HUQE', 'Lemmie', 'Stage', 'DataStage Specialist', 'IT Infrastructure', 'Amsterdam', 'garygeeke', '+31 20 555 0125', 'EMP', '2026-03-02 06:00+00'),
('bobnitter', 'CW-DLMYL9', 'Bob', 'Nitter', 'Integration Architect and Developer', 'IT Infrastructure', 'Amsterdam', 'garygeeke', '+31 20 555 0127', 'EMP', '2026-03-02 06:00+00'),
('maurazeller', 'CW-K34WSJ', 'Maura', 'Zeller', 'Sales Representative', 'Sales', 'Amsterdam', 'harryhopeful', '+31 20 555 0131', 'EMP', '2026-03-02 06:00+00'),
('zachnow', 'CW-U5PPXA', 'Zach', 'Now', 'Founder and Site Head', 'Executive Office', 'New York', NULL, '+1 212 555 0101', 'EMP', '2026-03-02 06:00+00'),
('harryhopeful', 'CW-5V7T2Y', 'Harry', 'Hopeful', 'Sales Leader', 'Sales', 'New York', 'zachnow', '+1 212 555 0130', 'EMP', '2026-03-02 06:00+00'),
('margodeal', 'CW-W9JFK6', 'Margo', 'Deal', 'Sales Representative', 'Sales', 'New York', 'harryhopeful', '+1 212 555 0132', 'EMP', '2026-03-02 06:00+00'),
('tessatube', 'CW-RMRC8S', 'Tessa', 'Tube', 'Lead Researcher', 'Research', 'New York', 'zachnow', '+1 212 555 0140', 'EMP', '2026-03-02 06:00+00'),
('calliequartile', 'CW-X2F75Q', 'Callie', 'Quartile', 'Data Scientist', 'Research', 'New York', 'tessatube', '+1 212 555 0142', 'EMP', '2026-03-02 06:00+00'),
('tanyatidie', 'CW-T3WZE8', 'Tanya', 'Tidie', 'Clinical Records Clerk', 'Clinical Records', 'New York', 'tessatube', '+1 212 555 0145', 'EMP', '2026-03-02 06:00+00'),
('ivorpadlock', 'CW-3NSATA', 'Ivor', 'Padlock', 'Chief Information Security Officer', 'Information Security', 'New York', 'zachnow', '+1 212 555 0170', 'EMP', '2026-03-02 06:00+00'),
('luisortega', 'CW-PLYYBU', 'Luis', 'Ortega', 'Depot Dangerous Goods Supervisor', 'Kansas City Depot', 'Kansas City', 'stewfaster', '+1 913 555 0118', 'EMP', '2026-03-02 06:00+00'),
('chantalroy', 'CW-G32FNJ', 'Chantal', 'Roy', 'Qualified Person', 'Edmonton Quality Assurance', 'Edmonton', 'stewfaster', '+1 780 555 0145', 'EMP', '2026-03-02 06:00+00'),
('benkowalski', 'CW-HFD9LG', 'Ben', 'Kowalski', 'Manufacturing Operator', 'Edmonton Manufacturing', 'Edmonton', 'chantalroy', '+1 780 555 0152', 'EMP', '2026-03-02 06:00+00'),
('priyasingh', 'CW-JS5LWU', 'Priya', 'Singh', 'Manufacturing Supervisor', 'Edmonton Manufacturing', 'Edmonton', 'chantalroy', '+1 780 555 0167', 'EMP', '2026-07-01 06:00+00'),
('tomwhitehorse', 'CW-GBAX2A', 'Tom', 'Whitehorse', 'Depot Dangerous Goods Supervisor', 'Edmonton Depot', 'Edmonton', 'stewfaster', '+1 780 555 0171', 'EMP', '2026-03-02 06:00+00'),
('grantable', NULL, 'Grant', 'Able', 'Consultant', 'Hampton Hospital', 'New York', NULL, '+1 212 555 0417', 'PTN', '2025-02-11 06:00+00'),
('juliestitched', NULL, 'Julie', 'Stitched', 'Surgeon', 'Bowden Arrow Hospital', 'Boston', NULL, NULL, 'PTN', '2025-02-11 06:00+00'),
('nelliedunn', NULL, 'Nellie', 'Dunn', 'Data Office', 'Old Market Hospital', 'Omaha', NULL, NULL, 'PTN', '2025-02-11 06:00+00')
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS cocopages.hr_sync (
  worker_ref varchar(20) NOT NULL,
  entry_typ varchar(3) NOT NULL,
  loc_cd varchar(4) NOT NULL,
  hire_dt date NOT NULL,
  leave_dt date,
  hr_sts varchar(10) NOT NULL,
  title varchar(120),
  mgr_ref varchar(20),
  CONSTRAINT hr_sync_pk PRIMARY KEY (worker_ref)
);
COMMENT ON TABLE cocopages.hr_sync IS 'Worker records received from HR (Worker Master Data) waiting for the nightly directory refresh: new workers to add, title and manager changes, and leavers whose dir_person entry is to be removed.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA cocopages TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA cocopages TO egeria_user, airflow_user;
