-- Subscription: coco_mfctrl9482__goods_inventory_stock - Austin Manufacturing Control System (Coco core) receives Goods Inventory Stock
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Batch Execution Records depends on it (issue material)
-- Keeps the issues of material to the shared Coco batches (A26- batches of 3000, 2050 and 9000) in mfc_issue (NEW),
-- whether issued from Coco's Austin Inventory or from the Austin site's own SAP stores.  Discards stock positions
-- and other movements (kept by the inventory systems) and issues to other batches, including Austin's own
-- products made on the same site.

UPDATE incoming_stock_position SET discard_reason = 'stock levels are kept by the inventory systems, not the control system';
UPDATE incoming_stock_movement SET discard_reason = 'stock movements are kept by the inventory systems, not the control system';

UPDATE incoming_material_issue m SET discard_reason = 'issue to a batch that is not a shared Coco batch' WHERE NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = m.batch_identifier) OR m.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_issue (movement_id, batch_id, item_cd, lot_no, qty_issued, lot_status)
SELECT m.stock_movement_identifier, m.batch_identifier, m.raw_material_code, m.lot_identifier, m.raw_material_issued_quantity,
       upper(m.lot_quarantine_status)
  FROM incoming_material_issue m
 WHERE m.discard_reason IS NULL
ON CONFLICT (movement_id) DO UPDATE SET batch_id = EXCLUDED.batch_id, item_cd = EXCLUDED.item_cd, lot_no = EXCLUDED.lot_no,
       qty_issued = EXCLUDED.qty_issued, lot_status = EXCLUDED.lot_status;
