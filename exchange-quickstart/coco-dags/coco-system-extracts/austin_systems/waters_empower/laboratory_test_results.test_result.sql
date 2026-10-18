-- Extract: Waters Empower 3 (Austin) -> Laboratory Test Results / test_result
-- Source: austin_systems.waters_empower (SoftwareServer::AUS-SYS-027::SN-CHR-AU-20180615)
-- Target: coco_data_hub.laboratory_test_results.test_result
-- Signed-off result joined to injection (sample name = LIMS sample ID); identifier prefixed EMP-; Pass/Fail to
-- boolean.
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
  r.processed_by::varchar(40) AS test_analyst_identifier
FROM waters_empower.result r
JOIN waters_empower.injection i ON i.injection_id = r.injection_id
WHERE r.signoff_status = 'Approved'
