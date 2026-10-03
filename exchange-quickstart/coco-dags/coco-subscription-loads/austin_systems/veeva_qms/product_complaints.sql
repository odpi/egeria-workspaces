-- Subscription: aus_veeva_qms__product_complaints - Veeva Vault QMS (Austin) receives Product Complaints
-- Destination: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Why it subscribes: Consolidated Safety Reports depends on it (complaint with safety content)
-- Keeps the Austin product complaints (ServiceNow CSM cases) as NEW complaint__qdm records for quality
-- investigation, with the customer service safety assessment on the same record. Complaints are only Austin's today;
-- any for other estates' products or batches are discarded.

UPDATE incoming_complaint i SET discard_reason = 'other estate: not an Austin product or batch'
 WHERE NOT ((i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000')) OR coalesce(i.batch_identifier, '') ~ '^A[0-9]{2}-')
    OR coalesce(i.batch_identifier, '') ~ '^[WE][0-9]{2}-';
INSERT INTO veeva_qms.complaint__qdm
       (id, name__v, received_datetime__c, reporter_type__c, product__c, batch_number__c, serial_number__c,
        description__c, csm_status__c)
SELECT ('0CQ' || upper(substr(md5(i.complaint_identifier), 1, 11))), i.complaint_identifier, i.complaint_received_timestamp,
       i.complaint_reporter_type, p.id, i.batch_identifier, i.pack_serial_number, i.complaint_description,
       i.complaint_current_status
  FROM incoming_complaint i
  LEFT JOIN veeva_qms.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, received_datetime__c = EXCLUDED.received_datetime__c,
       reporter_type__c = EXCLUDED.reporter_type__c, product__c = EXCLUDED.product__c,
       batch_number__c = EXCLUDED.batch_number__c, serial_number__c = EXCLUDED.serial_number__c,
       description__c = EXCLUDED.description__c, csm_status__c = EXCLUDED.csm_status__c;

UPDATE incoming_complaint_safety_assessment i SET discard_reason = 'complaint not held in QMS'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.complaint__qdm c WHERE c.name__v = i.complaint_identifier);
UPDATE veeva_qms.complaint__qdm c
   SET safety_content__c = i.complaint_safety_flag, safety_assessed_by__c = i.complaint_assessor_identifier,
       safety_assessed_datetime__c = i.complaint_assessment_timestamp,
       safety_case_reference__c = i.safety_report_identifier
  FROM incoming_complaint_safety_assessment i
 WHERE i.discard_reason IS NULL AND c.name__v = i.complaint_identifier
   AND (c.safety_content__c, c.safety_assessed_by__c, c.safety_assessed_datetime__c, c.safety_case_reference__c)
       IS DISTINCT FROM (i.complaint_safety_flag, i.complaint_assessor_identifier, i.complaint_assessment_timestamp,
                         i.safety_report_identifier);
