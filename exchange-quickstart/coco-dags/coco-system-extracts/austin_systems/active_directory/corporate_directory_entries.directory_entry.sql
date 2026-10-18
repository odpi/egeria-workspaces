-- Extract: Microsoft Active Directory (Austin) -> Corporate Directory Entries / directory_entry
-- Source: austin_systems.active_directory (SoftwareServer::AUS-SYS-031::SN-AD-AU-20170901)
-- Target: coco_data_hub.corporate_directory_entries.directory_entry
-- Enabled ad_user objects (synchronised staff); manager DN resolved to the manager's employeeID and pseudonymised;
-- office mapped to site code.
SELECT
  ('WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  u.givenname::varchar(80) AS person_first_name,
  u.sn::varchar(80) AS person_last_name,
  u.title::varchar(120) AS role_name,
  u.department::varchar(120) AS department_name,
  (CASE u.physicaldeliveryofficename WHEN 'Austin Plant' THEN 'US10' WHEN 'Austin Distribution Center' THEN 'US20' END)::varchar(20) AS site_code,
  (CASE WHEN m.employeeid IS NOT NULL THEN ('WP-' || upper(substr(md5('AUS:' || m.employeeid), 1, 12))) END)::varchar(40) AS manager_pseudonym_identifier,
  u.telephonenumber::varchar(30) AS person_work_phone_number,
  u.whenchanged AS directory_entry_current_timestamp
FROM active_directory.ad_user u
LEFT JOIN active_directory.ad_user m ON m.distinguishedname = u.manager
WHERE (u.useraccountcontrol & 2) = 0 AND u.employeeid IS NOT NULL
