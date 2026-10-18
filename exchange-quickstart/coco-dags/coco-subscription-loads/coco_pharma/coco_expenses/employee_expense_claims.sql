-- Subscription: coco_expenses__employee_expense_claims - Coco Expenses (Coco core) receives Employee Expense Claims
-- Destination: coco_pharma.coco_expenses (System::coco-expenses)
-- Why it subscribes: Expense Approvals depends on it (submit for approval)
-- Keeps nothing: Coco Expenses is itself the source of every Coco claim (its expense_report and expense_entry
-- rows), so those come back as rows it already holds; the other claims are EKG's (SAP Concur, WP- pseudonyms),
-- and EKG claimants are neither in Coco Expenses nor approved through it.

UPDATE incoming_claim_submission c SET discard_reason = 'Coco Expenses claim - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_expenses.expense_report r WHERE r.report_id = c.claim_identifier);
UPDATE incoming_claim_submission SET discard_reason = 'EKG claim - EKG claimants are not in Coco Expenses'
 WHERE discard_reason IS NULL;

UPDATE incoming_claim_line l SET discard_reason = 'Coco Expenses claim line - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_expenses.expense_entry e WHERE e.report_id = l.claim_identifier AND e.entry_no = l.claim_line_number);
UPDATE incoming_claim_line SET discard_reason = 'EKG claim line - EKG claimants are not in Coco Expenses'
 WHERE discard_reason IS NULL;

UPDATE incoming_claimant_cost_centre c SET discard_reason = 'Coco claimant cost centre - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_expenses.employee_cost_center e
                WHERE e.employee_ref = c.worker_pseudonym_identifier AND e.cost_center = c.cost_centre_code);
UPDATE incoming_claimant_cost_centre SET discard_reason = 'EKG claimant - not a Coco Expenses claimant'
 WHERE discard_reason IS NULL;
