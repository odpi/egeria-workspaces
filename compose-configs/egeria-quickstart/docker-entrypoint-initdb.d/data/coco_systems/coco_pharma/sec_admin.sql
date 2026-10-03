-- system-qualified-name: System::sec-admin
-- SecAdmin - Coco core.  Homegrown security administration for all access grants to Coco systems; feeds Access Entitlements.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS sec_admin;
COMMENT ON SCHEMA sec_admin IS 'SecAdmin (Coco core): entitlements, accounts and grants.';

CREATE TABLE IF NOT EXISTS sec_admin.sa_entitlement (
  sys_cd varchar(30) NOT NULL,
  ent_cd varchar(30) NOT NULL,
  ent_desc text NOT NULL,
  owner_yn char(1) NOT NULL,
  CONSTRAINT sa_entitlement_pk PRIMARY KEY (sys_cd, ent_cd)
);
COMMENT ON TABLE sec_admin.sa_entitlement IS 'Entitlements defined per system; owner_yn Y where holding it makes the worker a data owner in the catalogue.';

CREATE TABLE IF NOT EXISTS sec_admin.sa_user (
  acct_id varchar(60) NOT NULL,
  sys_cd varchar(30) NOT NULL,
  login varchar(30) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  created_dt date NOT NULL,
  removed_dt date,
  acct_sts char(1) NOT NULL,
  last_hr_evt varchar(16) NOT NULL,
  CONSTRAINT sa_user_pk PRIMARY KEY (acct_id)
);
COMMENT ON TABLE sec_admin.sa_user IS 'Accounts per worker per system. acct_sts A active, S suspended, R removed; last_hr_evt is the HRIM event that last changed it.';

CREATE TABLE IF NOT EXISTS sec_admin.sa_grant (
  acct_id varchar(60) NOT NULL,
  ent_cd varchar(30) NOT NULL,
  granted_dt date NOT NULL,
  revoked_dt date,
  CONSTRAINT sa_grant_pk PRIMARY KEY (acct_id, ent_cd)
);
COMMENT ON TABLE sec_admin.sa_grant IS 'Entitlements granted to each account.';

INSERT INTO sec_admin.sa_entitlement (sys_cd, ent_cd, ent_desc, owner_yn) VALUES
('winch-mfg-control', 'WMC_OPERATOR', 'Execute and sign process steps', 'N'),
('winch-mfg-control', 'WMC_QP', 'Certify and release batches', 'N'),
('ed-mfg-control', 'EMC_OPERATOR', 'Execute and sign operations', 'N'),
('ed-mfg-control', 'EMC_SUPERVISOR', 'Approve deviations and reassign operations', 'N'),
('ed-mfg-control', 'EMC_QP', 'Certify and release lots', 'N'),
('coco-ledgers', 'GL_AP_PAYER', 'Authorise supplier payments', 'N'),
('coco-ledgers', 'GL_JE_APPROVER', 'Approve manual journals', 'N'),
('coco-ledgers', 'GL_READ_ALL', 'Read all ledgers and payables', 'N'),
('coco-ledgers', 'GL_OWNER', 'Owner of ledger data in the open metadata catalogue', 'Y'),
('procurement01', 'PRC_VENDOR_ADMIN', 'Create and change vendors and bank details', 'N'),
('globalCRM', 'CRM_SALES', 'Manage accounts and orders', 'N'),
('coco-hrim', 'HR_ADMIN', 'Maintain worker records', 'N'),
('coco-hrim', 'HR_OWNER', 'Owner of worker data in the open metadata catalogue', 'Y'),
('egeria', 'CAT_DATA_OWNER', 'Data owner role in the open metadata catalogue', 'Y'),
('coco-inventory', 'INV_ADMIN', 'Administer inventory locations and items', 'N')
ON CONFLICT DO NOTHING;

INSERT INTO sec_admin.sa_user (acct_id, sys_cd, login, worker_ref, created_dt, removed_dt, acct_sts, last_hr_evt) VALUES
('winch-mfg-control:mgrange', 'winch-mfg-control', 'mgrange', 'CW-F53CJR', '2017-09-04', NULL, 'A', 'HRE-2017-0027'),
('winch-mfg-control:arahman', 'winch-mfg-control', 'arahman', 'CW-XE6DBG', '2025-10-30', NULL, 'A', 'HRE-2025-0044'),
('winch-mfg-control:otate', 'winch-mfg-control', 'otate', 'CW-K7H7ZQ', '2026-08-03', NULL, 'A', 'HRE-2026-0034'),
('winch-mfg-control:hbarlow', 'winch-mfg-control', 'hbarlow', 'CW-B76CPN', '2014-06-02', NULL, 'A', 'HRE-2014-0019'),
('ed-mfg-control:bkowalski', 'ed-mfg-control', 'bkowalski', 'CW-HFD9LG', '2018-01-15', NULL, 'A', 'HRE-2018-0004'),
('ed-mfg-control:psingh', 'ed-mfg-control', 'psingh', 'CW-JS5LWU', '2024-05-06', NULL, 'A', 'HRE-2026-0029'),
('ed-mfg-control:croy', 'ed-mfg-control', 'croy', 'CW-G32FNJ', '2015-08-17', NULL, 'A', 'HRE-2015-0031'),
('coco-ledgers:scounter', 'coco-ledgers', 'scounter', 'CW-GMCZHC', '2019-11-01', NULL, 'A', 'HRE-2012-0014'),
('coco-ledgers:ttally', 'coco-ledgers', 'ttally', 'CW-EZMUNR', '2020-07-10', NULL, 'A', 'HRE-2020-0016'),
('coco-ledgers:rmint', 'coco-ledgers', 'rmint', 'CW-T8FK9X', '2019-11-01', NULL, 'A', 'HRE-2018-0003'),
('coco-ledgers:sseeker', 'coco-ledgers', 'sseeker', 'CW-KDVCEA', '2026-05-29', NULL, 'A', 'HRE-2026-0022'),
('procurement01:rleftie', 'procurement01', 'rleftie', 'CW-E82P52', '2021-01-01', '2021-05-20', 'R', 'HRE-2021-0013'),
('globalCRM:mzeller', 'globalCRM', 'mzeller', 'CW-K34WSJ', '2019-03-01', NULL, 'A', 'HRE-2012-0021'),
('globalCRM:hsalle', 'globalCRM', 'hsalle', 'CW-JPKHTU', '2019-03-01', NULL, 'A', 'HRE-2013-0006'),
('coco-hrim:fbroker', 'coco-hrim', 'fbroker', 'CW-TC93US', '2018-02-01', NULL, 'A', 'HRE-2018-0008'),
('egeria:eoverview', 'egeria', 'eoverview', 'CW-VYNNPZ', '2023-05-15', NULL, 'A', 'HRE-2019-0015'),
('egeria:ttidie', 'egeria', 'ttidie', 'CW-T3WZE8', '2025-02-11', NULL, 'S', 'HRE-2015-0012'),
('coco-inventory:ggeeke', 'coco-inventory', 'ggeeke', 'CW-7K8YQG', '2020-05-01', NULL, 'A', 'HRE-2020-0011')
ON CONFLICT DO NOTHING;

INSERT INTO sec_admin.sa_grant (acct_id, ent_cd, granted_dt, revoked_dt) VALUES
('winch-mfg-control:mgrange', 'WMC_OPERATOR', '2017-09-04', NULL),
('winch-mfg-control:arahman', 'WMC_OPERATOR', '2025-10-30', NULL),
('winch-mfg-control:otate', 'WMC_OPERATOR', '2026-08-03', NULL),
('winch-mfg-control:hbarlow', 'WMC_QP', '2014-06-02', NULL),
('ed-mfg-control:bkowalski', 'EMC_OPERATOR', '2018-01-15', NULL),
('ed-mfg-control:psingh', 'EMC_OPERATOR', '2024-05-06', '2026-06-30'),
('ed-mfg-control:psingh', 'EMC_SUPERVISOR', '2026-06-30', NULL),
('ed-mfg-control:croy', 'EMC_QP', '2015-08-17', NULL),
('coco-ledgers:scounter', 'GL_AP_PAYER', '2019-11-01', NULL),
('coco-ledgers:ttally', 'GL_JE_APPROVER', '2020-07-10', NULL),
('coco-ledgers:ttally', 'GL_AP_PAYER', '2021-06-01', NULL),
('coco-ledgers:rmint', 'GL_JE_APPROVER', '2019-11-01', NULL),
('coco-ledgers:rmint', 'GL_OWNER', '2023-05-15', NULL),
('coco-ledgers:sseeker', 'GL_READ_ALL', '2026-05-29', NULL),
('procurement01:rleftie', 'PRC_VENDOR_ADMIN', '2021-01-01', '2021-05-20'),
('globalCRM:mzeller', 'CRM_SALES', '2019-03-01', NULL),
('globalCRM:hsalle', 'CRM_SALES', '2019-03-01', NULL),
('coco-hrim:fbroker', 'HR_ADMIN', '2018-02-01', NULL),
('coco-hrim:fbroker', 'HR_OWNER', '2023-05-15', NULL),
('egeria:eoverview', 'CAT_DATA_OWNER', '2023-05-15', NULL),
('egeria:ttidie', 'CAT_DATA_OWNER', '2025-02-11', NULL),
('coco-inventory:ggeeke', 'INV_ADMIN', '2020-05-01', NULL)
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS sec_admin.sa_hr_feed (
  worker_ref varchar(20) NOT NULL,
  worker_cat varchar(3) NOT NULL,
  company varchar(10) NOT NULL,
  site_cd varchar(4) NOT NULL,
  hire_dt date NOT NULL,
  leave_dt date,
  hr_sts char(1) NOT NULL,
  job_cd varchar(40),
  mgr_ref varchar(20),
  action_req varchar(9),
  CONSTRAINT sa_hr_feed_pk PRIMARY KEY (worker_ref)
);
COMMENT ON TABLE sec_admin.sa_hr_feed IS 'Worker status received from HR (Worker Master Data). hr_sts A active, L leave, T terminated; action_req PROVISION for an active worker with no accounts, REVOKE for a leaver who still has active accounts - the security administrators work this queue.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA sec_admin TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA sec_admin TO egeria_user, airflow_user;
