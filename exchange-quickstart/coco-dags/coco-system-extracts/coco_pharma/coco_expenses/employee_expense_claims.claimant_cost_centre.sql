-- Extract: Coco Expenses (Coco core) -> Employee Expense Claims / claimant_cost_centre
-- Source: coco_pharma.coco_expenses (System::coco-expenses)
-- Target: coco_data_hub.employee_expense_claims.claimant_cost_centre
-- employee_cost_center as is.
SELECT
  c.employee_ref::varchar(40)    AS worker_pseudonym_identifier,
  c.cost_center::varchar(20)     AS cost_centre_code,
  c.approver_ref::varchar(40)    AS claim_approver_identifier,
  c.spend_limit::numeric(18,2)   AS claim_maximum_amount
FROM coco_expenses.employee_cost_center c
