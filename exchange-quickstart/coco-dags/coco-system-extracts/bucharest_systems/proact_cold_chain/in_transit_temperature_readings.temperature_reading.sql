-- Extract: Proact Cold Chain Monitor (Bucharest) -> In-Transit Temperature Readings / temperature_reading
-- Source: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Target: coco_data_hub.in_transit_temperature_readings.temperature_reading
-- Measurements taken during a trip, with the trip's despatch number; device class to logger / live monitor.
SELECT
  m.device_id::varchar(40) AS device_identifier,
  m.measured_at AS device_reading_timestamp,
  t.shipment_ref::varchar(40) AS shipment_identifier,
  m.temp_c::double precision AS device_reading_temperature,
  m.location_label::varchar(120) AS device_location,
  (CASE d.device_class WHEN 'LIVE' THEN 'live monitor' ELSE 'logger' END)::varchar(20) AS device_type
FROM proact_cold_chain.measurement m
JOIN proact_cold_chain.trip t ON t.trip_id = m.trip_id
JOIN proact_cold_chain.device d ON d.device_id = m.device_id
