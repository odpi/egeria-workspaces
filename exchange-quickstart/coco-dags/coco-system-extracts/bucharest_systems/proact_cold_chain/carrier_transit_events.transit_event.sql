-- Extract: Proact Cold Chain Monitor (Bucharest) -> Carrier Transit Events / transit_event
-- Source: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Target: coco_data_hub.carrier_transit_events.transit_event
-- Tracked trip events of live monitors and logger start/stop (handover and delivery confirmation come from the MES);
-- event codes translated.
SELECT
  t.shipment_ref::varchar(40) AS shipment_identifier,
  (CASE e.event_code WHEN 'DEPARTED' THEN 'departed' WHEN 'ARRIVED' THEN 'arrived' WHEN 'DELAYED' THEN 'delayed'
        WHEN 'SIGNAL_LOST' THEN 'tracking lost' WHEN 'LOGGER_STARTED' THEN 'logger started'
        WHEN 'LOGGER_STOPPED' THEN 'logger stopped' ELSE lower(e.event_code) END)::varchar(20) AS shipment_transit_event_type,
  e.event_at AS shipment_transit_event_timestamp,
  t.carrier_ref::varchar(40) AS carrier_identifier,
  e.location_label::varchar(120) AS shipment_transit_event_location,
  e.message AS shipment_transit_event_description
FROM proact_cold_chain.trip_event e
JOIN proact_cold_chain.trip t ON t.trip_id = e.trip_id
