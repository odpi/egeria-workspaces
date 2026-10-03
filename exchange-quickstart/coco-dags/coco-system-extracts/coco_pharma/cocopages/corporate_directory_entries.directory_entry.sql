-- Extract: CocoPages (Coco core) -> Corporate Directory Entries / directory_entry
-- Source: coco_pharma.cocopages (System::cocopages)
-- Target: coco_data_hub.corporate_directory_entries.directory_entry
-- dir_person workers only (partners excluded); location names to HRIM site codes; manager uid to pseudonym by self-join.
SELECT
  d.worker_ref::varchar(40)         AS worker_pseudonym_identifier,
  d.fname::varchar(80)              AS person_first_name,
  d.lname::varchar(80)              AS person_last_name,
  d.title::varchar(120)             AS role_name,
  d.dept::varchar(120)              AS department_name,
  (CASE d.loc WHEN 'London' THEN 'LON' WHEN 'Amsterdam' THEN 'AMS' WHEN 'New York' THEN 'NYC' WHEN 'Winchester' THEN 'WIN'
              WHEN 'Edmonton' THEN 'EDM' WHEN 'Kansas City' THEN 'KCY' ELSE d.loc END)::varchar(20) AS site_code,
  m.worker_ref::varchar(40)         AS manager_pseudonym_identifier,
  d.phone::varchar(30)              AS person_work_phone_number,
  d.last_sync                       AS directory_entry_current_timestamp
FROM cocopages.dir_person d
LEFT JOIN cocopages.dir_person m ON m.uid = d.mgr_uid
WHERE d.entry_typ IN ('EMP', 'CTR') AND d.worker_ref IS NOT NULL
