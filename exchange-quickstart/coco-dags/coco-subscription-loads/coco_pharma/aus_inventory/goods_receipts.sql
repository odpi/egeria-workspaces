-- Subscription: coco_aus_inventory__goods_receipts - Austin Inventory (Coco core) receives Goods Receipts
-- Destination: coco_pharma.aus_inventory (System::aus-inventory)
-- Why it subscribes: Material Quarantine Dispositions depends on it (place in quarantine)
-- Keeps nothing: Austin Inventory receives Coco's materials at the Austin site itself (receiving_log,
-- rcv_inspection), so its receipts and inspections come back as rows it already holds.  The Austin site's own
-- SAP receipts (plant AUS1, Austin suppliers) are Austin's stock, which this system does not track, and the
-- depots' and EKG's receipts are for other locations.

UPDATE incoming_goods_receipt r SET discard_reason = 'Austin site receipt - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM aus_inventory.receiving_log l WHERE l.rcv_no = r.goods_receipt_identifier);
UPDATE incoming_goods_receipt SET discard_reason = 'Austin''s own SAP receipt - Austin stock is not tracked by Austin Inventory'
 WHERE discard_reason IS NULL AND warehouse_code IN ('AUS1', 'AUS2');
UPDATE incoming_goods_receipt SET discard_reason = 'receipt at another location' WHERE discard_reason IS NULL;

UPDATE incoming_receipt_inspection i SET discard_reason = 'inspection recorded in Austin Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM aus_inventory.rcv_inspection n WHERE n.rcv_no = i.goods_receipt_identifier AND n.insp_date = i.goods_receipt_inspection_date);
UPDATE incoming_receipt_inspection SET discard_reason = 'inspection of a receipt at another location' WHERE discard_reason IS NULL;
