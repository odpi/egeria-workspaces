-- Extract: Veeva Vault QMS (Austin) -> Batch Certification Decisions / certification_decision
-- Source: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Target: coco_data_hub.batch_certification_decisions.certification_decision
-- batch_disposition__c (decisions on batches with a linked deviation) joined to decider and quality event.
SELECT
  d.batch_number__c::varchar(40) AS batch_identifier,
  d.market__c::varchar(8) AS market_code,
  split_part(u.username__sys, '@', 1)::varchar(40) AS batch_certifier_identifier,
  d.decision_date__c AS batch_certification_date,
  replace(d.decision__c, '__c', '')::varchar(20) AS batch_certification_status,
  d.released_quantity__c AS batch_released_quantity,
  d.record_complete__c AS batch_record_complete_flag,
  q.name__v::varchar(40) AS deviation_identifier,
  d.notes__c AS batch_certification_notes,
  d.storage_conditions__c AS shipment_storage_description
FROM veeva_qms.batch_disposition__c d
JOIN veeva_qms.user__sys u ON u.id = d.decided_by__c
LEFT JOIN veeva_qms.quality_event__qdm q ON q.id = d.quality_event__c
