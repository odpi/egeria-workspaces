-- Subscription: aus_entra_id__worker_master_data - Microsoft Entra ID (Austin) receives Worker Master Data
-- Destination: austin_systems.entra_id (SoftwareServer::AUS-SYS-032::SN-AAD-AU-20200601)
-- Why it subscribes: Access Entitlements depends on it (provision or revoke)
-- Keeps, on the user whose employeeId the pseudonym resolves to, what Workday-driven provisioning writes in Entra:
-- employeeHireDate, employeeLeaveDateTime, employeeType and employeeOrgData costCenter (NEW columns), and the job
-- title for cloud-only users. accountEnabled and the sign-in block, which the entitlement extracts read, stay with
-- the lifecycle workflows. Other estates' workers and workers without an Entra user are discarded.

UPDATE incoming_worker i SET discard_reason = 'other estate: not an Austin (US01) worker'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_worker i SET discard_reason = 'no Entra ID user for this worker'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM entra_id.users u WHERE u.employeeid IS NOT NULL
                      AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE entra_id.users u
   SET employeehiredate = i.worker_hire_date,
       employeeleavedatetime = CASE WHEN u.employeeleavedatetime::date IS NOT DISTINCT FROM i.worker_leave_date
                                    THEN u.employeeleavedatetime
                                    ELSE i.worker_leave_date::timestamp AT TIME ZONE 'UTC' END,
       employeetype = CASE i.worker_type WHEN 'employee' THEN 'Employee' ELSE 'Contractor' END
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL AND u.employeeid IS NOT NULL AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier
   AND (u.employeehiredate IS DISTINCT FROM i.worker_hire_date
        OR u.employeeleavedatetime::date IS DISTINCT FROM i.worker_leave_date
        OR u.employeetype IS DISTINCT FROM CASE i.worker_type WHEN 'employee' THEN 'Employee' ELSE 'Contractor' END);

UPDATE incoming_worker_assignment i SET discard_reason = 'no Entra ID user for this worker (or not an Austin worker)'
 WHERE NOT EXISTS (SELECT 1 FROM entra_id.users u WHERE u.employeeid IS NOT NULL
                      AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE entra_id.users u
   SET employee_org_data_cost_center = i.cost_centre_code,
       jobtitle = CASE WHEN u.onpremisessyncenabled THEN u.jobtitle ELSE i.role_name END
  FROM incoming_worker_assignment i
 WHERE i.discard_reason IS NULL AND u.employeeid IS NOT NULL AND 'WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier
   AND (u.employee_org_data_cost_center IS DISTINCT FROM i.cost_centre_code
        OR (NOT u.onpremisessyncenabled AND u.jobtitle IS DISTINCT FROM i.role_name));
