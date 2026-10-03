-- Extract: Siemens Opcenter MES (Bucharest) -> Electronic Batch Records / batch_record_section
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.electronic_batch_records.batch_record_section
-- ebrsectionref joined to container; section type codes to words; interface partner name to the source system's
-- qualified name.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  r.externalref::varchar(40) AS batch_record_section_reference_identifier,
  (CASE r.sectiontype WHEN 'EXECUTION' THEN 'execution record' WHEN 'PROCESSDATA' THEN 'process parameters'
        WHEN 'LABRESULTS' THEN 'laboratory results' WHEN 'DEVIATION' THEN 'deviation disposition'
        WHEN 'SIGNATURE' THEN 'signature authority' ELSE lower(r.sectiontype) END)::varchar(40) AS batch_record_section_type,
  (CASE r.sourcesystem WHEN 'OPCENTER' THEN 'SoftwareServer::SYS-003::Siemens Opcenter MES' WHEN 'FACTORYTALK' THEN 'SoftwareServer::SYS-015::Rockwell FactoryTalk'
        WHEN 'LABWARE' THEN 'SoftwareServer::SYS-004::LIMS LabWare Enterprise' WHEN 'VEEVA_QMS' THEN 'SoftwareServer::SYS-002::Veeva Vault QMS'
        ELSE r.sourcesystem END)::varchar(60) AS system_identifier,
  r.receiveddate AS batch_record_section_received_timestamp
FROM opcenter_mes.ebrsectionref r
JOIN opcenter_mes.container c ON c.containerid = r.containerid
