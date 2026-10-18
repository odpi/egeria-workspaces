-- system-qualified-name: System::coco-ledgers
-- Coco Ledgers - Coco core.  SaaS general ledger for every Coco legal entity (receivables, payables, manual journals and balances); feeds Treatment Invoices (revenue recognition), Manual Journal Approvals, Supplier Payments and General Ledger Balances.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS coco_ledgers;
COMMENT ON SCHEMA coco_ledgers IS 'Coco Ledgers (Coco core): users, entities, accounts, journals, reviews, balances, receivables and payables.';

CREATE TABLE IF NOT EXISTS coco_ledgers.fm_user (
  user_email varchar(80) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  display_name varchar(80) NOT NULL,
  CONSTRAINT fm_user_pk PRIMARY KEY (user_email)
);
COMMENT ON TABLE coco_ledgers.fm_user IS 'Ledger users, with the HRIM worker pseudonym supplied by single sign-on.';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_entity (
  entity_id varchar(10) NOT NULL,
  entity_name varchar(80) NOT NULL,
  base_ccy varchar(3) NOT NULL,
  CONSTRAINT gl_entity_pk PRIMARY KEY (entity_id)
);
COMMENT ON TABLE coco_ledgers.gl_entity IS 'Legal entities kept in the ledger.';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_account (
  acct_no varchar(10) NOT NULL,
  acct_name varchar(80) NOT NULL,
  acct_type char(1) NOT NULL,
  CONSTRAINT gl_account_pk PRIMARY KEY (acct_no)
);
COMMENT ON TABLE coco_ledgers.gl_account IS 'Group chart of accounts (A asset, L liability, R revenue, E expense).';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_journal (
  je_id varchar(16) NOT NULL,
  entity_id varchar(10) NOT NULL,
  period_name varchar(6) NOT NULL,
  je_source varchar(4) NOT NULL,
  feed_batch_id varchar(20),
  description text NOT NULL,
  prepared_by varchar(80),
  submitted_at timestamptz NOT NULL,
  je_status varchar(10) NOT NULL,
  posted_at timestamptz,
  control_total numeric(16,2) NOT NULL,
  CONSTRAINT gl_journal_pk PRIMARY KEY (je_id)
);
COMMENT ON TABLE coco_ledgers.gl_journal IS 'Journal headers. period_name like ''Aug-26''; je_source AR, AP, PAY, FEED or MAN (manual); je_status PENDING, POSTED, REJECTED; control_total is the debit total entered at submission.';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_journal_line (
  je_id varchar(16) NOT NULL,
  line_no smallint NOT NULL,
  acct_no varchar(10) NOT NULL,
  dr_amt numeric(16,2) NOT NULL,
  cr_amt numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  cost_centre varchar(10),
  CONSTRAINT gl_journal_line_pk PRIMARY KEY (je_id, line_no)
);
COMMENT ON TABLE coco_ledgers.gl_journal_line IS 'Journal lines (debit and credit held separately).';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_je_review (
  je_id varchar(16) NOT NULL,
  action_at timestamptz NOT NULL,
  action_by varchar(80) NOT NULL,
  action varchar(8) NOT NULL,
  comments text,
  CONSTRAINT gl_je_review_pk PRIMARY KEY (je_id, action_at)
);
COMMENT ON TABLE coco_ledgers.gl_je_review IS 'Review actions on submitted journals: APPROVE, REJECT, RETURN.';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_period_balance (
  entity_id varchar(10) NOT NULL,
  period_name varchar(6) NOT NULL,
  acct_no varchar(10) NOT NULL,
  closing_balance numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  CONSTRAINT gl_period_balance_pk PRIMARY KEY (entity_id, period_name, acct_no)
);
COMMENT ON TABLE coco_ledgers.gl_period_balance IS 'Closing balances of closed periods (credit balances negative).';

CREATE TABLE IF NOT EXISTS coco_ledgers.ar_invoice (
  inv_no varchar(20) NOT NULL,
  entity_id varchar(10) NOT NULL,
  customer_no varchar(20) NOT NULL,
  order_ref varchar(20) NOT NULL,
  inv_date date NOT NULL,
  inv_amount numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  delivery_date date NOT NULL,
  rev_acct varchar(10) NOT NULL,
  rev_rec_date date NOT NULL,
  rev_amount numeric(16,2) NOT NULL,
  CONSTRAINT ar_invoice_pk PRIMARY KEY (inv_no)
);
COMMENT ON TABLE coco_ledgers.ar_invoice IS 'Receivable invoices received from the ordering system with their revenue recognition.';

CREATE TABLE IF NOT EXISTS coco_ledgers.ap_invoice (
  vendor_no integer NOT NULL,
  vendor_inv_no varchar(30) NOT NULL,
  po_no varchar(20) NOT NULL,
  grn_ref varchar(20),
  inv_amount numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  match_status char(1) NOT NULL,
  entity_id varchar(10) NOT NULL,
  CONSTRAINT ap_invoice_pk PRIMARY KEY (vendor_no, vendor_inv_no)
);
COMMENT ON TABLE coco_ledgers.ap_invoice IS 'Supplier invoices and their three-way match: M matched, V price/quantity variance, U unmatched.';

CREATE TABLE IF NOT EXISTS coco_ledgers.ap_payment (
  pay_id varchar(16) NOT NULL,
  vendor_no integer NOT NULL,
  vendor_inv_no varchar(30) NOT NULL,
  pay_amount numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  approved_by varchar(80) NOT NULL,
  approved_at timestamptz NOT NULL,
  vendor_screen_status varchar(3) NOT NULL,
  payee_acct_masked varchar(30) NOT NULL,
  gl_acct varchar(10) NOT NULL,
  CONSTRAINT ap_payment_pk PRIMARY KEY (pay_id)
);
COMMENT ON TABLE coco_ledgers.ap_payment IS 'Payments authorised and sent to the bank, with the vendor screening status (CLR, REV, BLK) and payee account read at authorisation.';

INSERT INTO coco_ledgers.fm_user (user_email, worker_ref, display_name) VALUES
('ReggieMint@Coco-Pharmaceuticals.org', 'CW-T8FK9X', 'Reggie Mint'),
('TomTally@Coco-Pharmaceuticals.org', 'CW-EZMUNR', 'Tom Tally'),
('SallyCounter@Coco-Pharmaceuticals.org', 'CW-GMCZHC', 'Sally Counter'),
('SidneySeeker@Coco-Pharmaceuticals.org', 'CW-KDVCEA', 'Sidney Seeker'),
('FaithBroker@Coco-Pharmaceuticals.org', 'CW-TC93US', 'Faith Broker')
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.gl_entity (entity_id, entity_name, base_ccy) VALUES
('COCO-US', 'Coco Pharmaceuticals Inc.', 'USD'),
('COCO-UK', 'Coco Pharmaceuticals UK Ltd', 'GBP'),
('COCO-NL', 'Coco Pharmaceuticals B.V.', 'EUR'),
('COCO-CA', 'Coco Pharmaceuticals Canada Inc.', 'CAD')
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.gl_account (acct_no, acct_name, acct_type) VALUES
('1000', 'Cash at bank', 'A'),
('1100', 'Trade receivables', 'A'),
('1400', 'Inventory', 'A'),
('2100', 'Trade payables', 'L'),
('2300', 'Accruals', 'L'),
('4000', 'Revenue - products', 'R'),
('4100', 'Revenue - personalised therapies', 'R'),
('5000', 'Cost of goods sold', 'E'),
('6100', 'Salaries and wages', 'E'),
('6200', 'Travel and expenses', 'E'),
('6210', 'Hospitality', 'E'),
('6300', 'Utilities', 'E'),
('6400', 'Fleet and fuel', 'E'),
('6900', 'Intercompany recharges', 'E')
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.gl_journal (je_id, entity_id, period_name, je_source, feed_batch_id, description, prepared_by, submitted_at, je_status, posted_at, control_total) VALUES
('JE-26-AR001', 'COCO-US', 'Jun-26', 'AR', 'CRM-FEED-20260610', 'Invoice INV-26-004417 order SO-26-01102', NULL, '2026-06-10 22:00+00', 'POSTED', '2026-06-10 22:05+00', 373000.0),
('JE-26-AR002', 'COCO-US', 'Jul-26', 'AR', 'CRM-FEED-20260701', 'Invoice INV-26-004562 order SO-26-01127', NULL, '2026-07-01 22:00+00', 'POSTED', '2026-07-01 22:05+00', 373000.0),
('JE-26-AR003', 'COCO-US', 'Jul-26', 'AR', 'CRM-FEED-20260723', 'Invoice INV-26-004698 order SO-26-01145', NULL, '2026-07-23 22:00+00', 'POSTED', '2026-07-23 22:05+00', 373000.0),
('JE-26-AR004', 'COCO-US', 'Aug-26', 'AR', 'CRM-FEED-20260820', 'Invoice INV-26-004901 order SO-26-01163', NULL, '2026-08-20 22:00+00', 'POSTED', '2026-08-20 22:05+00', 373000.0),
('JE-26-08812', 'COCO-UK', 'Aug-26', 'MAN', NULL, 'Accrual for Winchester solvent disposal', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-02 10:12+00', 'POSTED', '2026-09-02 15:00+00', 12400.0),
('JE-26-08840', 'COCO-US', 'Aug-26', 'MAN', NULL, 'Reclassify Cocolecel revenue booked to product revenue in Q2', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-03 09:40+00', 'POSTED', '2026-09-03 16:20+00', 746000.0),
('JE-26-08857', 'COCO-UK', 'Aug-26', 'MAN', NULL, 'Write down obsolete blister foil lot GML-FOIL-2605', 'SallyCounter@Coco-Pharmaceuticals.org', '2026-09-03 11:05+00', 'POSTED', '2026-09-05 14:10+00', 64300.0),
('JE-26-08863', 'COCO-NL', 'Aug-26', 'MAN', NULL, 'Intercompany recharge of Amsterdam IT services to Coco Pharmaceuticals UK', 'FaithBroker@Coco-Pharmaceuticals.org', '2026-09-04 08:15+00', 'POSTED', '2026-09-04 17:45+00', 185000.0),
('JE-26-09102', 'COCO-CA', 'Sep-26', 'MAN', NULL, 'Provision for rework after tablet press calibration lapse (E26-4010-0011)', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-28 13:00+00', 'PENDING', NULL, 58000.0),
('JE-26-09118', 'COCO-US', 'Sep-26', 'MAN', NULL, 'Year-to-date bonus accrual true-up', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-25 10:30+00', 'REJECTED', NULL, 420000.0),
('JE-26-09131', 'COCO-UK', 'Sep-26', 'MAN', NULL, 'Release of accrual for Worldwide Fleet Supplies invoice', 'SallyCounter@Coco-Pharmaceuticals.org', '2026-09-11 16:40+00', 'POSTED', '2026-09-11 17:02+00', 97500.0),
('JE-26-PY0805', 'COCO-UK', 'Aug-26', 'FEED', 'UK26M05', 'Feed UK26M05', NULL, '2026-08-28 20:00+00', 'POSTED', '2026-08-28 20:10+00', 106036.23),
('JE-26-PY0806', 'COCO-NL', 'Aug-26', 'FEED', 'VR-202608', 'Feed VR-202608', NULL, '2026-08-28 20:00+00', 'POSTED', '2026-08-28 20:10+00', 54320.99),
('JE-26-EX0901', 'COCO-UK', 'Sep-26', 'FEED', 'EXP-2609-01', 'Feed EXP-2609-01', NULL, '2026-09-28 20:00+00', 'POSTED', '2026-09-28 20:10+00', 1846.2),
('JE-26-AP001', 'COCO-UK', 'Sep-26', 'PAY', 'PAYRUN-20260904', 'Payment PAY-26-03311 to vendor 1000', NULL, '2026-09-04 10:00+00', 'POSTED', '2026-09-04 10:00+00', 18750.0),
('JE-26-AP002', 'COCO-UK', 'Sep-26', 'PAY', 'PAYRUN-20260918', 'Payment PAY-26-03318 to vendor 9000', NULL, '2026-09-18 10:00+00', 'POSTED', '2026-09-18 10:00+00', 2625.0),
('JE-26-AP003', 'COCO-CA', 'Sep-26', 'PAY', 'PAYRUN-20260909', 'Payment PAY-26-03324 to vendor 3000', NULL, '2026-09-09 10:00+00', 'POSTED', '2026-09-09 10:00+00', 41250.0)
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.gl_journal_line (je_id, line_no, acct_no, dr_amt, cr_amt, ccy, cost_centre) VALUES
('JE-26-AR001', 1, '1100', 373000.0, 0, 'USD', NULL),
('JE-26-AR001', 2, '4100', 0, 373000.0, 'USD', NULL),
('JE-26-AR002', 1, '1100', 373000.0, 0, 'USD', NULL),
('JE-26-AR002', 2, '4100', 0, 373000.0, 'USD', NULL),
('JE-26-AR003', 1, '1100', 373000.0, 0, 'USD', NULL),
('JE-26-AR003', 2, '4100', 0, 373000.0, 'USD', NULL),
('JE-26-AR004', 1, '1100', 373000.0, 0, 'USD', NULL),
('JE-26-AR004', 2, '4100', 0, 373000.0, 'USD', NULL),
('JE-26-08812', 1, '6900', 12400.0, 0, 'GBP', NULL),
('JE-26-08812', 2, '2300', 0, 12400.0, 'GBP', NULL),
('JE-26-08840', 1, '4000', 746000.0, 0, 'USD', NULL),
('JE-26-08840', 2, '4100', 0, 746000.0, 'USD', NULL),
('JE-26-08857', 1, '5000', 64300.0, 0, 'GBP', NULL),
('JE-26-08857', 2, '1400', 0, 64300.0, 'GBP', NULL),
('JE-26-08863', 1, '1100', 185000.0, 0, 'EUR', NULL),
('JE-26-08863', 2, '6900', 0, 185000.0, 'EUR', NULL),
('JE-26-09131', 1, '2300', 97500.0, 0, 'GBP', NULL),
('JE-26-09131', 2, '2100', 0, 97500.0, 'GBP', NULL),
('JE-26-PY0805', 1, '6100', 106036.23, 0, 'GBP', NULL),
('JE-26-PY0805', 2, '1000', 0, 106036.23, 'GBP', NULL),
('JE-26-PY0806', 1, '6200', 54320.99, 0, 'EUR', NULL),
('JE-26-PY0806', 2, '1000', 0, 54320.99, 'EUR', NULL),
('JE-26-EX0901', 1, '6200', 1846.2, 0, 'GBP', NULL),
('JE-26-EX0901', 2, '1000', 0, 1846.2, 'GBP', NULL),
('JE-26-AP001', 1, '2100', 18750.0, 0, 'GBP', NULL),
('JE-26-AP001', 2, '1000', 0, 18750.0, 'GBP', NULL),
('JE-26-AP002', 1, '2100', 2625.0, 0, 'USD', NULL),
('JE-26-AP002', 2, '1000', 0, 2625.0, 'USD', NULL),
('JE-26-AP003', 1, '2100', 41250.0, 0, 'EUR', NULL),
('JE-26-AP003', 2, '1000', 0, 41250.0, 'EUR', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.gl_je_review (je_id, action_at, action_by, action, comments) VALUES
('JE-26-08812', '2026-09-02 15:00+00', 'ReggieMint@Coco-Pharmaceuticals.org', 'APPROVE', NULL),
('JE-26-08840', '2026-09-03 16:20+00', 'ReggieMint@Coco-Pharmaceuticals.org', 'APPROVE', 'Agreed to CRM invoices INV-26-004417 and INV-26-004562.'),
('JE-26-08857', '2026-09-04 09:30+00', 'TomTally@Coco-Pharmaceuticals.org', 'RETURN', 'Attach the stock count and the QA rejection.'),
('JE-26-08857', '2026-09-05 14:10+00', 'TomTally@Coco-Pharmaceuticals.org', 'APPROVE', 'Evidence attached.'),
('JE-26-08863', '2026-09-04 17:45+00', 'ReggieMint@Coco-Pharmaceuticals.org', 'APPROVE', NULL),
('JE-26-09118', '2026-09-26 11:00+00', 'ReggieMint@Coco-Pharmaceuticals.org', 'REJECT', 'No calculation supporting the true-up; resubmit with the HR bonus schedule.'),
('JE-26-09131', '2026-09-11 17:02+00', 'TomTally@Coco-Pharmaceuticals.org', 'APPROVE', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.gl_period_balance (entity_id, period_name, acct_no, closing_balance, ccy) VALUES
('COCO-US', 'Jul-26', '1000', 5200300.0, 'USD'),
('COCO-US', 'Jul-26', '1100', 2400330.0, 'USD'),
('COCO-US', 'Jul-26', '2100', -1349370.0, 'USD'),
('COCO-US', 'Jul-26', '4000', -2899770.0, 'USD'),
('COCO-US', 'Jul-26', '6100', 610860.0, 'USD'),
('COCO-US', 'Jul-26', '6200', 48890.0, 'USD'),
('COCO-US', 'Jul-26', '4100', -746000.0, 'USD'),
('COCO-US', 'Aug-26', '1000', 5382300.0, 'USD'),
('COCO-US', 'Aug-26', '1100', 2484330.0, 'USD'),
('COCO-US', 'Aug-26', '2100', -1396620.0, 'USD'),
('COCO-US', 'Aug-26', '4000', -3001270.0, 'USD'),
('COCO-US', 'Aug-26', '6100', 632210.0, 'USD'),
('COCO-US', 'Aug-26', '6200', 50570.0, 'USD'),
('COCO-US', 'Aug-26', '4100', -1119000.0, 'USD'),
('COCO-UK', 'Jul-26', '1000', 3224300.0, 'GBP'),
('COCO-UK', 'Jul-26', '1100', 1488330.0, 'GBP'),
('COCO-UK', 'Jul-26', '2100', -836370.0, 'GBP'),
('COCO-UK', 'Jul-26', '4000', -1797770.0, 'GBP'),
('COCO-UK', 'Jul-26', '6100', 379060.0, 'GBP'),
('COCO-UK', 'Jul-26', '6200', 30650.0, 'GBP'),
('COCO-UK', 'Aug-26', '1000', 3337140.0, 'GBP'),
('COCO-UK', 'Aug-26', '1100', 1540410.0, 'GBP'),
('COCO-UK', 'Aug-26', '2100', -865665.0, 'GBP'),
('COCO-UK', 'Aug-26', '4000', -1860700.0, 'GBP'),
('COCO-UK', 'Aug-26', '6100', 392297.0, 'GBP'),
('COCO-UK', 'Aug-26', '6200', 31691.6, 'GBP'),
('COCO-NL', 'Jul-26', '1000', 2132300.0, 'EUR'),
('COCO-NL', 'Jul-26', '1100', 984330.0, 'EUR'),
('COCO-NL', 'Jul-26', '2100', -552870.0, 'EUR'),
('COCO-NL', 'Jul-26', '4000', -1188770.0, 'EUR'),
('COCO-NL', 'Jul-26', '6100', 250960.0, 'EUR'),
('COCO-NL', 'Jul-26', '6200', 20570.0, 'EUR'),
('COCO-NL', 'Aug-26', '1000', 2206920.0, 'EUR'),
('COCO-NL', 'Aug-26', '1100', 1018770.0, 'EUR'),
('COCO-NL', 'Aug-26', '2100', -572242.5, 'EUR'),
('COCO-NL', 'Aug-26', '4000', -1230385.0, 'EUR'),
('COCO-NL', 'Aug-26', '6100', 259713.5, 'EUR'),
('COCO-NL', 'Aug-26', '6200', 21258.8, 'EUR'),
('COCO-CA', 'Jul-26', '1000', 1456300.0, 'CAD'),
('COCO-CA', 'Jul-26', '1100', 672330.0, 'CAD'),
('COCO-CA', 'Jul-26', '2100', -377370.0, 'CAD'),
('COCO-CA', 'Jul-26', '4000', -811770.0, 'CAD'),
('COCO-CA', 'Jul-26', '6100', 171660.0, 'CAD'),
('COCO-CA', 'Jul-26', '6200', 14330.0, 'CAD'),
('COCO-CA', 'Aug-26', '1000', 1507260.0, 'CAD'),
('COCO-CA', 'Aug-26', '1100', 695850.0, 'CAD'),
('COCO-CA', 'Aug-26', '2100', -390600.0, 'CAD'),
('COCO-CA', 'Aug-26', '4000', -840190.0, 'CAD'),
('COCO-CA', 'Aug-26', '6100', 177638.0, 'CAD'),
('COCO-CA', 'Aug-26', '6200', 14800.4, 'CAD')
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.ar_invoice (inv_no, entity_id, customer_no, order_ref, inv_date, inv_amount, ccy, delivery_date, rev_acct, rev_rec_date, rev_amount) VALUES
('INV-26-004417', 'COCO-US', 'HAMPH', 'SO-26-01102', '2026-06-10', 373000.0, 'USD', '2026-06-09', '4100', '2026-06-09', 373000.0),
('INV-26-004562', 'COCO-US', 'BOWAH', 'SO-26-01127', '2026-07-01', 373000.0, 'USD', '2026-06-30', '4100', '2026-06-30', 373000.0),
('INV-26-004698', 'COCO-US', 'OAKDH', 'SO-26-01145', '2026-07-23', 373000.0, 'USD', '2026-07-22', '4100', '2026-07-22', 373000.0),
('INV-26-004901', 'COCO-US', 'HAMPH', 'SO-26-01163', '2026-08-20', 373000.0, 'USD', '2026-08-19', '4100', '2026-08-19', 373000.0)
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.ap_invoice (vendor_no, vendor_inv_no, po_no, grn_ref, inv_amount, ccy, match_status, entity_id) VALUES
(1000, 'GML-INV-88213', 'PO-AMS-26-0371', 'WDR-260805/1', 18750.0, 'GBP', 'M', 'COCO-UK'),
(9000, 'WWE-2608-1177', 'PO-AMS-26-0380', 'WDR-260819/1', 2625.0, 'USD', 'M', 'COCO-UK'),
(3000, 'GG/26/0412', 'PO-AMS-26-0373', 'ED-GR-26-0079', 41250.0, 'EUR', 'M', 'COCO-CA'),
(7000, 'BASE-RE-2609-044', 'PO-AMS-26-0402', 'WDR-260916/1', 36400.0, 'EUR', 'V', 'COCO-UK'),
(2000, 'TT-77120', 'PO-AUS-26-0240', 'AUS-RCV-26-0402', 52000.0, 'USD', 'M', 'COCO-US'),
(2000, 'TT-77341', 'PO-AUS-26-0251', 'AUS-RCV-26-0431', 39000.0, 'USD', 'M', 'COCO-US'),
(4000, '4000-INV-2609-17', 'PO-KC-26-0088', NULL, 97500.0, 'USD', 'U', 'COCO-US'),
(6000, 'SGE-26-08-5521', 'PO-UK-26-0012', NULL, 14380.4, 'GBP', 'M', 'COCO-UK'),
(6002, 'AE-2608-99120', 'PO-AUS-26-0007', NULL, 22915.77, 'USD', 'M', 'COCO-US'),
(6001, 'NLE-0826-3301', 'PO-NL-26-0004', NULL, 9882.1, 'EUR', 'M', 'COCO-NL')
ON CONFLICT DO NOTHING;

INSERT INTO coco_ledgers.ap_payment (pay_id, vendor_no, vendor_inv_no, pay_amount, ccy, approved_by, approved_at, vendor_screen_status, payee_acct_masked, gl_acct) VALUES
('PAY-26-03311', 1000, 'GML-INV-88213', 18750.0, 'GBP', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-04 10:00+00', 'CLR', 'GB33BUKB****2201', '1400'),
('PAY-26-03318', 9000, 'WWE-2608-1177', 2625.0, 'USD', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-18 10:00+00', 'CLR', 'IN-****6620', '1400'),
('PAY-26-03324', 3000, 'GG/26/0412', 41250.0, 'EUR', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-09 10:00+00', 'CLR', 'NL91ABNA****7732', '1400'),
('PAY-26-03329', 2000, 'TT-77120', 52000.0, 'USD', 'TomTally@Coco-Pharmaceuticals.org', '2026-09-22 10:00+00', 'CLR', 'US-****4471', '1400'),
('PAY-26-03337', 4000, '4000-INV-2609-17', 97500.0, 'USD', 'SallyCounter@Coco-Pharmaceuticals.org', '2026-09-12 07:48+00', 'REV', 'MT84MALT****3050', '6400'),
('PAY-26-03340', 6000, 'SGE-26-08-5521', 14380.4, 'GBP', 'SallyCounter@Coco-Pharmaceuticals.org', '2026-09-15 10:00+00', 'CLR', 'GB82LOYD****5521', '6300'),
('PAY-26-03342', 6002, 'AE-2608-99120', 22915.77, 'USD', 'SallyCounter@Coco-Pharmaceuticals.org', '2026-09-15 10:05+00', 'CLR', 'US-****7263', '6300'),
('PAY-26-03345', 6001, 'NLE-0826-3301', 9882.1, 'EUR', 'SallyCounter@Coco-Pharmaceuticals.org', '2026-09-15 10:10+00', 'CLR', 'NL02RABO****4410', '6300')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS coco_ledgers.ap_vendor (
  vendor_no integer NOT NULL,
  vendor_name varchar(200) NOT NULL,
  vendor_type varchar(40) NOT NULL,
  country varchar(60) NOT NULL,
  approved_yn char(1) NOT NULL,
  approved_on date,
  vendor_status varchar(20) NOT NULL,
  screen_status varchar(3),
  screened_on date,
  risk_rating varchar(20),
  screen_ref varchar(40),
  anomaly_ref varchar(40),
  payee_acct_masked varchar(40),
  payee_bank varchar(120),
  payee_bank_country varchar(60),
  bank_change_ref varchar(40),
  bank_verified_on date,
  CONSTRAINT ap_vendor_pk PRIMARY KEY (vendor_no)
);
COMMENT ON TABLE coco_ledgers.ap_vendor IS 'Payables vendor master maintained from Supplier Master Data: status, screening status (CLR, REV, BLK) and the verified payee account that ap_payment reads at authorisation.';

CREATE TABLE IF NOT EXISTS coco_ledgers.ap_po (
  po_no varchar(40) NOT NULL,
  vendor_no integer NOT NULL,
  po_date date NOT NULL,
  po_amount numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  approved_by varchar(40) NOT NULL,
  po_status varchar(20) NOT NULL,
  CONSTRAINT ap_po_pk PRIMARY KEY (po_no)
);
COMMENT ON TABLE coco_ledgers.ap_po IS 'Purchase orders received from Purchase Orders And Receipts, the first leg of the three-way match of ap_invoice.';

CREATE TABLE IF NOT EXISTS coco_ledgers.ap_po_receipt (
  grn_ref varchar(40) NOT NULL,
  po_no varchar(40) NOT NULL,
  line_no smallint NOT NULL,
  rcv_date date NOT NULL,
  rcv_qty integer NOT NULL,
  CONSTRAINT ap_po_receipt_pk PRIMARY KEY (grn_ref, po_no, line_no)
);
COMMENT ON TABLE coco_ledgers.ap_po_receipt IS 'Goods receipt confirmations against purchase orders, the second leg of the three-way match.';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_feed_batch (
  feed_batch_id varchar(40) NOT NULL,
  source_sys varchar(60) NOT NULL,
  period_name varchar(6) NOT NULL,
  posted_at timestamptz NOT NULL,
  line_count integer NOT NULL,
  control_total numeric(16,2) NOT NULL,
  feed_status varchar(20) NOT NULL,
  CONSTRAINT gl_feed_batch_pk PRIMARY KEY (feed_batch_id)
);
COMMENT ON TABLE coco_ledgers.gl_feed_batch IS 'Subledger feed batches received from Subledger Postings, waiting for the journal import that creates FEED journals.';

CREATE TABLE IF NOT EXISTS coco_ledgers.gl_interface (
  feed_batch_id varchar(40) NOT NULL,
  line_no integer NOT NULL,
  entity_id varchar(10) NOT NULL,
  acct_no varchar(20) NOT NULL,
  txn_ref varchar(40) NOT NULL,
  amount numeric(16,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  CONSTRAINT gl_interface_pk PRIMARY KEY (feed_batch_id, line_no)
);
COMMENT ON TABLE coco_ledgers.gl_interface IS 'Journal import interface: subledger posting lines for Coco legal entities (signed amount, debit positive) waiting to be imported as FEED journals.';

CREATE TABLE IF NOT EXISTS coco_ledgers.ar_fulfilment (
  order_ref varchar(40) NOT NULL,
  batch_no varchar(40) NOT NULL,
  event_typ varchar(12) NOT NULL,
  event_at timestamptz NOT NULL,
  event_loc varchar(120),
  CONSTRAINT ar_fulfilment_pk PRIMARY KEY (order_ref, batch_no, event_typ)
);
COMMENT ON TABLE coco_ledgers.ar_fulfilment IS 'Fulfilment confirmations of personalised therapy orders (DELIVERED, ADMINISTERED) from Therapy Delivery Events, which release the receivable invoice and fix the delivery date for revenue recognition.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA coco_ledgers TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA coco_ledgers TO egeria_user, airflow_user;
