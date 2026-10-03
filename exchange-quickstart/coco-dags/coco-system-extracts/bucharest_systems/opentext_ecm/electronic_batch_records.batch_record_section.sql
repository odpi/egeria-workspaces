-- Extract: OpenText ECM (Bucharest) -> Electronic Batch Records / batch_record_section
-- Source: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Target: coco_data_hub.electronic_batch_records.batch_record_section
-- Signed batch record PDFs archived from the MES (category Dosar de lot, source OPCENTER); section reference = OTCS
-- node id.
SELECT
  b.valstr::varchar(40) AS batch_identifier,
  ('OTCS-' || d.dataid)::varchar(40) AS batch_record_section_reference_identifier,
  'signed batch record'::varchar(40) AS batch_record_section_type,
  'SoftwareServer::SYS-024::OpenText ECM'::varchar(60) AS system_identifier,
  d.createdate AS batch_record_section_received_timestamp
FROM opentext_ecm.dtree d
JOIN opentext_ecm.llattrdata b ON b.id = d.dataid AND b.defid = 3001 AND b.attrid = 2
JOIN opentext_ecm.llattrdata src ON src.id = d.dataid AND src.defid = 3001 AND src.attrid = 4
WHERE d.subtype = 144 AND src.valstr = 'OPCENTER'
