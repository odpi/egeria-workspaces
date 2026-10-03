-- Extract: Coco Expenses (Coco core) -> Employee Expense Claims / claim_line
-- Source: coco_pharma.coco_expenses (System::coco-expenses)
-- Target: coco_data_hub.employee_expense_claims.claim_line
-- expense_entry; expense types grouped into travel, hospitality, accommodation, other.
SELECT
  e.report_id::varchar(40)       AS claim_identifier,
  e.entry_no::integer            AS claim_line_number,
  (CASE WHEN e.expense_type IN ('AIRFARE', 'RAIL', 'TAXI', 'MILEAGE') THEN 'travel'
        WHEN e.expense_type IN ('MEALS', 'BUS_MEAL_HCP') THEN 'hospitality'
        WHEN e.expense_type = 'HOTEL' THEN 'accommodation' ELSE 'other' END)::varchar(40) AS claim_line_type,
  e.transaction_date             AS claim_line_date,
  e.amount::numeric(18,2)        AS claim_line_amount,
  e.description                  AS claim_line_description,
  e.attendee_hcp_id::varchar(40) AS claim_line_recipient_identifier,
  e.receipt_image_id::varchar(60) AS claim_line_evidence_identifier
FROM coco_expenses.expense_entry e
