-- Extract: Coco Expenses (Coco core) -> Expense Approvals / approval_decision
-- Source: coco_pharma.coco_expenses (System::coco-expenses)
-- Target: coco_data_hub.expense_approvals.approval_decision
-- approval_history; actions to status words.
SELECT
  h.report_id::varchar(40)       AS claim_identifier,
  h.action_at                    AS claim_approval_timestamp,
  h.actor_ref::varchar(40)       AS claim_approver_identifier,
  (CASE h.action WHEN 'APPROVE' THEN 'approved' WHEN 'REJECT' THEN 'rejected' ELSE 'returned' END)::varchar(20) AS claim_approval_status,
  h.comment                      AS claim_approval_notes
FROM coco_expenses.approval_history h
