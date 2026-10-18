-- Extract: Rockwell FactoryTalk SCADA (Austin) -> Commissioned Packs / commissioned_pack
-- Source: austin_systems.factorytalk_scada (SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610)
-- Target: coco_data_hub.commissioned_packs.commissioned_pack
-- COMMISSION events; pack code is the NDC recovered from the GTIN; verified when a VERIFY event exists; YYMMDD expiry
-- to date; serial is GTIN.serial (SGTIN).
SELECT
  (c.gtin || '.' || c.serial_no)::varchar(40) AS pack_serial_number,
  (substr(c.gtin, 4, 5) || '-' || substr(c.gtin, 9, 3) || '-' || substr(c.gtin, 12, 2))::varchar(20) AS pack_code,
  c.lot::varchar(40) AS batch_identifier,
  to_date('20' || c.expiry_yymmdd, 'YYYYMMDD') AS pack_expiry_date,
  c.event_time AS pack_commissioned_timestamp,
  EXISTS (SELECT 1 FROM factorytalk_scada.line_serial_event v
          WHERE v.event_type = 'VERIFY' AND v.gtin = c.gtin AND v.serial_no = c.serial_no) AS pack_verified_flag,
  c.line_id::varchar(40) AS equipment_identifier
FROM factorytalk_scada.line_serial_event c
WHERE c.event_type = 'COMMISSION'
