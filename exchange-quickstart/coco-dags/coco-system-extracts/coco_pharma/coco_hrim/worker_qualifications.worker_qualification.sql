-- Extract: Human Resources Information Manager (HRIM) (Coco core) -> Worker Qualifications / worker_qualification
-- Source: coco_pharma.coco_hrim (System::coco-hrim)
-- Target: coco_data_hub.worker_qualifications.worker_qualification
-- emp_competency with the competency name and the job the worker held when it was gained; status derived from expiry against the run date (lapsing = within 60 days).
SELECT
  p.worker_ref::varchar(40)        AS worker_pseudonym_identifier,
  q.comp_cd::varchar(40)           AS competency_code,
  c.comp_name::varchar(120)        AS competency_name,
  q.achieved_dt                    AS qualification_start_date,
  q.expiry_dt                      AS qualification_expiry_date,
  (CASE WHEN q.expiry_dt < current_date THEN 'lapsed'
        WHEN q.expiry_dt < current_date + 60 THEN 'lapsing' ELSE 'current' END)::varchar(20) AS qualification_current_status,
  q.training_ref::varchar(40)      AS training_completion_identifier,
  q.cert_no::varchar(40)           AS certificate_identifier,
  a.job_code::varchar(40)          AS role_code
FROM coco_hrim.emp_competency q
JOIN coco_hrim.person p ON p.emp_no = q.emp_no
JOIN coco_hrim.competency c ON c.comp_cd = q.comp_cd
JOIN LATERAL (SELECT ja.job_code FROM coco_hrim.job_assignment ja
              WHERE ja.emp_no = q.emp_no AND ja.eff_date <= q.achieved_dt
              ORDER BY ja.eff_date DESC LIMIT 1) a ON true
