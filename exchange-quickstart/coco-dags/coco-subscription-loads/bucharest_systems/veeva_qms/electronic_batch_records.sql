-- Subscription: buc_veeva_qms__electronic_batch_records - Veeva Vault QMS (Bucharest) receives Electronic Batch Records
-- Destination: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Why it subscribes: Batch Certification Decisions depends on it (batch record for review)
-- Keeps the EBR header of each EKG batch that has a Vault quality event - the batches the QP certifies in Vault
-- (batch_disposition__c) - in the new custom object batch__c (id BAT- + batch), reviewed before the disposition.
-- Batches without a quality event are certified by exception in the MES and are discarded; record sections stay in the
-- MES and ECM; release authorisations are the MES's or already Vault's own dispositions.  Other companies' batches are
-- discarded (Coco group data - EKG is not yet integrated).
UPDATE incoming_batch_record SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE batch_identifier !~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_batch_record i SET discard_reason = 'no quality event - certified by exception in the MES'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM veeva_qms.quality_event__qdm q WHERE q.batch_number__c = i.batch_identifier);
UPDATE incoming_batch_record_section SET discard_reason = 'EBR sections are reviewed in the MES and ECM'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_batch_record_section SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_release_authorisation i SET discard_reason = 'QP decision recorded in Vault (batch_disposition__c) - already held'
 WHERE EXISTS (SELECT 1 FROM veeva_qms.batch_disposition__c d WHERE d.batch_number__c = i.batch_identifier AND d.market__c = i.market_code);
UPDATE incoming_release_authorisation SET discard_reason = 'released by exception in the MES'
 WHERE discard_reason IS NULL AND batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_release_authorisation SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO veeva_qms.batch__c (id, name__v, product__c, start_date__c, end_date__c, quantity__c, record_complete__c,
                                certification_status__c, modified_date__v)
SELECT left('BAT-' || i.batch_identifier, 20), i.batch_identifier,
       (SELECT p.id FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code),
       i.batch_start_timestamp, i.batch_end_timestamp, i.batch_quantity, i.batch_record_complete_flag,
       (CASE WHEN i.batch_certification_status IS NULL THEN NULL ELSE replace(i.batch_certification_status, ' ', '_') || '__c' END),
       now()
  FROM incoming_batch_record i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE
   SET name__v = EXCLUDED.name__v, product__c = EXCLUDED.product__c, start_date__c = EXCLUDED.start_date__c,
       end_date__c = EXCLUDED.end_date__c, quantity__c = EXCLUDED.quantity__c, record_complete__c = EXCLUDED.record_complete__c,
       certification_status__c = EXCLUDED.certification_status__c, modified_date__v = now()
 WHERE (veeva_qms.batch__c.name__v, veeva_qms.batch__c.product__c, veeva_qms.batch__c.start_date__c, veeva_qms.batch__c.end_date__c,
        veeva_qms.batch__c.quantity__c, veeva_qms.batch__c.record_complete__c, veeva_qms.batch__c.certification_status__c)
       IS DISTINCT FROM (EXCLUDED.name__v, EXCLUDED.product__c, EXCLUDED.start_date__c, EXCLUDED.end_date__c,
                         EXCLUDED.quantity__c, EXCLUDED.record_complete__c, EXCLUDED.certification_status__c);
