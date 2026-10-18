-- Extract: ServiceNow Customer Service Management (Austin) -> Consolidated Safety Reports / safety_report
-- Source: austin_systems.servicenow_csm (SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601)
-- Target: coco_data_hub.consolidated_safety_reports.safety_report
-- Adverse event cases; a case opened from a complaint takes the complaint as its source, a direct call is its own
-- source.
SELECT
  c.number::varchar(40) AS safety_report_identifier,
  c.opened_at AS safety_report_received_timestamp,
  (CASE WHEN p.sys_id IS NOT NULL THEN 'complaint' WHEN c.u_reporter_type = 'hcp' THEN 'clinician' ELSE 'other' END)::varchar(20) AS safety_report_source_type,
  coalesce(p.number, c.number)::varchar(40) AS safety_report_source_identifier,
  NULL::varchar(40) AS patient_pseudonym_identifier,
  c.u_product_code::varchar(20) AS product_code,
  c.u_lot_number::varchar(40) AS batch_identifier,
  NULL::varchar(40) AS clinical_trial_identifier,
  coalesce(c.description, c.short_description) AS adverse_event_description,
  c.u_safety_case_ref::varchar(40) AS safety_case_identifier
FROM servicenow_csm.sn_customerservice_case c
LEFT JOIN servicenow_csm.sn_customerservice_case p ON p.sys_id = c.parent
WHERE c.category = 'adverse_event'
