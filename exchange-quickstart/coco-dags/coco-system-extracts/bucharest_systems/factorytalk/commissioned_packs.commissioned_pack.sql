-- Extract: Rockwell FactoryTalk (Bucharest) -> Commissioned Packs / commissioned_pack
-- Source: bucharest_systems.factorytalk (SoftwareServer::SYS-015::Rockwell FactoryTalk)
-- Target: coco_data_hub.commissioned_packs.commissioned_pack
-- COMMISSION events; pack code is the GTIN (the EU FMD product code); verified when a VERIFY event exists; YYMMDD
-- expiry to date; serial is GTIN.serial.
SELECT
  (c.gtin || '.' || c.serial_no)::varchar(40) AS pack_serial_number,
  c.gtin::varchar(20) AS pack_code,
  c.lot::varchar(40) AS batch_identifier,
  to_date('20' || c.expiry_yymmdd, 'YYYYMMDD') AS pack_expiry_date,
  c.event_time AS pack_commissioned_timestamp,
  EXISTS (SELECT 1 FROM factorytalk.line_serial_event v
          WHERE v.event_type = 'VERIFY' AND v.gtin = c.gtin AND v.serial_no = c.serial_no) AS pack_verified_flag,
  c.line_id::varchar(40) AS equipment_identifier
FROM factorytalk.line_serial_event c
WHERE c.event_type = 'COMMISSION'
