-- Subscription: coco_austin_haz_mat__goods_inventory_stock - Austin HazMat Inventory (Coco core) receives Goods Inventory Stock
-- Destination: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Why it subscribes: Hazardous Material Holdings depends on it (hazardous holdings)
-- Keeps the stock positions at Coco's Austin site locations (AUS- locations of Austin Inventory) in stock_check
-- (NEW), checked against storage_location_qty, which feeds Hazardous Material Holdings and is counted by the
-- site.  Discards Austin's own SAP stock (AUS1, AUS2 - Austin's EHS covers it), other sites' and EKG's stock,
-- and stock movements and issues.

UPDATE incoming_stock_position SET discard_reason = 'Austin''s own SAP stock - covered by Austin''s EHS systems'
 WHERE warehouse_code IN ('AUS1', 'AUS2');
UPDATE incoming_stock_position SET discard_reason = 'not at the Austin site'
 WHERE discard_reason IS NULL AND warehouse_code NOT LIKE 'AUS-%';

INSERT INTO austin_haz_mat.stock_check (item_no, storage_loc, lot_no, qty_on_hand, as_of)
SELECT p.product_code, p.warehouse_code, coalesce(p.lot_identifier, '-'), p.stock_level, p.stock_current_timestamp
  FROM incoming_stock_position p
 WHERE p.discard_reason IS NULL
ON CONFLICT (item_no, storage_loc, lot_no) DO UPDATE SET qty_on_hand = EXCLUDED.qty_on_hand, as_of = EXCLUDED.as_of;

UPDATE incoming_stock_movement SET discard_reason = 'holdings are checked against stock positions, not movements';
UPDATE incoming_material_issue SET discard_reason = 'holdings are checked against stock positions, not issues';
