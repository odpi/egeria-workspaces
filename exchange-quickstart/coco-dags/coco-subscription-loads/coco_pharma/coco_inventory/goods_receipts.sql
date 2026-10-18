-- Subscription: coco_inventory__goods_receipts - Coco Inventory (Coco core) receives Goods Receipts
-- Destination: coco_pharma.coco_inventory (System::coco-inventory)
-- Why it subscribes: Material Quarantine Dispositions depends on it (place in quarantine)
-- Keeps the depots' receipts at Coco's own locations (Winchester, Edmonton, Kansas City) in inv_rcpt_ntf (NEW),
-- from which each lot is booked into quarantine (inv_qrn, which feeds Material Quarantine Dispositions and so is
-- not written from the feed).  Discards receipts at the Austin site (kept by Austin Inventory), Austin's own SAP
-- receipts (AUS1) and EKG's; receipt inspections are recorded in Coco Inventory itself, so Coco ones come back
-- as rows it already holds and the rest are other estates'.

UPDATE incoming_goods_receipt SET discard_reason = 'Austin site receipt - kept by Austin Inventory' WHERE warehouse_code LIKE 'AUS-%';
UPDATE incoming_goods_receipt r SET discard_reason = 'receipt at an Austin or EKG warehouse - not a Coco location'
 WHERE r.discard_reason IS NULL AND NOT (r.warehouse_code IN (SELECT loc_cd FROM coco_inventory.inv_loc) OR r.warehouse_code ~ '^(WIN|EDM|KC)-');

INSERT INTO coco_inventory.inv_rcpt_ntf (grn_ref, po_ref, supp_no, item_cd, lot_no, rcpt_dt, qty, loc_cd, cert_ref)
SELECT r.goods_receipt_identifier, r.order_identifier, r.supplier_identifier, r.raw_material_code, r.lot_identifier,
       r.goods_receipt_date, r.goods_receipt_quantity, r.warehouse_code, r.certificate_identifier
  FROM incoming_goods_receipt r
 WHERE r.discard_reason IS NULL
ON CONFLICT (grn_ref) DO UPDATE SET po_ref = EXCLUDED.po_ref, supp_no = EXCLUDED.supp_no, item_cd = EXCLUDED.item_cd,
       lot_no = EXCLUDED.lot_no, rcpt_dt = EXCLUDED.rcpt_dt, qty = EXCLUDED.qty, loc_cd = EXCLUDED.loc_cd, cert_ref = EXCLUDED.cert_ref;

UPDATE incoming_receipt_inspection i SET discard_reason = 'inspection recorded in Coco Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_inventory.inv_insp n WHERE n.grn_ref = i.goods_receipt_identifier AND n.insp_dt = i.goods_receipt_inspection_date);
UPDATE incoming_receipt_inspection i SET discard_reason = 'inspection of a receipt that is not at a Coco location'
 WHERE i.discard_reason IS NULL;
