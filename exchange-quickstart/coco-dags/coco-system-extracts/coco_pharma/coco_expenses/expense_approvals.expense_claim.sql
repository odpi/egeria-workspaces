-- Extract: Coco Expenses (Coco core) -> Expense Approvals / expense_claim
-- Source: coco_pharma.coco_expenses (System::coco-expenses)
-- Target: coco_data_hub.expense_approvals.expense_claim
-- expense_report rows that have been submitted for approval.
SELECT
  r.report_id::varchar(40)       AS claim_identifier,
  r.employee_ref::varchar(40)    AS worker_pseudonym_identifier,
  r.submitted_at                 AS claim_submitted_timestamp,
  r.report_total::numeric(18,2)  AS claim_total_amount,
  r.currency::varchar(3)         AS claim_currency_code,
  r.gl_account::varchar(20)      AS ledger_account_code,
  r.approver_ref::varchar(40)    AS claim_approver_identifier
FROM coco_expenses.expense_report r
WHERE r.submitted_at IS NOT NULL
