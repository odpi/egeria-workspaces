-- Subscription: buc_opcenter_mes__carrier_transit_events - Siemens Opcenter MES (Bucharest) receives Carrier Transit Events
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Cold Chain Transit Records depends on it (carrier journey events)
-- Keeps the journey events the cold chain monitor reports for shipments this MES monitors (shipmentmonitor) in the new
-- table extshipmentevent; the handover and delivery events are the MES's own (shipmenteventhistory) and are discarded
-- (no feedback loop).  EKG despatches the MES does not monitor are discarded, as are other companies' shipments (Coco
-- group data - EKG is not yet integrated).
UPDATE incoming_transit_event i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.shipmenteventhistory e
                WHERE e.shipmentname = i.shipment_identifier AND e.eventdate = i.shipment_transit_event_timestamp);
UPDATE incoming_transit_event i SET discard_reason = 'shipment not monitored by the MES'
 WHERE i.discard_reason IS NULL AND i.shipment_identifier LIKE 'EXP-%'
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier);
UPDATE incoming_transit_event i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier);

INSERT INTO opcenter_mes.extshipmentevent (shipmentname, eventtype, eventdate, carriervendor, location, comments, sourcesystem)
SELECT i.shipment_identifier, i.shipment_transit_event_type, i.shipment_transit_event_timestamp, left(i.carrier_identifier, 10),
       i.shipment_transit_event_location, i.shipment_transit_event_description, 'PROACT'
  FROM incoming_transit_event i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipmentname, eventtype, eventdate) DO UPDATE
   SET carriervendor = EXCLUDED.carriervendor, location = EXCLUDED.location, comments = EXCLUDED.comments;
