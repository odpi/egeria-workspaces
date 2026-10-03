-- Extract: Active Directory (Bucharest) -> Corporate Directory Entries / directory_entry
-- Source: bucharest_systems.active_directory (SoftwareServer::SYS-008::Active Directory)
-- Target: coco_data_hub.corporate_directory_entries.directory_entry
-- Enabled ad_user objects of staff with no mailbox (mail null; mailbox users come from Microsoft 365); manager DN
-- resolved to the manager's employeeID and pseudonymised; office mapped to site code.
SELECT
  ('WP-' || upper(substr(md5('EKG:' || u.employeeid), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  u.givenname::varchar(80) AS person_first_name,
  u.sn::varchar(80) AS person_last_name,
  u.title::varchar(120) AS role_name,
  u.department::varchar(120) AS department_name,
  (CASE u.physicaldeliveryofficename WHEN 'Fabrica București' THEN 'RO10' ELSE u.physicaldeliveryofficename END)::varchar(20) AS site_code,
  (CASE WHEN m.employeeid IS NOT NULL THEN ('WP-' || upper(substr(md5('EKG:' || m.employeeid), 1, 12))) END)::varchar(40) AS manager_pseudonym_identifier,
  u.telephonenumber::varchar(30) AS person_work_phone_number,
  u.whenchanged AS directory_entry_current_timestamp
FROM active_directory.ad_user u
LEFT JOIN active_directory.ad_user m ON m.distinguishedname = u.manager
WHERE (u.useraccountcontrol & 2) = 0 AND u.employeeid IS NOT NULL AND u.mail IS NULL
