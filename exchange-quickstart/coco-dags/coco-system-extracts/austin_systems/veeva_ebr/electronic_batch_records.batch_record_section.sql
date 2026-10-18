-- Extract: Veeva Vault EBR (Austin) -> Electronic Batch Records / batch_record_section
-- Source: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Target: coco_data_hub.electronic_batch_records.batch_record_section
-- batch_record_section__c joined to batch__v; section types translated and source system codes mapped to system
-- qualified names.
SELECT
  b.name__v::varchar(40) AS batch_identifier,
  s.section_reference__c::varchar(40) AS batch_record_section_reference_identifier,
  replace(replace(s.section_type__c, '__c', ''), '_', ' ')::varchar(40) AS batch_record_section_type,
  (CASE s.source_system__c
     WHEN 'OPCENTER' THEN 'SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601' WHEN 'FACTORYTALK' THEN 'SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610'
     WHEN 'KAFKA' THEN 'SoftwareServer::AUS-SYS-007::KAFKA-AUS-001' WHEN 'LABWARE' THEN 'SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820'
     WHEN 'VAULT_QMS' THEN 'SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901' ELSE 'SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301' END)::varchar(60) AS system_identifier,
  s.received_datetime__c AS batch_record_section_received_timestamp
FROM veeva_ebr.batch_record_section__c s
JOIN veeva_ebr.batch__v b ON b.id = s.batch__c
