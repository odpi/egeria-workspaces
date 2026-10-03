-- Extract: Human Resources Information Manager (HRIM) (Coco core) -> Worker Master Data / worker
-- Source: coco_pharma.coco_hrim (System::coco-hrim)
-- Target: coco_data_hub.worker_master_data.worker
-- person; codes expanded, worker identified by pseudonym only.
SELECT
  p.worker_ref::varchar(40)        AS worker_pseudonym_identifier,
  (CASE p.worker_cat WHEN 'CTR' THEN 'contractor' ELSE 'employee' END)::varchar(20) AS worker_type,
  p.company::varchar(10)           AS legal_entity_code,
  p.location::varchar(20)          AS site_code,
  p.hire_date                      AS worker_hire_date,
  p.term_date                      AS worker_leave_date,
  (CASE p.emp_status WHEN 'A' THEN 'active' WHEN 'L' THEN 'on leave' ELSE 'left' END)::varchar(20) AS worker_current_status
FROM coco_hrim.person p
