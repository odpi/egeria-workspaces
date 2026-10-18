-- Subscription: aus_cornerstone_lms__qualification_expiry_warnings - Cornerstone OnDemand LMS (Austin) receives Qualification Expiry Warnings
-- Destination: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Why it subscribes: Training Completions depends on it (refresher required)
-- Keeps warnings about Austin learners (pseudonym resolved to the Cornerstone user ID) for competencies in its
-- library in the NEW compliance_alert table, from which the administrator assigns the refresher; the transcript
-- table, which the extracts read, is not written. Warnings about other estates' workers or unknown competencies are
-- discarded.

UPDATE incoming_qualification_expiry_warning i SET discard_reason = 'not a Cornerstone learner (other estate)'
 WHERE NOT EXISTS (SELECT 1 FROM cornerstone_lms.users u WHERE 'WP-' || upper(substr(md5('AUS:' || u.user_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_qualification_expiry_warning i SET discard_reason = 'competency not in the Cornerstone library'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM cornerstone_lms.competency c WHERE c.competency_id = i.competency_code);

INSERT INTO cornerstone_lms.compliance_alert
       (alert_id, user_id, competency_id, expiration_dt, raised_dt, alert_type, due_dt)
SELECT i.qualification_warning_identifier, u.user_id, i.competency_code, i.qualification_expiry_date,
       i.qualification_warning_raised_timestamp, i.qualification_warning_type, i.training_due_date
  FROM incoming_qualification_expiry_warning i
  JOIN cornerstone_lms.users u ON 'WP-' || upper(substr(md5('AUS:' || u.user_id), 1, 12)) = i.worker_pseudonym_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (alert_id) DO UPDATE SET
       user_id = EXCLUDED.user_id, competency_id = EXCLUDED.competency_id, expiration_dt = EXCLUDED.expiration_dt,
       raised_dt = EXCLUDED.raised_dt, alert_type = EXCLUDED.alert_type, due_dt = EXCLUDED.due_dt;
