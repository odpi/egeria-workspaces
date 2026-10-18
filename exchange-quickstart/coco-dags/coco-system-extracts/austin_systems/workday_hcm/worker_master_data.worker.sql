-- Extract: Workday Human Capital Management (Austin) -> Worker Master Data / worker
-- Source: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Target: coco_data_hub.worker_master_data.worker
-- workday_hcm.worker; pseudonymises employee_id, maps location to site code and active/on-leave flags to status words.
SELECT
  ('WP-' || upper(substr(md5('AUS:' || w.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  (CASE WHEN w.worker_type = 'Employee' THEN 'employee' ELSE 'contractor' END)::varchar(20) AS worker_type,
  w.company_id::varchar(10) AS legal_entity_code,
  (CASE w.location_id WHEN 'LOC-AUS-PLANT' THEN 'US10' WHEN 'LOC-AUS-DC' THEN 'US20' ELSE w.location_id END)::varchar(20) AS site_code,
  w.hire_date AS worker_hire_date,
  w.termination_date AS worker_leave_date,
  (CASE WHEN NOT w.active THEN 'left' WHEN w.on_leave THEN 'on leave' ELSE 'active' END)::varchar(20) AS worker_current_status
FROM workday_hcm.worker w
