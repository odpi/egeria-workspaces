-- Subscription: aus_veeva_ebr__laboratory_test_results - Veeva Vault EBR (Austin) receives Laboratory Test Results
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (finished product results)
-- Keeps the in-process and finished-product samples, results and certificates of analysis of batches that have a
-- record in this vault, as NEW qc_sample__c, qc_result__c and certificate_of_analysis__c records for review by
-- exception. Raw-material samples and certificates (lot release is SAP/WMS business) and EKG results are discarded.

UPDATE incoming_sample i SET discard_reason = 'raw material sample: no batch record'
 WHERE i.batch_identifier IS NULL AND coalesce(i.lot_identifier, '') ~ '^RM[0-9]{2}-';
UPDATE incoming_sample i SET discard_reason = 'other estate: not an Austin sample'
 WHERE i.discard_reason IS NULL AND coalesce(i.batch_identifier, '') !~ '^A[0-9]{2}-';
UPDATE incoming_sample i SET discard_reason = 'no batch record in this vault'
 WHERE i.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.qc_sample__c (id, name__v, batch__c, sample_type__c, collected_datetime__c, status__c)
SELECT ('0QS' || upper(substr(md5(i.sample_identifier), 1, 11))), i.sample_identifier, b.id, i.sample_type,
       i.sample_collection_timestamp, i.sample_current_status
  FROM incoming_sample i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch__c = EXCLUDED.batch__c, sample_type__c = EXCLUDED.sample_type__c,
       collected_datetime__c = EXCLUDED.collected_datetime__c, status__c = EXCLUDED.status__c;

UPDATE incoming_test_result i SET discard_reason = 'sample not linked to a batch record in this vault'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.qc_sample__c s WHERE s.name__v = i.sample_identifier);
INSERT INTO veeva_ebr.qc_result__c
       (id, name__v, qc_sample__c, test__c, result_value__c, unit__c, specification_min__c, specification_max__c,
        conforms__c, completed_datetime__c, analyst__c)
SELECT ('0QR' || upper(substr(md5(i.test_result_identifier), 1, 11))), i.test_result_identifier, s.id, i.test_code, i.test_value,
       i.test_unit, i.specification_minimum_value, i.specification_maximum_value, i.test_conformity_flag,
       i.test_completed_timestamp, i.test_analyst_identifier
  FROM incoming_test_result i JOIN veeva_ebr.qc_sample__c s ON s.name__v = i.sample_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, qc_sample__c = EXCLUDED.qc_sample__c, test__c = EXCLUDED.test__c,
       result_value__c = EXCLUDED.result_value__c, unit__c = EXCLUDED.unit__c,
       specification_min__c = EXCLUDED.specification_min__c, specification_max__c = EXCLUDED.specification_max__c,
       conforms__c = EXCLUDED.conforms__c, completed_datetime__c = EXCLUDED.completed_datetime__c,
       analyst__c = EXCLUDED.analyst__c;

UPDATE incoming_certificate_of_analysis i SET discard_reason = 'raw material certificate: no batch record'
 WHERE i.batch_identifier IS NULL;
UPDATE incoming_certificate_of_analysis i SET discard_reason = CASE WHEN i.batch_identifier ~ '^A[0-9]{2}-'
       THEN 'no batch record in this vault' ELSE 'other estate: not an Austin batch' END
 WHERE i.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.certificate_of_analysis__c
       (id, name__v, batch__c, certificate_date__c, conforms__c, approved_by__c)
SELECT ('0CA' || upper(substr(md5(i.certificate_identifier), 1, 11))), i.certificate_identifier, b.id, i.certificate_date,
       i.certificate_conformity_flag, i.certificate_approver_identifier
  FROM incoming_certificate_of_analysis i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch__c = EXCLUDED.batch__c, certificate_date__c = EXCLUDED.certificate_date__c,
       conforms__c = EXCLUDED.conforms__c, approved_by__c = EXCLUDED.approved_by__c;
