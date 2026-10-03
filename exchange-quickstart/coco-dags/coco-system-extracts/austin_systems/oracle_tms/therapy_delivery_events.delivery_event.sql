-- Extract: Oracle TMS (Austin) -> Therapy Delivery Events / delivery_event
-- Source: austin_systems.oracle_tms (SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004)
-- Target: coco_data_hub.therapy_delivery_events.delivery_event
-- ie_shipmentstatus events on patient therapy shipments (those carrying an ORDER_NO reference) except administration;
-- status codes translated; order, batch, patient and storage from shipment_refnum; location from the status location.
SELECT
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.BATCH_NO' LIMIT 1)::varchar(40) AS batch_identifier,
  (CASE e.status_code_gid WHEN 'AUS.RELEASED' THEN 'released' WHEN 'AUS.PICKED_UP' THEN 'dispatched'
        WHEN 'AUS.DELIVERED' THEN 'delivered' ELSE 'in transit' END)::varchar(20) AS shipment_event_type,
  e.event_date AS shipment_event_timestamp,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.PATIENT_REF' LIMIT 1)::varchar(40) AS patient_pseudonym_identifier,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.ORDER_NO' LIMIT 1)::varchar(40) AS order_identifier,
  (l.location_name || ', ' || l.city)::varchar(120) AS shipment_event_location,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.STORAGE' LIMIT 1) AS shipment_storage_description
FROM oracle_tms.ie_shipmentstatus e
JOIN oracle_tms.shipment s ON s.shipment_gid = e.shipment_gid
LEFT JOIN oracle_tms.location l ON l.location_gid = e.status_location_gid
WHERE e.status_code_gid <> 'AUS.ADMINISTERED'
  AND EXISTS (SELECT 1 FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.ORDER_NO')
