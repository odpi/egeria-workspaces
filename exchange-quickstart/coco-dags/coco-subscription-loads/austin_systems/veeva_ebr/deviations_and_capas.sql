-- Subscription: aus_veeva_ebr__deviations_and_capas - Veeva Vault EBR (Austin) receives Deviations And CAPAs
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (deviation disposition)
-- Keeps, for each Austin QMS deviation raised against a batch that has a record in this vault, a NEW
-- batch_deviation__c record with the investigation's disposition, so the reviewer sees open deviations before
-- certification. Deviations not linked to a batch, CAPA actions (managed in QMS) and EKG/TrackWise records are
-- discarded.

UPDATE incoming_deviation i SET discard_reason = 'other estate: not an Austin QMS deviation'
 WHERE i.deviation_identifier !~ '^DEV-[0-9]{2}-';
UPDATE incoming_deviation i SET discard_reason = 'not linked to a batch'
 WHERE i.discard_reason IS NULL AND i.batch_identifier IS NULL;
UPDATE incoming_deviation i SET discard_reason = 'no batch record in this vault'
 WHERE i.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.batch_deviation__c
       (id, name__v, batch__c, raised_datetime__c, source__c, severity__c, description__c, state__c)
SELECT ('0BV' || upper(substr(md5(i.deviation_identifier), 1, 11))), i.deviation_identifier, b.id, i.deviation_raised_timestamp,
       i.deviation_source_type, i.deviation_severity, i.deviation_description, i.deviation_current_status
  FROM incoming_deviation i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch__c = EXCLUDED.batch__c, raised_datetime__c = EXCLUDED.raised_datetime__c,
       source__c = EXCLUDED.source__c, severity__c = EXCLUDED.severity__c,
       description__c = EXCLUDED.description__c, state__c = EXCLUDED.state__c;

UPDATE incoming_investigation i SET discard_reason = 'deviation not linked to a batch record in this vault'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.batch_deviation__c d WHERE d.name__v = i.deviation_identifier);
UPDATE veeva_ebr.batch_deviation__c d
   SET disposition__c = i.deviation_disposition_status,
       investigation_completed__c = i.deviation_investigation_completed_date,
       impact__c = i.deviation_impact_description
  FROM incoming_investigation i
 WHERE i.discard_reason IS NULL AND d.name__v = i.deviation_identifier
   AND (d.disposition__c, d.investigation_completed__c, d.impact__c) IS DISTINCT FROM
       (i.deviation_disposition_status, i.deviation_investigation_completed_date, i.deviation_impact_description);

UPDATE incoming_corrective_action SET discard_reason = 'CAPA actions are managed in QMS, not the batch record';
