-- Extract: LIMS LabWare Enterprise (Bucharest) -> Laboratory Test Results / test_result
-- Source: bucharest_systems.labware_lims (SoftwareServer::SYS-004::LIMS LabWare Enterprise)
-- Target: coco_data_hub.laboratory_test_results.test_result
-- Approved results on laboratory samples joined to product_spec for the limits; in_spec T/F to boolean; identifier
-- prefixed LW-.
SELECT
  ('LW-' || r.result_number)::varchar(40) AS test_result_identifier,
  s.text_id::varchar(40) AS sample_identifier,
  r.analysis::varchar(40) AS test_code,
  r.formatted_entry::varchar(60) AS test_value,
  r.units::varchar(20) AS test_unit,
  ps.min_value::varchar(60) AS specification_minimum_value,
  ps.max_value::varchar(60) AS specification_maximum_value,
  (r.in_spec = 'T') AS test_conformity_flag,
  r.entered_on AS test_completed_timestamp,
  r.entered_by::varchar(40) AS test_analyst_identifier
FROM labware_lims.result r
JOIN labware_lims.sample s ON s.sample_number = r.sample_number
LEFT JOIN labware_lims.product_spec ps ON ps.product = s.product AND ps.analysis = r.analysis AND ps.component = r.name
WHERE s.sample_type <> 'SUPPLIER_COA' AND r.status = 'A'
