-- Extract: Veeva Vault EBR (Austin) -> Electronic Batch Records / batch_record
-- Source: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Target: coco_data_hub.electronic_batch_records.batch_record
-- batch__v joined to product__v; Vault status mapped to awaiting review / certified / rejected.
SELECT
  b.name__v::varchar(40) AS batch_identifier,
  p.product_code__c::varchar(20) AS product_code,
  b.patient_pseudonym__c::varchar(40) AS patient_pseudonym_identifier,
  b.start_datetime__c AS batch_start_timestamp,
  b.end_datetime__c AS batch_end_timestamp,
  b.quantity__c AS batch_quantity,
  b.record_complete__c AS batch_record_complete_flag,
  (CASE b.status__v WHEN 'certified__c' THEN 'certified' WHEN 'rejected__c' THEN 'rejected' ELSE 'awaiting review' END)::varchar(20) AS batch_certification_status
FROM veeva_ebr.batch__v b
JOIN veeva_ebr.product__v p ON p.id = b.product__c
