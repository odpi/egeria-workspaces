-- Extract: Veeva Vault EBR (Austin) -> Batch Certification Decisions / certification_decision
-- Source: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Target: coco_data_hub.batch_certification_decisions.certification_decision
-- batch_release__c for batches with no deviation-disposition section (decisions on batches with a linked deviation are
-- taken in Veeva QMS).
SELECT
  b.name__v::varchar(40) AS batch_identifier,
  r.market__c::varchar(8) AS market_code,
  split_part(u.username__sys, '@', 1)::varchar(40) AS batch_certifier_identifier,
  r.certification_date__c AS batch_certification_date,
  replace(r.decision__c, '__c', '')::varchar(20) AS batch_certification_status,
  r.released_quantity__c AS batch_released_quantity,
  b.record_complete__c AS batch_record_complete_flag,
  NULL::varchar(40) AS deviation_identifier,
  r.notes__c AS batch_certification_notes,
  r.storage_conditions__c AS shipment_storage_description
FROM veeva_ebr.batch_release__c r
JOIN veeva_ebr.batch__v b ON b.id = r.batch__c
JOIN veeva_ebr.user__sys u ON u.id = r.certified_by__c
WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.batch_record_section__c s
                  WHERE s.batch__c = b.id AND s.section_type__c = 'deviation_disposition__c')
