-- Subscription: aus_veeva_ebr__electronic_batch_records - Veeva Vault EBR (Austin) receives Electronic Batch Records
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Batch Certification Decisions depends on it (batch record for review)
-- Keeps nothing: the vault is the Austin source of Electronic Batch Records, so rows for batches it holds are its
-- own record coming back (and writing them would loop into its extracts). Coco Winchester/Edmonton batch records and
-- EKG batch records are other estates' and are discarded.

UPDATE incoming_batch_record i SET discard_reason = 'already held: supplied by this vault'
 WHERE EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
UPDATE incoming_batch_record i SET discard_reason = CASE WHEN i.batch_identifier ~ '^[WE][0-9]{2}-'
       THEN 'other estate: Coco factory batch' ELSE 'other estate: not an Austin batch' END
 WHERE i.discard_reason IS NULL;

UPDATE incoming_batch_record_section i SET discard_reason = 'already held: supplied by this vault'
 WHERE EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
UPDATE incoming_batch_record_section i SET discard_reason = CASE WHEN i.batch_identifier ~ '^[WE][0-9]{2}-'
       THEN 'other estate: Coco factory batch' ELSE 'other estate: not an Austin batch' END
 WHERE i.discard_reason IS NULL;

UPDATE incoming_release_authorisation i SET discard_reason = 'already held: supplied by this vault'
 WHERE EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
UPDATE incoming_release_authorisation i SET discard_reason = CASE WHEN i.batch_identifier ~ '^[WE][0-9]{2}-'
       THEN 'other estate: Coco factory batch' ELSE 'other estate: not an Austin batch' END
 WHERE i.discard_reason IS NULL;
