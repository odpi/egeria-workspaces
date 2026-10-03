-- Subscription: aus_veeva_qms__electronic_batch_records - Veeva Vault QMS (Austin) receives Electronic Batch Records
-- Destination: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Why it subscribes: Batch Certification Decisions depends on it (batch record for review)
-- Keeps the Austin site's batch records (including Coco products made at Austin) as NEW batch_record_review__c
-- records - completeness and EBR status - so QA can take the disposition where a deviation is linked; the
-- batch_disposition__c table, which feeds Batch Certification Decisions, is only written by that decision. Section
-- detail and market releases stay in the EBR; Coco factory and EKG batches are discarded.

UPDATE incoming_batch_record i SET discard_reason = CASE WHEN i.batch_identifier ~ '^[WE][0-9]{2}-'
       THEN 'other estate: Coco factory batch' ELSE 'other estate: not an Austin batch' END
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
INSERT INTO veeva_qms.batch_record_review__c
       (id, name__v, product__c, patient_pseudonym__c, batch_start__c, batch_end__c, quantity__c,
        record_complete__c, ebr_status__c)
SELECT ('0BW' || upper(substr(md5(i.batch_identifier), 1, 11))), i.batch_identifier, p.id, i.patient_pseudonym_identifier,
       i.batch_start_timestamp, i.batch_end_timestamp, i.batch_quantity, i.batch_record_complete_flag,
       i.batch_certification_status
  FROM incoming_batch_record i
  LEFT JOIN veeva_qms.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, product__c = EXCLUDED.product__c,
       patient_pseudonym__c = EXCLUDED.patient_pseudonym__c, batch_start__c = EXCLUDED.batch_start__c,
       batch_end__c = EXCLUDED.batch_end__c, quantity__c = EXCLUDED.quantity__c,
       record_complete__c = EXCLUDED.record_complete__c, ebr_status__c = EXCLUDED.ebr_status__c;

UPDATE incoming_batch_record_section SET discard_reason = 'section detail stays in the EBR';
UPDATE incoming_release_authorisation SET discard_reason = 'market releases are recorded in the EBR';
