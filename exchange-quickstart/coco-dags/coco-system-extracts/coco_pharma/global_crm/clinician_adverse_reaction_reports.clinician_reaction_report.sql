-- Extract: Global customer ordering system (Coco core) -> Clinician Adverse Reaction Reports / clinician_reaction_report
-- Source: coco_pharma.global_crm (System::globalCRM)
-- Target: coco_data_hub.clinician_adverse_reaction_reports.clinician_reaction_report
-- adverse_reaction__c; free-typed severity normalised to capitalised words.
SELECT
  r.name::varchar(40)                   AS adverse_event_identifier,
  r.reported_date__c                    AS adverse_event_reported_date,
  r.patient_reference__c::varchar(40)   AS patient_pseudonym_identifier,
  r.reporter__c::varchar(40)            AS clinician_identifier,
  r.product_code__c::varchar(20)        AS product_code,
  r.batch_number__c::varchar(40)        AS batch_identifier,
  r.description__c                      AS adverse_event_description,
  initcap(r.severity__c)::varchar(20)   AS adverse_event_reported_severity
FROM global_crm.adverse_reaction__c r
