-- Subscription: buc_active_directory__worker_master_data - Active Directory (Bucharest) receives Worker Master Data
-- Destination: bucharest_systems.active_directory (SoftwareServer::SYS-008::Active Directory)
-- Why it subscribes: Access Entitlements depends on it (provision or revoke); Corporate Directory Entries depends on it (directory entry)
-- Keeps, for EKG workers with an AD account (employeeID matched through the EKG pseudonym rule): employeeType and the
-- Workday status (extensionAttribute11) from worker, the cost centre (departmentNumber) and job profile
-- (extensionAttribute12) from worker_assignment.  Enabling/disabling accounts and the attributes the directory extracts
-- read stay with the IAM process (a leaver is flagged in extensionAttribute11 for the deprovisioning review).
-- Discards Coco and Austin workers (EKG is not yet integrated) and EKG workers who have no AD account.
UPDATE incoming_worker SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE legal_entity_code IS DISTINCT FROM 'RO01';
UPDATE incoming_worker i SET discard_reason = 'EKG worker without an Active Directory account'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM active_directory.ad_user u
                    WHERE u.employeeid IS NOT NULL
                      AND 'WP-' || upper(substr(md5('EKG:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment a SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE a.worker_pseudonym_identifier LIKE 'CW-%'
    OR EXISTS (SELECT 1 FROM incoming_worker w WHERE w.worker_pseudonym_identifier = a.worker_pseudonym_identifier
                AND w.legal_entity_code IS DISTINCT FROM 'RO01');
UPDATE incoming_worker_assignment a SET discard_reason = 'not an EKG worker with an Active Directory account'
 WHERE a.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM active_directory.ad_user u
                    WHERE u.employeeid IS NOT NULL
                      AND 'WP-' || upper(substr(md5('EKG:' || u.employeeid), 1, 12)) = a.worker_pseudonym_identifier);

UPDATE active_directory.ad_user u
   SET employeetype = i.worker_type,
       extensionattribute11 = (CASE WHEN i.worker_current_status = 'left'
                                    THEN 'left ' || coalesce(to_char(i.worker_leave_date, 'YYYY-MM-DD'), '')
                                    ELSE i.worker_current_status END)
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL AND u.employeeid IS NOT NULL
   AND 'WP-' || upper(substr(md5('EKG:' || u.employeeid), 1, 12)) = i.worker_pseudonym_identifier;

UPDATE active_directory.ad_user u
   SET departmentnumber = a.cost_centre_code,
       extensionattribute12 = a.role_code
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND u.employeeid IS NOT NULL
   AND 'WP-' || upper(substr(md5('EKG:' || u.employeeid), 1, 12)) = a.worker_pseudonym_identifier;
