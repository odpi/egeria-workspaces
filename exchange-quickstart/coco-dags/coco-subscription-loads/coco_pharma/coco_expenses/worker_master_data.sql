-- Subscription: coco_expenses__worker_master_data - Coco Expenses (Coco core) receives Worker Master Data
-- Destination: coco_pharma.coco_expenses (System::coco-expenses)
-- Why it subscribes: Employee Expense Claims (expense access) and Expense Approvals (approver, cost centre) depend on it
-- Keeps every Coco worker (CW- pseudonyms, employees and contractors): the record goes to the employee import
-- feed employee_import (NEW, reimbursement currency from the legal entity), and existing claimant profiles
-- (employee_profile) get their default cost centre, approver (the line manager) and active flag refreshed.
-- Discards Austin/EKG workers, who claim in their own expense systems.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - claims in its own estate''s expense system'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';

INSERT INTO coco_expenses.employee_import (employee_ref, legal_entity, work_site, employee_type, hire_date, termination_date,
       employment_status, reimbursement_currency)
SELECT w.worker_pseudonym_identifier, w.legal_entity_code, w.site_code, w.worker_type, w.worker_hire_date, w.worker_leave_date,
       w.worker_current_status,
       (CASE w.legal_entity_code WHEN 'COCO-UK' THEN 'GBP' WHEN 'COCO-NL' THEN 'EUR' WHEN 'COCO-CA' THEN 'CAD' ELSE 'USD' END)
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL
ON CONFLICT (employee_ref) DO UPDATE SET legal_entity = EXCLUDED.legal_entity, work_site = EXCLUDED.work_site,
       employee_type = EXCLUDED.employee_type, hire_date = EXCLUDED.hire_date, termination_date = EXCLUDED.termination_date,
       employment_status = EXCLUDED.employment_status, reimbursement_currency = EXCLUDED.reimbursement_currency;

UPDATE coco_expenses.employee_profile p SET active = (CASE WHEN w.worker_current_status = 'left' THEN 'N' ELSE 'Y' END)
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL AND w.worker_pseudonym_identifier = p.employee_ref
   AND p.active IS DISTINCT FROM (CASE WHEN w.worker_current_status = 'left' THEN 'N' ELSE 'Y' END);

UPDATE incoming_worker_assignment a SET discard_reason = 'not a Coco worker known to Coco Expenses'
 WHERE NOT EXISTS (SELECT 1 FROM coco_expenses.employee_import i WHERE i.employee_ref = a.worker_pseudonym_identifier);

UPDATE coco_expenses.employee_import i
   SET job_title = a.role_name, cost_center = a.cost_centre_code, approver_ref = a.manager_pseudonym_identifier
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = i.employee_ref;

UPDATE coco_expenses.employee_profile p
   SET default_cost_center = a.cost_centre_code, approver_ref = coalesce(a.manager_pseudonym_identifier, p.approver_ref)
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = p.employee_ref
   AND (p.default_cost_center, p.approver_ref) IS DISTINCT FROM (a.cost_centre_code, coalesce(a.manager_pseudonym_identifier, p.approver_ref));
