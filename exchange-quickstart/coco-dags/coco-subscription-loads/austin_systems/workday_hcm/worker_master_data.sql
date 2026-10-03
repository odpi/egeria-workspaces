-- Subscription: aus_workday_hcm__worker_master_data - Workday Human Capital Management (Austin) receives Worker Master Data
-- Destination: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Keeps nothing: Workday is the system of record for every Austin worker in this product, so Austin rows (pseudonyms
-- that resolve to a Workday employee ID) are its own data coming back, and Coco (CW-) and EKG (RO01) workers belong
-- to other estates. Discarding them all is what keeps the worker extracts loop-free.

UPDATE incoming_worker i SET discard_reason = 'other estate: not an Austin (US01) worker'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_worker i SET discard_reason = 'already held: supplied by Workday (system of record)'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM workday_hcm.worker w WHERE 'WP-' || upper(substr(md5('AUS:' || w.employee_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker SET discard_reason = 'pseudonym does not resolve to a Workday worker'
 WHERE discard_reason IS NULL;

UPDATE incoming_worker_assignment i SET discard_reason = 'already held: supplied by Workday (system of record)'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.worker w WHERE 'WP-' || upper(substr(md5('AUS:' || w.employee_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment SET discard_reason = 'other estate: pseudonym is not an Austin worker'
 WHERE discard_reason IS NULL;
