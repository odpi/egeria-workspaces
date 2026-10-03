-- Extract: Cornerstone OnDemand LMS (Austin) -> Training Completions / assessment_result
-- Source: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Target: coco_data_hub.training_completions.assessment_result
-- transcript_test attempts; passed Y/N to boolean.
SELECT
  a.reg_num::varchar(40) AS training_completion_identifier,
  a.attempt_dt AS training_assessment_date,
  a.score::double precision AS training_assessment_value,
  a.passing_score::double precision AS training_assessment_minimum_value,
  (a.passed = 'Y') AS training_assessment_passed_flag
FROM cornerstone_lms.transcript_test a
