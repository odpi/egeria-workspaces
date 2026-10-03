-- Extract: Cornerstone OnDemand LMS (Austin) -> Training Completions / refresher_schedule
-- Source: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Target: coco_data_hub.training_completions.refresher_schedule
-- Open refresher registrations (Registered / Past Due transcripts) with their due date and any scheduled session.
SELECT
  ('WP-' || upper(substr(md5('AUS:' || t.user_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  lc.competency_id::varchar(40) AS competency_code,
  t.due_dt AS training_due_date,
  l.lo_course_no::varchar(40) AS training_course_code,
  t.session_start_dt AS training_scheduled_date
FROM cornerstone_lms.transcript t
JOIN cornerstone_lms.training l ON l.lo_id = t.lo_id
JOIN cornerstone_lms.lo_competency lc ON lc.lo_id = t.lo_id
WHERE t.transcript_status IN ('Registered', 'Past Due', 'In Progress')
