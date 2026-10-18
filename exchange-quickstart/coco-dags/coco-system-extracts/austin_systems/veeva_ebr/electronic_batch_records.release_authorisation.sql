-- Extract: Veeva Vault EBR (Austin) -> Electronic Batch Records / release_authorisation
-- Source: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Target: coco_data_hub.electronic_batch_records.release_authorisation
-- batch_release__c joined to batch__v and the certifying user.
SELECT
  b.name__v::varchar(40) AS batch_identifier,
  r.market__c::varchar(8) AS market_code,
  r.released_quantity__c AS batch_released_quantity,
  r.certification_date__c AS batch_certification_date,
  split_part(u.username__sys, '@', 1)::varchar(40) AS batch_certifier_identifier
FROM veeva_ebr.batch_release__c r
JOIN veeva_ebr.batch__v b ON b.id = r.batch__c
JOIN veeva_ebr.user__sys u ON u.id = r.certified_by__c
WHERE r.decision__c = 'certified__c'
