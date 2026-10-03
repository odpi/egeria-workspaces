-- Subscription: aus_cornerstone_lms__worker_master_data - Cornerstone OnDemand LMS (Austin) receives Worker Master Data
-- Destination: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Why it subscribes: Training Completions depends on it (worker and role); Worker Qualifications depends on it (new worker record)
-- Keeps the learner status, last hire date and position OU (= Workday job profile, which drives the role-based
-- curriculum) on the users row of each Austin worker who is already a learner (user_id = Workday employee ID behind
-- the pseudonym). users is not read by any extract. Coco and EKG workers, and Austin workers not yet loaded as
-- learners, are discarded.

UPDATE incoming_worker i SET discard_reason = 'other estate: not an Austin (US01) worker'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_worker i SET discard_reason = 'not a Cornerstone learner'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM cornerstone_lms.users u WHERE 'WP-' || upper(substr(md5('AUS:' || u.user_id), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE cornerstone_lms.users u
   SET user_status = CASE WHEN i.worker_current_status = 'left' THEN 'Inactive' ELSE 'Active' END,
       last_hire_date = i.worker_hire_date
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL AND 'WP-' || upper(substr(md5('AUS:' || u.user_id), 1, 12)) = i.worker_pseudonym_identifier
   AND (u.user_status, u.last_hire_date) IS DISTINCT FROM
       (CASE WHEN i.worker_current_status = 'left' THEN 'Inactive' ELSE 'Active' END, i.worker_hire_date);

UPDATE incoming_worker_assignment i SET discard_reason = 'not a Cornerstone learner (or not an Austin worker)'
 WHERE NOT EXISTS (SELECT 1 FROM cornerstone_lms.users u WHERE 'WP-' || upper(substr(md5('AUS:' || u.user_id), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE cornerstone_lms.users u
   SET ou_position_id = i.role_code
  FROM incoming_worker_assignment i
 WHERE i.discard_reason IS NULL AND 'WP-' || upper(substr(md5('AUS:' || u.user_id), 1, 12)) = i.worker_pseudonym_identifier
   AND u.ou_position_id IS DISTINCT FROM i.role_code;
