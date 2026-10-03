-- Extract: Empower Chromatography (Bucharest) -> Laboratory Test Results / test_result
-- Source: bucharest_systems.empower_cds (SoftwareServer::SYS-027::Empower Chromatography)
-- Target: coco_data_hub.laboratory_test_results.test_result
-- Signed-off results joined to injection (sample name = LIMS sample ID); identifier prefixed EMP-; Pass/Fail to
-- boolean; analyst login lower-cased.
SELECT
  ('EMP-' || r.result_id)::varchar(40) AS test_result_identifier,
  i.sample_name::varchar(40) AS sample_identifier,
  r.cf_test_code::varchar(40) AS test_code,
  r.cf_reported_value::varchar(60) AS test_value,
  r.cf_units::varchar(20) AS test_unit,
  r.cf_spec_min::varchar(60) AS specification_minimum_value,
  r.cf_spec_max::varchar(60) AS specification_maximum_value,
  (r.cf_pass_fail = 'Pass') AS test_conformity_flag,
  r.date_processed AS test_completed_timestamp,
  lower(r.processed_by)::varchar(40) AS test_analyst_identifier
FROM empower_cds.result r
JOIN empower_cds.injection i ON i.injection_id = r.injection_id
WHERE r.signoff_status = 'Approved'
