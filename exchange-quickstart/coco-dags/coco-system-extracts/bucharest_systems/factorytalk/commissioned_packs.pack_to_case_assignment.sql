-- Extract: Rockwell FactoryTalk (Bucharest) -> Commissioned Packs / pack_to_case_assignment
-- Source: bucharest_systems.factorytalk (SoftwareServer::SYS-015::Rockwell FactoryTalk)
-- Target: coco_data_hub.commissioned_packs.pack_to_case_assignment
-- AGGREGATE events: pack GTIN.serial to parent case SSCC.
SELECT
  (a.gtin || '.' || a.serial_no)::varchar(40) AS pack_serial_number,
  a.parent_sscc::varchar(40) AS case_serial_number,
  a.event_time AS pack_aggregated_timestamp
FROM factorytalk.line_serial_event a
WHERE a.event_type = 'AGGREGATE'
