-- Extract: Salesforce Sales Cloud CRM (Austin) -> Clinician Adverse Reaction Reports / clinician_reaction_report
-- Source: austin_systems.salesforce_crm (SoftwareServer::AUS-SYS-016::SN-CRM-AU-20200901)
-- Target: coco_data_hub.clinician_adverse_reaction_reports.clinician_reaction_report
-- adverse_reaction_report__c joined to the reporting contact's NPI.
SELECT
  r.name::varchar(40) AS adverse_event_identifier,
  r.createddate::date AS adverse_event_reported_date,
  r.patient_pseudonym__c::varchar(40) AS patient_pseudonym_identifier,
  c.npi__c::varchar(40) AS clinician_identifier,
  r.product_code__c::varchar(20) AS product_code,
  r.batch_number__c::varchar(40) AS batch_identifier,
  r.reaction_description__c AS adverse_event_description,
  lower(r.reported_severity__c)::varchar(20) AS adverse_event_reported_severity
FROM salesforce_crm.adverse_reaction_report__c r
JOIN salesforce_crm.contact c ON c.sfid = r.reporter__c
WHERE NOT r.isdeleted
