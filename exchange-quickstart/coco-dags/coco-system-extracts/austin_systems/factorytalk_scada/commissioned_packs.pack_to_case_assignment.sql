-- Extract: Rockwell FactoryTalk SCADA (Austin) -> Commissioned Packs / pack_to_case_assignment
-- Source: austin_systems.factorytalk_scada (SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610)
-- Target: coco_data_hub.commissioned_packs.pack_to_case_assignment
-- AGGREGATE events: pack SGTIN to parent case SSCC.
SELECT
  (a.gtin || '.' || a.serial_no)::varchar(40) AS pack_serial_number,
  a.parent_sscc::varchar(40) AS case_serial_number,
  a.event_time AS pack_aggregated_timestamp
FROM factorytalk_scada.line_serial_event a
WHERE a.event_type = 'AGGREGATE'
