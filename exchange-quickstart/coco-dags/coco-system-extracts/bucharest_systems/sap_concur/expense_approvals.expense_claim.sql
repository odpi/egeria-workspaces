-- Extract: SAP Concur (Bucharest) -> Expense Approvals / expense_claim
-- Source: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Target: coco_data_hub.expense_approvals.expense_claim
-- Submitted reports with the claimant pseudonymised from the Workday employee ID, the G/L account of the report's
-- largest entry and the approver of the first workflow step (Concur login = e-mail local part).
SELECT
  r.report_id::varchar(40) AS claim_identifier,
  ('WP-' || upper(substr(md5('EKG:' || r.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  r.submit_date AS claim_submitted_timestamp,
  r.total_claimed_amount::numeric(18,2) AS claim_total_amount,
  r.currency_code::varchar(3) AS claim_currency_code,
  (SELECT e.journal_account_code FROM sap_concur.entry e WHERE e.report_key = r.report_key
   ORDER BY e.posted_amount DESC, e.entry_key LIMIT 1)::varchar(20) AS ledger_account_code,
  (SELECT lower(split_part(ae.login_id, '@', 1)) FROM sap_concur.report_workflow w
   JOIN sap_concur.employee ae ON ae.employee_id = w.approver_employee_id
   WHERE w.report_key = r.report_key AND w.step_sequence = 1)::varchar(40) AS claim_approver_identifier
FROM sap_concur.report r
WHERE r.submit_date IS NOT NULL
