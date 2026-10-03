-- Extract: Workday HCM (Bucharest) -> Worker Master Data / worker_assignment
-- Source: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Target: coco_data_hub.worker_master_data.worker_assignment
-- Latest worker_position row per worker joined to job_profile; manager pseudonymised with the same rule as the worker.
SELECT DISTINCT ON (p.employee_id)
  ('WP-' || upper(substr(md5('EKG:' || p.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  p.job_profile_id::varchar(40) AS role_code,
  j.job_profile_name::varchar(120) AS role_name,
  p.cost_center_id::varchar(20) AS cost_centre_code,
  (CASE WHEN p.manager_employee_id IS NOT NULL THEN ('WP-' || upper(substr(md5('EKG:' || p.manager_employee_id), 1, 12))) END)::varchar(40) AS manager_pseudonym_identifier,
  p.effective_date AS worker_assignment_start_date,
  j.approval_authority_amount::numeric(18,2) AS worker_spending_maximum_amount,
  j.work_hazards AS worker_hazard_profile_description
FROM workday_hcm.worker_position p
JOIN workday_hcm.job_profile j ON j.job_profile_id = p.job_profile_id
WHERE p.primary_job
ORDER BY p.employee_id, p.effective_date DESC
