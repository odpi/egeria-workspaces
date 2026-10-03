-- Subscription: buc_proact_cold_chain__carrier_transit_events - Proact Cold Chain Monitor (Bucharest) receives Carrier Transit Events
-- Destination: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Why it subscribes: Cold Chain Transit Records depends on it (carrier journey events)
-- Keeps the custody events the MES reports for EKG despatches that have a monitored trip (handover to the carrier,
-- delivery confirmation) in the new table partner_event, shown on the trip timeline; the monitor's own trip events are
-- already held and are discarded (no feedback loop).  EKG despatches without a trip are discarded, as are other
-- companies' shipments (Coco group data - EKG is not yet integrated).
UPDATE incoming_transit_event i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM proact_cold_chain.trip_event e JOIN proact_cold_chain.trip t ON t.trip_id = e.trip_id
                WHERE t.shipment_ref = i.shipment_identifier AND e.event_at = i.shipment_transit_event_timestamp);
UPDATE incoming_transit_event i SET discard_reason = 'no monitored trip for this shipment'
 WHERE i.discard_reason IS NULL AND i.shipment_identifier LIKE 'EXP-%'
   AND NOT EXISTS (SELECT 1 FROM proact_cold_chain.trip t WHERE t.shipment_ref = i.shipment_identifier);
UPDATE incoming_transit_event i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM proact_cold_chain.trip t WHERE t.shipment_ref = i.shipment_identifier);

INSERT INTO proact_cold_chain.partner_event (shipment_ref, event_code, event_at, carrier_ref, location_label, message, source)
SELECT i.shipment_identifier, upper(replace(i.shipment_transit_event_type, ' ', '_')), i.shipment_transit_event_timestamp,
       left(i.carrier_identifier, 10), i.shipment_transit_event_location, i.shipment_transit_event_description, 'OPCENTER'
  FROM incoming_transit_event i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipment_ref, event_code, event_at) DO UPDATE
   SET carrier_ref = EXCLUDED.carrier_ref, location_label = EXCLUDED.location_label, message = EXCLUDED.message;
