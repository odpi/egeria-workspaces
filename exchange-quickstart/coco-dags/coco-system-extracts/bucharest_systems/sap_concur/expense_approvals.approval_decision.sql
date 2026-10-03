-- Extract: SAP Concur (Bucharest) -> Expense Approvals / approval_decision
-- Source: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Target: coco_data_hub.expense_approvals.approval_decision
-- Workflow steps that have been actioned (approved or sent back), with the approver's Concur login.
SELECT
  r.report_id::varchar(40) AS claim_identifier,
  w.action_datetime AS claim_approval_timestamp,
  lower(split_part(ae.login_id, '@', 1))::varchar(40) AS claim_approver_identifier,
  (CASE w.status WHEN 'APPROVED' THEN 'approved' WHEN 'SENT_BACK' THEN 'sent back' ELSE 'rejected' END)::varchar(20) AS claim_approval_status,
  w.comment AS claim_approval_notes
FROM sap_concur.report_workflow w
JOIN sap_concur.report r ON r.report_key = w.report_key
JOIN sap_concur.employee ae ON ae.employee_id = w.approver_employee_id
WHERE w.action_datetime IS NOT NULL
