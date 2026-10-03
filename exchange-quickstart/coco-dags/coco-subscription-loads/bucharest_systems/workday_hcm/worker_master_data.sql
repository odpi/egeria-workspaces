-- Subscription: buc_workday_hcm__worker_master_data - Workday HCM (Bucharest) receives Worker Master Data
-- Destination: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Workday is the source of EKG's worker master data, so every EKG worker and assignment is already held here and is
-- discarded (no feedback loop); Coco and Austin workers are discarded too (EKG is not yet integrated).  Nothing is
-- written.
UPDATE incoming_worker i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.worker w
                WHERE 'WP-' || upper(substr(md5('EKG:' || w.employee_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.worker w
                WHERE 'WP-' || upper(substr(md5('EKG:' || w.employee_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_worker_assignment SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
