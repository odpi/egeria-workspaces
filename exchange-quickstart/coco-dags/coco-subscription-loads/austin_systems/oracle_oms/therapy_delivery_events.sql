-- Subscription: aus_oracle_oms__therapy_delivery_events - Oracle Order Management (Austin) receives Therapy Delivery Events
-- Destination: austin_systems.oracle_oms (SoftwareServer::AUS-SYS-011::SN-OMS-AU-20200310)
-- Why it subscribes: Treatment Invoices depends on it (fulfilment confirmed)
-- Keeps the delivery and administration confirmations of Austin therapy shipments for orders it holds (source order
-- number = portal order) in the NEW doo_fulfillment_event_int interface table, from which the fulfilment line is
-- closed and AutoInvoice runs. In-transit tracking events and events for orders it does not hold are discarded.

UPDATE incoming_delivery_event i SET discard_reason = 'other estate: not an Austin therapy batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_delivery_event i SET discard_reason = 'tracking event: fulfilment not yet confirmed'
 WHERE i.discard_reason IS NULL AND i.shipment_event_type <> 'delivered';
UPDATE incoming_delivery_event i SET discard_reason = 'order not held in Order Management'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM oracle_oms.doo_headers_all h WHERE h.source_order_number = i.order_identifier);
INSERT INTO oracle_oms.doo_fulfillment_event_int
       (header_id, lot_number, event_code, event_date, event_location, patient_ref, source_reference)
SELECT DISTINCT ON (h.header_id, i.batch_identifier) h.header_id, i.batch_identifier, 'DELIVERED',
       i.shipment_event_timestamp, i.shipment_event_location, i.patient_pseudonym_identifier, i.order_identifier
  FROM incoming_delivery_event i JOIN oracle_oms.doo_headers_all h ON h.source_order_number = i.order_identifier
 WHERE i.discard_reason IS NULL
 ORDER BY h.header_id, i.batch_identifier, i.shipment_event_timestamp DESC
ON CONFLICT (header_id, lot_number, event_code) DO UPDATE SET
       event_date = EXCLUDED.event_date, event_location = EXCLUDED.event_location,
       patient_ref = EXCLUDED.patient_ref, source_reference = EXCLUDED.source_reference;

UPDATE incoming_administration_confirmation i SET discard_reason = 'other estate: not an Austin therapy batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_administration_confirmation i SET discard_reason = 'order not held in Order Management'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM oracle_oms.doo_headers_all h WHERE h.source_order_number = i.order_identifier);
INSERT INTO oracle_oms.doo_fulfillment_event_int
       (header_id, lot_number, event_code, event_date, event_location, patient_ref, source_reference)
SELECT h.header_id, i.batch_identifier, 'ADMINISTERED', i.treatment_administration_timestamp,
       'NPI ' || i.clinician_identifier, i.patient_pseudonym_identifier, i.order_identifier
  FROM incoming_administration_confirmation i
  JOIN oracle_oms.doo_headers_all h ON h.source_order_number = i.order_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (header_id, lot_number, event_code) DO UPDATE SET
       event_date = EXCLUDED.event_date, event_location = EXCLUDED.event_location,
       patient_ref = EXCLUDED.patient_ref, source_reference = EXCLUDED.source_reference;
