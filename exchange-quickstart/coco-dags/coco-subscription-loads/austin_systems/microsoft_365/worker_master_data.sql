-- Subscription: aus_microsoft_365__worker_master_data - Microsoft 365 (Austin) receives Worker Master Data
-- Destination: austin_systems.microsoft_365 (SoftwareServer::AUS-SYS-033::SN-M365-AU-20200601)
-- Why it subscribes: Corporate Directory Entries depends on it (directory entry)
-- Keeps, on the Exchange Online recipient whose customAttribute1 (Workday employee ID) the pseudonym resolves to,
-- the job profile, cost centre and worker status in customAttribute2-4 (NEW columns) for address-list and dynamic-
-- group rules. The attributes the directory extract reads are not touched. Other estates' workers and workers with
-- no mailbox are discarded.

UPDATE incoming_worker i SET discard_reason = 'other estate: not an Austin (US01) worker'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_worker i SET discard_reason = 'no Microsoft 365 mailbox for this worker'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM microsoft_365.exo_recipient r WHERE r.customattribute1 IS NOT NULL
                      AND 'WP-' || upper(substr(md5('AUS:' || r.customattribute1), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE microsoft_365.exo_recipient r
   SET customattribute4 = i.worker_current_status
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL AND r.customattribute1 IS NOT NULL
   AND 'WP-' || upper(substr(md5('AUS:' || r.customattribute1), 1, 12)) = i.worker_pseudonym_identifier
   AND r.customattribute4 IS DISTINCT FROM i.worker_current_status;

UPDATE incoming_worker_assignment i SET discard_reason = 'no Microsoft 365 mailbox for this worker (or not an Austin worker)'
 WHERE NOT EXISTS (SELECT 1 FROM microsoft_365.exo_recipient r WHERE r.customattribute1 IS NOT NULL
                      AND 'WP-' || upper(substr(md5('AUS:' || r.customattribute1), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE microsoft_365.exo_recipient r
   SET customattribute2 = i.role_code, customattribute3 = i.cost_centre_code
  FROM incoming_worker_assignment i
 WHERE i.discard_reason IS NULL AND r.customattribute1 IS NOT NULL
   AND 'WP-' || upper(substr(md5('AUS:' || r.customattribute1), 1, 12)) = i.worker_pseudonym_identifier
   AND (r.customattribute2, r.customattribute3) IS DISTINCT FROM (i.role_code, i.cost_centre_code);
