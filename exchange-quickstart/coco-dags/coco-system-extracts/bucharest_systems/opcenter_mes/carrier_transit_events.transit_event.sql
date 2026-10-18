-- Extract: Siemens Opcenter MES (Bucharest) -> Carrier Transit Events / transit_event
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.carrier_transit_events.transit_event
-- Dispatch-side events from shipmenteventhistory (handover and proof of delivery); carrier is the SAP vendor number
-- without leading zeros.
SELECT
  e.shipmentname::varchar(40) AS shipment_identifier,
  (CASE e.eventtype WHEN 'HandedToCarrier' THEN 'handed over' WHEN 'DeliveryConfirmed' THEN 'delivery confirmed'
        ELSE lower(e.eventtype) END)::varchar(20) AS shipment_transit_event_type,
  e.eventdate AS shipment_transit_event_timestamp,
  ltrim(e.carriervendor, '0')::varchar(40) AS carrier_identifier,
  e.location::varchar(120) AS shipment_transit_event_location,
  e.comments AS shipment_transit_event_description
FROM opcenter_mes.shipmenteventhistory e
