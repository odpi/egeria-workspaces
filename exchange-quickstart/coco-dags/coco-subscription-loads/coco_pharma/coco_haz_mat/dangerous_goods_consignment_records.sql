-- Subscription: coco_haz_mat__dangerous_goods_consignment_records - Coco HazMat Inventory (Coco core) receives Dangerous Goods Consignment Records
-- Destination: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Why it subscribes: Hazardous Material Holdings depends on it (consignment record)
-- Keeps the consignments despatched from Coco's depots (signed by Coco workers, CW- pseudonyms) in hm_consign
-- (NEW), used to reconcile hm_hold after hazardous material leaves a site.  Discards consignment documents (kept
-- by the depots), Austin's own shipments (its own distribution and EHS) and EKG's.

UPDATE incoming_consignment_declaration SET discard_reason = 'Austin or EKG shipment - not from a Coco depot'
 WHERE declaration_signatory_identifier NOT LIKE 'CW-%';

INSERT INTO coco_haz_mat.hm_consign (cons_ref, desp_dt, carr_ref, ship_to, un_no, qty, uom, signed_by, signed_ts, dg_cert)
SELECT c.shipment_identifier, c.shipment_dispatch_date, c.carrier_identifier, c.shipment_ship_to_address,
       c.transport_classification_code, c.shipment_quantity, c.shipment_unit, c.declaration_signatory_identifier,
       c.declaration_signed_timestamp, c.certificate_identifier
  FROM incoming_consignment_declaration c
 WHERE c.discard_reason IS NULL
ON CONFLICT (cons_ref) DO UPDATE SET desp_dt = EXCLUDED.desp_dt, carr_ref = EXCLUDED.carr_ref, ship_to = EXCLUDED.ship_to,
       un_no = EXCLUDED.un_no, qty = EXCLUDED.qty, uom = EXCLUDED.uom, signed_by = EXCLUDED.signed_by,
       signed_ts = EXCLUDED.signed_ts, dg_cert = EXCLUDED.dg_cert;

UPDATE incoming_consignment_document SET discard_reason = 'consignment documents are kept by the depots';
