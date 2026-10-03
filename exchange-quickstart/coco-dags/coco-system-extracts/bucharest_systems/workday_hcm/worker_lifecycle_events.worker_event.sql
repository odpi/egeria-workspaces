-- Extract: Workday HCM (Bucharest) -> Worker Lifecycle Events / worker_event
-- Source: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Target: coco_data_hub.worker_lifecycle_events.worker_event
-- business_process_event mapped to joiner/mover/leaver; the proposed job profile is the new role.
SELECT
  e.event_id::varchar(40) AS worker_event_identifier,
  ('WP-' || upper(substr(md5('EKG:' || e.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  (CASE e.business_process_type
     WHEN 'Hire' THEN 'joiner' WHEN 'Contract Contingent Worker' THEN 'joiner'
     WHEN 'Change Job' THEN 'mover' ELSE 'leaver' END)::varchar(10) AS worker_event_type,
  e.effective_date AS worker_event_start_date,
  e.initiated_moment AS worker_event_raised_timestamp,
  e.proposed_job_profile_id::varchar(40) AS role_code,
  e.comment AS worker_event_description
FROM workday_hcm.business_process_event e
WHERE e.status = 'Successfully Completed'
  AND e.business_process_type IN ('Hire', 'Contract Contingent Worker', 'Change Job', 'Terminate', 'End Contingent Worker Contract')
