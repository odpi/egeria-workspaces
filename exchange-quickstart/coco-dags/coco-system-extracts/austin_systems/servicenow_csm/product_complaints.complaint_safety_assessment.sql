-- Extract: ServiceNow Customer Service Management (Austin) -> Product Complaints / complaint_safety_assessment
-- Source: austin_systems.servicenow_csm (SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601)
-- Target: coco_data_hub.product_complaints.complaint_safety_assessment
-- Assessed complaint cases joined to the assessor and to any child adverse event case (the safety report).
SELECT
  c.number::varchar(40) AS complaint_identifier,
  c.u_safety_flag AS complaint_safety_flag,
  u.user_name::varchar(40) AS complaint_assessor_identifier,
  c.u_safety_assessed_at AS complaint_assessment_timestamp,
  ae.number::varchar(40) AS safety_report_identifier
FROM servicenow_csm.sn_customerservice_case c
JOIN servicenow_csm.sys_user u ON u.sys_id = c.u_safety_assessed_by
LEFT JOIN servicenow_csm.sn_customerservice_case ae ON ae.parent = c.sys_id AND ae.category = 'adverse_event'
WHERE c.category = 'product_complaint' AND c.u_safety_assessed_at IS NOT NULL
