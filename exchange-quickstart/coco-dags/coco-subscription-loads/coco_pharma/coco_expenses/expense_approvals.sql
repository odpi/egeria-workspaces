-- Subscription: coco_expenses__expense_approvals - Coco Expenses (Coco core) receives Expense Approvals
-- Destination: coco_pharma.coco_expenses (System::coco-expenses)
-- Why it subscribes: Employee Expense Claims depends on it (approval decision)
-- Keeps nothing: approvals of Coco claims are made in Coco Expenses itself (approval_history), so they come
-- back as rows it already holds; the rest are EKG's approvals of EKG claims, which Coco Expenses does not hold.

UPDATE incoming_expense_claim c SET discard_reason = 'Coco Expenses claim - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_expenses.expense_report r WHERE r.report_id = c.claim_identifier);
UPDATE incoming_expense_claim SET discard_reason = 'EKG claim - not approved through Coco Expenses'
 WHERE discard_reason IS NULL;

UPDATE incoming_approval_decision d SET discard_reason = 'Coco Expenses approval - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_expenses.approval_history h
                WHERE h.report_id = d.claim_identifier AND h.action_at = d.claim_approval_timestamp);
UPDATE incoming_approval_decision SET discard_reason = 'EKG approval - not a Coco Expenses claim'
 WHERE discard_reason IS NULL;
