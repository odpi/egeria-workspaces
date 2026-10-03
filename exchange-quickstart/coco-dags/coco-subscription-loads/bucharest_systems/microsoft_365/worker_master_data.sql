-- Subscription: buc_microsoft_365__worker_master_data - Microsoft 365 (Bucharest) receives Worker Master Data
-- Destination: bucharest_systems.microsoft_365 (SoftwareServer::SYS-007::Microsoft 365)
-- Why it subscribes: Corporate Directory Entries depends on it (directory entry)
-- Keeps, on the Exchange Online recipient of each EKG worker (CustomAttribute1 = Workday employee ID, matched through
-- the EKG pseudonym rule): the cost centre (CustomAttribute2), job profile (CustomAttribute3) and worker status
-- (CustomAttribute4), used by address-book policies and dynamic groups.  Name, title, department, office and manager are
-- synchronised from AD and are not touched.  Discards Coco and Austin workers (EKG is not yet integrated) and EKG workers
-- without a mailbox (shop-floor staff).
UPDATE incoming_worker SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE legal_entity_code IS DISTINCT FROM 'RO01';
UPDATE incoming_worker i SET discard_reason = 'EKG worker without an Exchange Online mailbox'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM microsoft_365.exo_recipient r
                    WHERE r.customattribute1 IS NOT NULL
                      AND 'WP-' || upper(substr(md5('EKG:' || r.customattribute1), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_worker_assignment a SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE a.worker_pseudonym_identifier LIKE 'CW-%'
    OR EXISTS (SELECT 1 FROM incoming_worker w WHERE w.worker_pseudonym_identifier = a.worker_pseudonym_identifier
                AND w.legal_entity_code IS DISTINCT FROM 'RO01');
UPDATE incoming_worker_assignment a SET discard_reason = 'not an EKG worker with an Exchange Online mailbox'
 WHERE a.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM microsoft_365.exo_recipient r
                    WHERE r.customattribute1 IS NOT NULL
                      AND 'WP-' || upper(substr(md5('EKG:' || r.customattribute1), 1, 12)) = a.worker_pseudonym_identifier);

UPDATE microsoft_365.exo_recipient r
   SET customattribute4 = (CASE WHEN i.worker_current_status = 'left'
                                THEN 'left ' || coalesce(to_char(i.worker_leave_date, 'YYYY-MM-DD'), '')
                                ELSE i.worker_current_status END)
  FROM incoming_worker i
 WHERE i.discard_reason IS NULL AND r.customattribute1 IS NOT NULL
   AND 'WP-' || upper(substr(md5('EKG:' || r.customattribute1), 1, 12)) = i.worker_pseudonym_identifier;

UPDATE microsoft_365.exo_recipient r
   SET customattribute2 = a.cost_centre_code,
       customattribute3 = a.role_code
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND r.customattribute1 IS NOT NULL
   AND 'WP-' || upper(substr(md5('EKG:' || r.customattribute1), 1, 12)) = a.worker_pseudonym_identifier;
