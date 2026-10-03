-- Extract: Oracle Order Management (Austin) -> Clinician Adverse Reaction Reports / clinician_reaction_report
-- Source: austin_systems.oracle_oms (SoftwareServer::AUS-SYS-011::SN-OMS-AU-20200310)
-- Target: coco_data_hub.clinician_adverse_reaction_reports.clinician_reaction_report
-- CLIN_ADV_RXN order holds joined to the order, its line (product, lot) and the PatientTherapy flexfield (patient
-- pseudonym, clinician NPI).
SELECT
  ('HOLD-' || x.hold_instance_id)::varchar(40) AS adverse_event_identifier,
  x.applied_date::date AS adverse_event_reported_date,
  e.attribute_char1::varchar(40) AS patient_pseudonym_identifier,
  e.attribute_char2::varchar(40) AS clinician_identifier,
  l.inventory_item_number::varchar(20) AS product_code,
  l.lot_number::varchar(40) AS batch_identifier,
  x.hold_comments AS adverse_event_description,
  lower(x.attribute1)::varchar(20) AS adverse_event_reported_severity
FROM oracle_oms.doo_hold_instances x
JOIN oracle_oms.doo_headers_all h ON h.header_id = x.header_id
JOIN oracle_oms.doo_lines_all l ON l.line_id = x.line_id
JOIN oracle_oms.doo_headers_eff_b e ON e.header_id = h.header_id AND e.context_code = 'PatientTherapy'
WHERE x.hold_code = 'CLIN_ADV_RXN'
