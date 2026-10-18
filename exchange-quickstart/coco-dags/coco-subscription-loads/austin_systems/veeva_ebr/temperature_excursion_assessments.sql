-- Subscription: aus_veeva_ebr__temperature_excursion_assessments - Veeva Vault EBR (Austin) receives Temperature Excursion Assessments
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (disposition recorded)
-- Keeps excursion assessments for batches that have a record in this vault as NEW excursion_assessment__c records,
-- so the disposition is part of the batch history at review. Assessments for other estates' batches, or for batches
-- without a record here, are discarded.

UPDATE incoming_excursion_assessment i SET discard_reason = CASE
       WHEN i.batch_identifier ~ '^[WE][0-9]{2}-' THEN 'other estate: Coco factory batch'
       WHEN i.batch_identifier ~ '^A[0-9]{2}-' THEN 'no batch record in this vault'
       ELSE 'other estate: not an Austin batch' END
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.excursion_assessment__c
       (id, name__v, batch__c, shipment__c, product_code__c, assessed_by__c, assessed_datetime__c,
        stability_reference__c, disposition__c, notes__c)
SELECT ('0EX' || upper(substr(md5(i.excursion_identifier), 1, 11))), i.excursion_identifier, b.id, i.shipment_identifier, i.product_code,
       i.excursion_assessor_identifier, i.excursion_assessment_timestamp, i.excursion_stability_reference_identifier,
       i.excursion_disposition_status, i.excursion_assessment_notes
  FROM incoming_excursion_assessment i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch__c = EXCLUDED.batch__c, shipment__c = EXCLUDED.shipment__c,
       product_code__c = EXCLUDED.product_code__c, assessed_by__c = EXCLUDED.assessed_by__c,
       assessed_datetime__c = EXCLUDED.assessed_datetime__c,
       stability_reference__c = EXCLUDED.stability_reference__c, disposition__c = EXCLUDED.disposition__c,
       notes__c = EXCLUDED.notes__c;
