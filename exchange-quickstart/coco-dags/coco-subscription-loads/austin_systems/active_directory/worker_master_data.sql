-- Subscription: aus_active_directory__worker_master_data - Microsoft Active Directory (Austin) receives Worker Master Data
-- Destination: austin_systems.active_directory (SoftwareServer::AUS-SYS-031::SN-AD-AU-20170901)
-- Why it subscribes: Access Entitlements depends on it (provision or revoke); Corporate Directory Entries depends on it (directory entry)
-- Keeps, on the ad_user object whose employeeID the pseudonym resolves to, the HR attributes the provisioning rules
-- key on: employeeType, the Workday status and leave date (extensionAttribute3/4), the cost centre
-- (departmentNumber) and job profile (extensionAttribute2) - NEW columns. Attributes the extracts read (title,
-- whenChanged, userAccountControl, accountExpires) are left to the AD admins. Other estates' workers and Austin
-- workers with no AD account are discarded.

UPDATE incoming_worker i SET discard_reason = 'other estate: not an Austin (US01) worker'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_worker i SET discard_reason = 'no AD account for this worker'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM active_directory.ad_user u WHERE u.employeeid IS NOT NULL
                      AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE active_directory.ad_user u
   SET employeetype = CASE i.worker_type WHEN 'employee' THEN 'Employee' ELSE 'Contractor' END,
       extensionattribute3 = i.worker_current_status,
       extensionattribute4 = to_char(i.worker_leave_date, 'YYYY-MM-DD')
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL AND u.employeeid IS NOT NULL AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier
   AND (u.employeetype, u.extensionattribute3, u.extensionattribute4) IS DISTINCT FROM
       (CASE i.worker_type WHEN 'employee' THEN 'Employee' ELSE 'Contractor' END, i.worker_current_status,
        to_char(i.worker_leave_date, 'YYYY-MM-DD'));

UPDATE incoming_worker_assignment i SET discard_reason = 'no AD account for this worker (or not an Austin worker)'
 WHERE NOT EXISTS (SELECT 1 FROM active_directory.ad_user u WHERE u.employeeid IS NOT NULL
                      AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE active_directory.ad_user u
   SET departmentnumber = i.cost_centre_code, extensionattribute2 = i.role_code
  FROM incoming_worker_assignment i
 WHERE i.discard_reason IS NULL AND u.employeeid IS NOT NULL AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier
   AND (u.departmentnumber, u.extensionattribute2) IS DISTINCT FROM (i.cost_centre_code, i.role_code);
