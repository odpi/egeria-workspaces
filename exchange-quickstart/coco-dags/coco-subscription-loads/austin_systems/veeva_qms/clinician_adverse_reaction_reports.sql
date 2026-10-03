-- Subscription: aus_veeva_qms__clinician_adverse_reaction_reports - Veeva Vault QMS (Austin) receives Clinician Adverse Reaction Reports
-- Destination: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Why it subscribes: Consolidated Safety Reports depends on it (clinician report)
-- Keeps clinician reaction reports about Austin products or batches (Salesforce portal reports and reactions phoned
-- to the Oracle order desk) as NEW external_safety_report__c records, which the quality unit triages; the
-- safety_intake__c register, which feeds Consolidated Safety Reports, holds only reports first received by QMS.
-- Coco's reports (other estate) are discarded.

UPDATE incoming_clinician_reaction_report i SET discard_reason = 'other estate: not an Austin product or batch'
 WHERE NOT (i.product_code LIKE 'AU-%' OR coalesce(i.batch_identifier, '') ~ '^A[0-9]{2}-');
INSERT INTO veeva_qms.external_safety_report__c
       (id, name__v, reported_date__c, patient_pseudonym__c, clinician__c, product__c, batch_number__c,
        event_description__c, reported_severity__c)
SELECT ('0XR' || upper(substr(md5(i.adverse_event_identifier), 1, 11))), i.adverse_event_identifier, i.adverse_event_reported_date,
       i.patient_pseudonym_identifier, i.clinician_identifier, p.id, i.batch_identifier,
       i.adverse_event_description, i.adverse_event_reported_severity
  FROM incoming_clinician_reaction_report i
  LEFT JOIN veeva_qms.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, reported_date__c = EXCLUDED.reported_date__c,
       patient_pseudonym__c = EXCLUDED.patient_pseudonym__c, clinician__c = EXCLUDED.clinician__c,
       product__c = EXCLUDED.product__c, batch_number__c = EXCLUDED.batch_number__c,
       event_description__c = EXCLUDED.event_description__c, reported_severity__c = EXCLUDED.reported_severity__c;
