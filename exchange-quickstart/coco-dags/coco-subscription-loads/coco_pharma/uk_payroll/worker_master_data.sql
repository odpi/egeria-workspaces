-- Subscription: coco_uk_payroll__worker_master_data - UK payroll (Coco core) receives Worker Master Data
-- Destination: coco_pharma.uk_payroll (System::UK payroll)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Keeps the employees of Coco Pharmaceuticals UK Ltd (legal entity COCO-UK): every record goes to the HR
-- interface file hr_feed (NEW) for starters, leavers and transfers, and the default cost centre of employees
-- already on the payroll (pay_employee, matched on the HRIM pseudonym) is refreshed.  Discards other Coco
-- legal entities (their own payrolls), contractors (not paid through payroll) and Austin/EKG workers.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - not on a Coco payroll'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker SET discard_reason = 'not employed by Coco Pharmaceuticals UK Ltd - paid by the ' || legal_entity_code || ' payroll'
 WHERE discard_reason IS NULL AND legal_entity_code <> 'COCO-UK';
UPDATE incoming_worker SET discard_reason = 'contractor - not paid through payroll'
 WHERE discard_reason IS NULL AND worker_type <> 'employee';

INSERT INTO uk_payroll.hr_feed (worker_ref, company, site, start_date, leave_date, hr_status)
SELECT w.worker_pseudonym_identifier, w.legal_entity_code, w.site_code, w.worker_hire_date, w.worker_leave_date,
       upper(w.worker_current_status)
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL
ON CONFLICT (worker_ref) DO UPDATE SET company = EXCLUDED.company, site = EXCLUDED.site, start_date = EXCLUDED.start_date,
       leave_date = EXCLUDED.leave_date, hr_status = EXCLUDED.hr_status;

UPDATE incoming_worker_assignment a SET discard_reason = 'worker not on the UK payroll'
 WHERE NOT EXISTS (SELECT 1 FROM uk_payroll.hr_feed f WHERE f.worker_ref = a.worker_pseudonym_identifier);

UPDATE uk_payroll.hr_feed f
   SET job_code = a.role_code, job_title = a.role_name, cost_ctr = a.cost_centre_code, mgr_ref = a.manager_pseudonym_identifier
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = f.worker_ref;

UPDATE uk_payroll.pay_employee e SET cost_ctr = a.cost_centre_code
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = e.worker_ref
   AND e.cost_ctr IS DISTINCT FROM a.cost_centre_code;
