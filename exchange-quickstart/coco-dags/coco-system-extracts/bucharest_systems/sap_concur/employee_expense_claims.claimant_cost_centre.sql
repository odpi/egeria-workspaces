-- Extract: SAP Concur (Bucharest) -> Employee Expense Claims / claimant_cost_centre
-- Source: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Target: coco_data_hub.employee_expense_claims.claimant_cost_centre
-- Each claimant's default cost centre plus every cost centre they have allocated entries to, with the cost object
-- approver and the claimant's per-report limit.
WITH pairs AS (
  SELECT e.employee_id, e.org_unit_2 AS cost_centre FROM sap_concur.employee e
  WHERE EXISTS (SELECT 1 FROM sap_concur.report r WHERE r.employee_id = e.employee_id)
  UNION
  SELECT r.employee_id, a.custom1_cost_center FROM sap_concur.allocation a
  JOIN sap_concur.entry n ON n.entry_key = a.entry_key JOIN sap_concur.report r ON r.report_key = n.report_key
)
SELECT
  ('WP-' || upper(substr(md5('EKG:' || p.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  p.cost_centre::varchar(20) AS cost_centre_code,
  lower(split_part(ae.login_id, '@', 1))::varchar(40) AS claim_approver_identifier,
  e.custom20_expense_limit::numeric(18,2) AS claim_maximum_amount
FROM pairs p
JOIN sap_concur.employee e ON e.employee_id = p.employee_id
JOIN sap_concur.cost_object_approver c ON c.cost_object_code = p.cost_centre
JOIN sap_concur.employee ae ON ae.employee_id = c.approver_employee_id
