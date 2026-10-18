-- Extract: Coco Expenses (Coco core) -> Employee Expense Claims / claim_submission
-- Source: coco_pharma.coco_expenses (System::coco-expenses)
-- Target: coco_data_hub.employee_expense_claims.claim_submission
-- expense_report; drafts carry their creation time, SENT_BACK counted as draft again.
SELECT
  r.report_id::varchar(40)       AS claim_identifier,
  r.employee_ref::varchar(40)    AS worker_pseudonym_identifier,
  coalesce(r.submitted_at, r.created_at) AS claim_submitted_timestamp,
  r.report_total::numeric(18,2)  AS claim_total_amount,
  r.currency::varchar(3)         AS claim_currency_code,
  (CASE r.status WHEN 'DRAFT' THEN 'draft' WHEN 'SENT_BACK' THEN 'draft' WHEN 'SUBMITTED' THEN 'submitted'
                 WHEN 'APPROVED' THEN 'approved' WHEN 'PAID' THEN 'paid' ELSE 'rejected' END)::varchar(20) AS claim_current_status
FROM coco_expenses.expense_report r
