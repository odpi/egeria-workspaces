-- Subscription: coco_manufacturing_planning__patient_sample_consignments - Global Manufacturing Planning (Coco core) receives Patient Sample Consignments
-- Destination: coco_pharma.manufacturing_planning (System::manufacturing-planning)
-- Why it subscribes: Personalised Manufacturing Schedule depends on it (patient material received)
-- Keeps consignments of patient material for Coco's personalised orders (globalCRM SO- orders) in inbd_asn (NEW),
-- the advance notice the site books the material in against (inbd_matl, which feeds the Personalised
-- Manufacturing Schedule, is written on arrival, not from this feed).  Discards consignments for Austin/EKG
-- orders, whose material goes to the acquired estates' own sites.  No system supplies this product yet.

UPDATE incoming_sample_consignment SET discard_reason = 'Austin or EKG personalised order - material goes to the acquired estate''s site'
 WHERE order_identifier NOT LIKE 'SO-%';

INSERT INTO manufacturing_planning.inbd_asn (consignment_no, cust_ord_ref, patient_ref, origin_site, collected_ts, dispatched_ts,
       delivered_ts, viab_hrs, arr_note, carrier_ref)
SELECT c.shipment_identifier, c.order_identifier, c.patient_pseudonym_identifier, c.sample_collection_location,
       c.sample_collection_timestamp, c.shipment_dispatch_timestamp, c.shipment_delivery_timestamp, c.sample_viable_duration,
       c.shipment_arrival_description, c.carrier_identifier
  FROM incoming_sample_consignment c
 WHERE c.discard_reason IS NULL
ON CONFLICT (consignment_no) DO UPDATE SET cust_ord_ref = EXCLUDED.cust_ord_ref, patient_ref = EXCLUDED.patient_ref,
       origin_site = EXCLUDED.origin_site, collected_ts = EXCLUDED.collected_ts, dispatched_ts = EXCLUDED.dispatched_ts,
       delivered_ts = EXCLUDED.delivered_ts, viab_hrs = EXCLUDED.viab_hrs, arr_note = EXCLUDED.arr_note,
       carrier_ref = EXCLUDED.carrier_ref;
