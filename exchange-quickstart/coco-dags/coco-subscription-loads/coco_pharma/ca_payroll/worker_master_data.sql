-- Subscription: coco_ca_payroll__worker_master_data - Canadian payroll (Coco core) receives Worker Master Data
-- Destination: coco_pharma.ca_payroll (System::CA payroll)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Keeps the employees of Coco Pharmaceuticals Canada Inc. (COCO-CA): every record goes to the HR interface
-- hr_interface (NEW, dates as text YYYYMMDD in this installation's style), and employees already on the payroll
-- (employee_master, matched on the HRIM pseudonym) get their home cost centre refreshed.  Discards other Coco
-- legal entities (their own payrolls), contractors and Austin/EKG workers.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - not on a Coco payroll'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker SET discard_reason = 'not employed by Coco Pharmaceuticals Canada Inc. - paid by the ' || legal_entity_code || ' payroll'
 WHERE discard_reason IS NULL AND legal_entity_code <> 'COCO-CA';
UPDATE incoming_worker SET discard_reason = 'contractor - not paid through payroll'
 WHERE discard_reason IS NULL AND worker_type <> 'employee';

INSERT INTO ca_payroll.hr_interface (worker_ref, company_code, work_location, hire_date, term_date, emp_status)
SELECT w.worker_pseudonym_identifier, 'CPCA', w.site_code, to_char(w.worker_hire_date, 'YYYYMMDD'),
       to_char(w.worker_leave_date, 'YYYYMMDD'),
       (CASE w.worker_current_status WHEN 'left' THEN 'T' WHEN 'on leave' THEN 'L' ELSE 'A' END)
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL
ON CONFLICT (worker_ref) DO UPDATE SET work_location = EXCLUDED.work_location, hire_date = EXCLUDED.hire_date,
       term_date = EXCLUDED.term_date, emp_status = EXCLUDED.emp_status;

UPDATE incoming_worker_assignment a SET discard_reason = 'worker not on the Canadian payroll'
 WHERE NOT EXISTS (SELECT 1 FROM ca_payroll.hr_interface f WHERE f.worker_ref = a.worker_pseudonym_identifier);

UPDATE ca_payroll.hr_interface f
   SET job_code = a.role_code, job_title = a.role_name, home_cost_centre = a.cost_centre_code,
       supervisor_ref = a.manager_pseudonym_identifier
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = f.worker_ref;

UPDATE ca_payroll.employee_master e SET home_cost_centre = a.cost_centre_code
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = e.worker_ref
   AND e.home_cost_centre IS DISTINCT FROM a.cost_centre_code;
