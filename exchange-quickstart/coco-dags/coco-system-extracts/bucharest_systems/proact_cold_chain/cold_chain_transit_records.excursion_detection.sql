-- Extract: Proact Cold Chain Monitor (Bucharest) -> Cold Chain Transit Records / excursion_detection
-- Source: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Target: coco_data_hub.cold_chain_transit_records.excursion_detection
-- Alarms raised during a trip (a signal loss is a data-gap excursion); duration in minutes.
SELECT
  a.alarm_id::varchar(40) AS excursion_identifier,
  t.shipment_ref::varchar(40) AS shipment_identifier,
  a.started_at AS excursion_start_timestamp,
  a.ended_at AS excursion_end_timestamp,
  (extract(epoch FROM a.ended_at - a.started_at) / 60)::integer AS excursion_duration,
  a.peak_value::double precision AS excursion_maximum_temperature,
  (CASE a.alarm_type WHEN 'TEMP_HIGH' THEN 'temperature high' WHEN 'TEMP_LOW' THEN 'temperature low'
        ELSE 'data gap' END)::varchar(20) AS excursion_type
FROM proact_cold_chain.alarm a
JOIN proact_cold_chain.trip t ON t.trip_id = a.trip_id
WHERE a.ended_at IS NOT NULL
