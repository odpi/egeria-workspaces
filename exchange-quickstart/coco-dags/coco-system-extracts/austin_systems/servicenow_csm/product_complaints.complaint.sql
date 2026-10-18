-- Extract: ServiceNow Customer Service Management (Austin) -> Product Complaints / complaint
-- Source: austin_systems.servicenow_csm (SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601)
-- Target: coco_data_hub.product_complaints.complaint
-- sn_customerservice_case of category product_complaint; reporter choice values and case state translated.
SELECT
  c.number::varchar(40) AS complaint_identifier,
  c.opened_at AS complaint_received_timestamp,
  (CASE c.u_reporter_type WHEN 'hcp' THEN 'healthcare professional' ELSE c.u_reporter_type END)::varchar(100) AS complaint_reporter_type,
  c.u_product_code::varchar(20) AS product_code,
  c.u_lot_number::varchar(40) AS batch_identifier,
  c.u_serial_number::varchar(40) AS pack_serial_number,
  coalesce(c.description, c.short_description) AS complaint_description,
  (CASE WHEN c.state IN (3, 6, 7) THEN 'closed' WHEN c.u_investigation_required THEN 'under investigation'
        ELSE 'open' END)::varchar(20) AS complaint_current_status
FROM servicenow_csm.sn_customerservice_case c
WHERE c.category = 'product_complaint'
