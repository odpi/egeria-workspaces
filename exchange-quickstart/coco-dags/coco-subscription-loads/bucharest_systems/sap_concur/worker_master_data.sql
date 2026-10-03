-- Subscription: buc_sap_concur__worker_master_data - SAP Concur (Bucharest) receives Worker Master Data
-- Destination: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Why it subscribes: Employee Expense Claims depends on it (expense access); Expense Approvals depends on it (approver and cost centre)
-- Keeps, on the Concur employee profile of each EKG worker (employee_id = Workday employee ID, matched through the EKG
-- pseudonym rule): active Y/N and the company (org_unit_1) from worker, the default cost centre (org_unit_2) from
-- worker_assignment - the Workday employee import.  Profiles are created when expense access is granted (a login is
-- needed), so EKG workers without a profile are discarded, as are Coco and Austin workers (EKG is not yet integrated).
UPDATE incoming_worker SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE legal_entity_code IS DISTINCT FROM 'RO01';
UPDATE incoming_worker i SET discard_reason = 'EKG worker without a Concur profile'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM sap_concur.employee e
                    WHERE 'WP-' || upper(substr(md5('EKG:' || e.employee_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment a SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE a.worker_pseudonym_identifier LIKE 'CW-%'
    OR EXISTS (SELECT 1 FROM incoming_worker w WHERE w.worker_pseudonym_identifier = a.worker_pseudonym_identifier
                AND w.legal_entity_code IS DISTINCT FROM 'RO01');
UPDATE incoming_worker_assignment a SET discard_reason = 'not an EKG worker with a Concur profile'
 WHERE a.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM sap_concur.employee e
                    WHERE 'WP-' || upper(substr(md5('EKG:' || e.employee_id), 1, 12)) = a.worker_pseudonym_identifier);

UPDATE sap_concur.employee e
   SET active = (CASE WHEN i.worker_current_status = 'left' THEN 'N' ELSE 'Y' END),
       org_unit_1 = i.legal_entity_code
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL
   AND 'WP-' || upper(substr(md5('EKG:' || e.employee_id), 1, 12)) = i.worker_pseudonym_identifier;

UPDATE sap_concur.employee e
   SET org_unit_2 = a.cost_centre_code
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.cost_centre_code IS NOT NULL
   AND 'WP-' || upper(substr(md5('EKG:' || e.employee_id), 1, 12)) = a.worker_pseudonym_identifier;
