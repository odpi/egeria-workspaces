-- Extract: Microsoft 365 (Bucharest) -> Corporate Directory Entries / directory_entry
-- Source: bucharest_systems.microsoft_365 (SoftwareServer::SYS-007::Microsoft 365)
-- Target: coco_data_hub.corporate_directory_entries.directory_entry
-- User mailboxes (shared mailboxes of leavers excluded); manager address resolved to the manager's employee ID; office
-- mapped to site code.
SELECT
  ('WP-' || upper(substr(md5('EKG:' || r.customattribute1), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  r.firstname::varchar(80) AS person_first_name,
  r.lastname::varchar(80) AS person_last_name,
  r.title::varchar(120) AS role_name,
  r.department::varchar(120) AS department_name,
  (CASE r.office WHEN 'Fabrica București' THEN 'RO10' ELSE r.office END)::varchar(20) AS site_code,
  (CASE WHEN m.customattribute1 IS NOT NULL THEN ('WP-' || upper(substr(md5('EKG:' || m.customattribute1), 1, 12))) END)::varchar(40) AS manager_pseudonym_identifier,
  r.phone::varchar(30) AS person_work_phone_number,
  r.whenchanged AS directory_entry_current_timestamp
FROM microsoft_365.exo_recipient r
LEFT JOIN microsoft_365.exo_recipient m ON m.primarysmtpaddress = r.manager
WHERE r.recipienttypedetails = 'UserMailbox'
