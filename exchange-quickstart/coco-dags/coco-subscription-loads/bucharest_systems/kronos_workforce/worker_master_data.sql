-- Subscription: buc_kronos_workforce__worker_master_data - Kronos Workforce (Bucharest) receives Worker Master Data
-- Destination: bucharest_systems.kronos_workforce (SoftwareServer::SYS-023::Kronos Workforce)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Keeps, on the Kronos person of each EKG worker (personnum = Workday employee ID, matched through the EKG pseudonym
-- rule): hire date and employment status (Active / Inactive for leave / Terminated, with the status date) from worker,
-- and the home labour account of the Workday cost centre (laborlev2nm) from worker_assignment.  New hires are created by
-- the Workday employee export, not here.  Discards Coco and Austin workers (EKG is not yet integrated) and EKG workers
-- without a Kronos person (contingent workers are not timekept).
UPDATE incoming_worker SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE legal_entity_code IS DISTINCT FROM 'RO01';
UPDATE incoming_worker i SET discard_reason = 'EKG worker without a Kronos person record'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM kronos_workforce.person p
                    WHERE 'WP-' || upper(substr(md5('EKG:' || p.personnum), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment a SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE a.worker_pseudonym_identifier LIKE 'CW-%'
    OR EXISTS (SELECT 1 FROM incoming_worker w WHERE w.worker_pseudonym_identifier = a.worker_pseudonym_identifier
                AND w.legal_entity_code IS DISTINCT FROM 'RO01');
UPDATE incoming_worker_assignment a SET discard_reason = 'not an EKG worker with a Kronos person record'
 WHERE a.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM kronos_workforce.person p
                    WHERE 'WP-' || upper(substr(md5('EKG:' || p.personnum), 1, 12)) = a.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment a SET discard_reason = 'cost centre has no Kronos labour account'
 WHERE a.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM kronos_workforce.laboracct l WHERE l.laborlev2nm = a.cost_centre_code);

WITH w AS (
  SELECT i.worker_pseudonym_identifier, i.worker_hire_date, i.worker_leave_date,
         (CASE i.worker_current_status WHEN 'left' THEN 'Terminated' WHEN 'on leave' THEN 'Inactive' ELSE 'Active' END) AS status
    FROM incoming_worker i WHERE i.discard_reason IS NULL
)
UPDATE kronos_workforce.person p
   SET hiredtm = coalesce(w.worker_hire_date, p.hiredtm),
       employmentstatusdtm = (CASE WHEN p.employmentstatus = w.status THEN p.employmentstatusdtm
                                   WHEN w.status = 'Terminated' THEN coalesce(w.worker_leave_date, current_date)
                                   ELSE current_date END),
       employmentstatus = w.status
  FROM w
 WHERE 'WP-' || upper(substr(md5('EKG:' || p.personnum), 1, 12)) = w.worker_pseudonym_identifier;

UPDATE kronos_workforce.person p
   SET homelaboracctid = l.laboracctid
  FROM incoming_worker_assignment a
  JOIN kronos_workforce.laboracct l ON l.laborlev2nm = a.cost_centre_code
 WHERE a.discard_reason IS NULL
   AND 'WP-' || upper(substr(md5('EKG:' || p.personnum), 1, 12)) = a.worker_pseudonym_identifier;
