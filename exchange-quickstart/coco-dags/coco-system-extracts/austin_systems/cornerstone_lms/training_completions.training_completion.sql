-- Extract: Cornerstone OnDemand LMS (Austin) -> Training Completions / training_completion
-- Source: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Target: coco_data_hub.training_completions.training_completion
-- Completed transcript rows joined to training and lo_competency; learner pseudonymised from user_id.
SELECT
  t.reg_num::varchar(40) AS training_completion_identifier,
  ('WP-' || upper(substr(md5('AUS:' || t.user_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  l.lo_course_no::varchar(40) AS training_course_code,
  lc.competency_id::varchar(40) AS competency_code,
  t.completion_dt AS training_completed_date,
  t.expiration_dt AS training_expiry_date
FROM cornerstone_lms.transcript t
JOIN cornerstone_lms.training l ON l.lo_id = t.lo_id
JOIN cornerstone_lms.lo_competency lc ON lc.lo_id = t.lo_id
WHERE t.transcript_status = 'Completed'
