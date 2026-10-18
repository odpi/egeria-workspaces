-- Extract: Human Resources Information Manager (HRIM) (Coco core) -> Worker Lifecycle Events / worker_event
-- Source: coco_pharma.coco_hrim (System::coco-hrim)
-- Target: coco_data_hub.worker_lifecycle_events.worker_event
-- hr_event; HIR/XFR/TER to joiner/mover/leaver, employee number to pseudonym.
SELECT
  e.event_id::varchar(40)          AS worker_event_identifier,
  p.worker_ref::varchar(40)        AS worker_pseudonym_identifier,
  (CASE e.event_type WHEN 'HIR' THEN 'joiner' WHEN 'XFR' THEN 'mover' ELSE 'leaver' END)::varchar(10) AS worker_event_type,
  e.eff_date                       AS worker_event_start_date,
  e.raised_at                      AS worker_event_raised_timestamp,
  e.new_job_code::varchar(40)      AS role_code,
  e.event_text                     AS worker_event_description
FROM coco_hrim.hr_event e
JOIN coco_hrim.person p ON p.emp_no = e.emp_no
