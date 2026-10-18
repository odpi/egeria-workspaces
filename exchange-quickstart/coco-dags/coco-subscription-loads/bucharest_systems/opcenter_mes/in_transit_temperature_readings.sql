-- Subscription: buc_opcenter_mes__in_transit_temperature_readings - Siemens Opcenter MES (Bucharest) receives In-Transit Temperature Readings
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Cold Chain Transit Records depends on it (transit temperature record)
-- Keeps the logger readings of shipments this MES monitors (shipmentmonitor) in the new table shipmenttemperature, from
-- which the transit record is reviewed; the transit record's own min/max (an extract source) is not changed.  Readings
-- of EKG despatches the MES does not monitor are discarded, as are other companies' readings (Coco group data - EKG
-- is not yet integrated).
UPDATE incoming_temperature_reading i SET discard_reason = 'shipment not monitored by the MES'
 WHERE i.shipment_identifier LIKE 'EXP-%'
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier);
UPDATE incoming_temperature_reading i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier);

INSERT INTO opcenter_mes.shipmenttemperature (loggerid, readingdate, shipmentname, temperature, location, devicetype)
SELECT i.device_identifier, i.device_reading_timestamp, i.shipment_identifier, round(i.device_reading_temperature::numeric, 1),
       i.device_location, i.device_type
  FROM incoming_temperature_reading i
 WHERE i.discard_reason IS NULL AND i.device_reading_temperature IS NOT NULL
ON CONFLICT (loggerid, readingdate) DO UPDATE
   SET shipmentname = EXCLUDED.shipmentname, temperature = EXCLUDED.temperature, location = EXCLUDED.location,
       devicetype = EXCLUDED.devicetype;
UPDATE incoming_temperature_reading SET discard_reason = 'reading has no temperature'
 WHERE discard_reason IS NULL AND device_reading_temperature IS NULL;
