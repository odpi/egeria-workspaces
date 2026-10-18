-- Extract: SAP Concur (Bucharest) -> Employee Expense Claims / claim_submission
-- Source: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Target: coco_data_hub.employee_expense_claims.claim_submission
-- Submitted reports; approval and payment status codes combined into the claim status.
SELECT
  r.report_id::varchar(40) AS claim_identifier,
  ('WP-' || upper(substr(md5('EKG:' || r.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  r.submit_date AS claim_submitted_timestamp,
  r.total_claimed_amount::numeric(18,2) AS claim_total_amount,
  r.currency_code::varchar(3) AS claim_currency_code,
  (CASE WHEN r.payment_status_code = 'P_PAID' THEN 'paid' WHEN r.approval_status_code = 'A_APPR' THEN 'approved'
        WHEN r.approval_status_code = 'A_RESU' THEN 'sent back' ELSE 'submitted' END)::varchar(20) AS claim_current_status
FROM sap_concur.report r
WHERE r.submit_date IS NOT NULL
