-- Extract: Microsoft 365 (Austin) -> Corporate Directory Entries / directory_entry
-- Source: austin_systems.microsoft_365 (SoftwareServer::AUS-SYS-033::SN-M365-AU-20200601)
-- Target: coco_data_hub.corporate_directory_entries.directory_entry
-- Cloud-only user mailboxes (isdirsynced = false; synced staff come from Active Directory); manager address resolved
-- to the manager's employee ID.
SELECT
  ('WP-' || upper(substr(md5('AUS:' || r.customattribute1), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  r.firstname::varchar(80) AS person_first_name,
  r.lastname::varchar(80) AS person_last_name,
  r.title::varchar(120) AS role_name,
  r.department::varchar(120) AS department_name,
  (CASE r.office WHEN 'Austin Plant' THEN 'US10' WHEN 'Austin Distribution Center' THEN 'US20' END)::varchar(20) AS site_code,
  (CASE WHEN m.customattribute1 IS NOT NULL THEN ('WP-' || upper(substr(md5('AUS:' || m.customattribute1), 1, 12))) END)::varchar(40) AS manager_pseudonym_identifier,
  r.phone::varchar(30) AS person_work_phone_number,
  r.whenchanged AS directory_entry_current_timestamp
FROM microsoft_365.exo_recipient r
LEFT JOIN microsoft_365.exo_recipient m ON m.primarysmtpaddress = r.manager
WHERE NOT r.isdirsynced AND r.recipienttypedetails = 'UserMailbox'
