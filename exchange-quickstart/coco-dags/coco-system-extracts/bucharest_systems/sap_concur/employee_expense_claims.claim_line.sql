-- Extract: SAP Concur (Bucharest) -> Employee Expense Claims / claim_line
-- Source: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Target: coco_data_hub.employee_expense_claims.claim_line
-- Entries numbered within their report; recipient = the healthcare professional attendee (first HCP), evidence =
-- receipt image.
SELECT
  r.report_id::varchar(40) AS claim_identifier,
  (row_number() OVER (PARTITION BY e.report_key ORDER BY e.entry_key))::integer AS claim_line_number,
  e.expense_type_name::varchar(40) AS claim_line_type,
  e.transaction_date AS claim_line_date,
  e.posted_amount::numeric(18,2) AS claim_line_amount,
  e.business_purpose AS claim_line_description,
  (SELECT a.external_id FROM sap_concur.attendee a WHERE a.entry_key = e.entry_key AND a.attendee_type_code = 'HCP'
   ORDER BY a.attendee_key LIMIT 1)::varchar(40) AS claim_line_recipient_identifier,
  e.receipt_image_id::varchar(60) AS claim_line_evidence_identifier
FROM sap_concur.entry e
JOIN sap_concur.report r ON r.report_key = e.report_key
WHERE r.submit_date IS NOT NULL
