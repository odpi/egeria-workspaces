-- Extract: Human Resources Information Manager (HRIM) (Coco core) -> Worker Master Data / worker_assignment
-- Source: coco_pharma.coco_hrim (System::coco-hrim)
-- Target: coco_data_hub.worker_master_data.worker_assignment
-- latest job_assignment per worker with job title; manager employee number to pseudonym; zero spend authority reported as none.
WITH cur AS (
  SELECT DISTINCT ON (a.emp_no) a.*
  FROM coco_hrim.job_assignment a
  ORDER BY a.emp_no, a.eff_date DESC
)
SELECT
  p.worker_ref::varchar(40)        AS worker_pseudonym_identifier,
  c.job_code::varchar(40)          AS role_code,
  j.job_title::varchar(120)        AS role_name,
  c.cost_center::varchar(20)       AS cost_centre_code,
  m.worker_ref::varchar(40)        AS manager_pseudonym_identifier,
  c.eff_date                       AS worker_assignment_start_date,
  nullif(c.spend_auth, 0)::numeric(18,2) AS worker_spending_maximum_amount,
  j.haz_profile                    AS worker_hazard_profile_description
FROM cur c
JOIN coco_hrim.person p ON p.emp_no = c.emp_no
JOIN coco_hrim.job j ON j.job_code = c.job_code
LEFT JOIN coco_hrim.person m ON m.emp_no = c.mgr_emp_no
