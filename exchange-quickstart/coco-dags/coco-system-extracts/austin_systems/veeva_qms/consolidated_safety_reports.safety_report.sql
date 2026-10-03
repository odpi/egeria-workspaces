-- Extract: Veeva Vault QMS (Austin) -> Consolidated Safety Reports / safety_report
-- Source: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Target: coco_data_hub.consolidated_safety_reports.safety_report
-- safety_intake__c joined to product__v; source picklist translated; received time is first receipt at the originating
-- door.
SELECT
  si.name__v::varchar(40) AS safety_report_identifier,
  si.received_datetime__c AS safety_report_received_timestamp,
  (CASE si.source_type__c WHEN 'clinician__c' THEN 'clinician' WHEN 'complaint__c' THEN 'complaint'
        WHEN 'trial_site__c' THEN 'trial site' WHEN 'literature__c' THEN 'literature' ELSE 'other' END)::varchar(20) AS safety_report_source_type,
  si.source_reference__c::varchar(40) AS safety_report_source_identifier,
  si.patient_pseudonym__c::varchar(40) AS patient_pseudonym_identifier,
  p.product_code__c::varchar(20) AS product_code,
  si.batch_number__c::varchar(40) AS batch_identifier,
  si.trial_reference__c::varchar(40) AS clinical_trial_identifier,
  si.event_description__c AS adverse_event_description,
  si.safety_case_reference__c::varchar(40) AS safety_case_identifier
FROM veeva_qms.safety_intake__c si
JOIN veeva_qms.product__v p ON p.id = si.product__c
