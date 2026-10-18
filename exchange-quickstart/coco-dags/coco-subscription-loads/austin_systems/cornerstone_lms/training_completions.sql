-- Subscription: aus_cornerstone_lms__training_completions - Cornerstone OnDemand LMS (Austin) receives Training Completions
-- Destination: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Why it subscribes: Worker Qualifications depends on it (completion and assessment)
-- Keeps nothing: Cornerstone is the only source of Training Completions, so every completion, assessment and
-- refresher row is its own transcript data coming back (reg_num already in transcript, or a learner and competency
-- it already schedules). Anything else would be another estate's and is discarded too.

UPDATE incoming_training_completion i SET discard_reason = 'already held: Cornerstone transcript'
 WHERE EXISTS (SELECT 1 FROM cornerstone_lms.transcript t WHERE t.reg_num = i.training_completion_identifier);
UPDATE incoming_training_completion SET discard_reason = 'other estate: not a Cornerstone transcript'
 WHERE discard_reason IS NULL;

UPDATE incoming_assessment_result i SET discard_reason = 'already held: Cornerstone transcript test'
 WHERE EXISTS (SELECT 1 FROM cornerstone_lms.transcript t WHERE t.reg_num = i.training_completion_identifier);
UPDATE incoming_assessment_result SET discard_reason = 'other estate: not a Cornerstone transcript'
 WHERE discard_reason IS NULL;

UPDATE incoming_refresher_schedule i SET discard_reason = 'already held: Cornerstone refresher registration'
 WHERE EXISTS (SELECT 1 FROM cornerstone_lms.transcript t
                 JOIN cornerstone_lms.lo_competency c ON c.lo_id = t.lo_id
                WHERE 'WP-' || upper(substr(md5('AUS:' || t.user_id), 1, 12)) = i.worker_pseudonym_identifier
                  AND c.competency_id = i.competency_code AND t.due_dt = i.training_due_date);
UPDATE incoming_refresher_schedule SET discard_reason = 'not a Cornerstone refresher registration (other estate)'
 WHERE discard_reason IS NULL;
