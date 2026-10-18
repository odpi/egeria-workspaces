-- Subscription: coco_ledgers__therapy_delivery_events - Coco Ledgers (Coco core) receives Therapy Delivery Events
-- Destination: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Why it subscribes: Treatment Invoices depends on it (fulfilment confirmed)
-- Keeps the fulfilment confirmations of Coco's personalised therapy orders (globalCRM SO- orders): the delivered
-- event and the administration confirmation go to ar_fulfilment (NEW), which releases the receivable and fixes
-- the delivery date for revenue recognition; other shipment events (released, dispatched, in transit) are not
-- accounting events.  Discards Austin's own cell therapy orders (TO- orders, product AU-7710), invoiced by Austin.

UPDATE incoming_delivery_event SET discard_reason = 'Austin therapy order - invoiced by the Austin estate'
 WHERE order_identifier NOT LIKE 'SO-%';
UPDATE incoming_delivery_event SET discard_reason = 'shipment progress event - only delivery confirms fulfilment'
 WHERE discard_reason IS NULL AND shipment_event_type <> 'delivered';

INSERT INTO coco_ledgers.ar_fulfilment (order_ref, batch_no, event_typ, event_at, event_loc)
SELECT DISTINCT ON (e.order_identifier, e.batch_identifier)
       e.order_identifier, e.batch_identifier, 'DELIVERED', e.shipment_event_timestamp, e.shipment_event_location
  FROM incoming_delivery_event e
 WHERE e.discard_reason IS NULL
 ORDER BY e.order_identifier, e.batch_identifier, e.shipment_event_timestamp DESC
ON CONFLICT (order_ref, batch_no, event_typ) DO UPDATE SET event_at = EXCLUDED.event_at, event_loc = EXCLUDED.event_loc;

UPDATE incoming_administration_confirmation SET discard_reason = 'Austin therapy order - invoiced by the Austin estate'
 WHERE order_identifier NOT LIKE 'SO-%';

INSERT INTO coco_ledgers.ar_fulfilment (order_ref, batch_no, event_typ, event_at, event_loc)
SELECT DISTINCT ON (a.order_identifier, a.batch_identifier)
       a.order_identifier, a.batch_identifier, 'ADMINISTERED', a.treatment_administration_timestamp, NULL
  FROM incoming_administration_confirmation a
 WHERE a.discard_reason IS NULL
 ORDER BY a.order_identifier, a.batch_identifier, a.treatment_administration_timestamp DESC
ON CONFLICT (order_ref, batch_no, event_typ) DO UPDATE SET event_at = EXCLUDED.event_at;
