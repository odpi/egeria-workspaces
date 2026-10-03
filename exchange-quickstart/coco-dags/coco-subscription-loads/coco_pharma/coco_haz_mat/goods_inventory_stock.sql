-- Subscription: coco_haz_mat__goods_inventory_stock - Coco HazMat Inventory (Coco core) receives Goods Inventory Stock
-- Destination: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Why it subscribes: Hazardous Material Holdings depends on it (hazardous holdings)
-- Keeps the stock positions at Coco's locations other than Austin (Winchester, Edmonton, Kansas City) in
-- hm_stk_chk (NEW), checked against hm_hold to find hazardous holdings not yet recorded; hm_hold itself feeds
-- Hazardous Material Holdings and is maintained by the site safety officers.  Discards positions at the Austin
-- site (Austin HazMat Inventory's), Austin's own and EKG's stock, and stock movements and issues.

UPDATE incoming_stock_position SET discard_reason = 'Austin site stock - checked by Austin HazMat Inventory'
 WHERE warehouse_code LIKE 'AUS-%';
UPDATE incoming_stock_position SET discard_reason = 'Austin or EKG stock - not a Coco location'
 WHERE discard_reason IS NULL AND warehouse_code !~ '^(WIN|EDM|KC)-';

INSERT INTO coco_haz_mat.hm_stk_chk (item_cd, loc_cd, lot_no, qty, upd_ts)
SELECT p.product_code, p.warehouse_code, coalesce(p.lot_identifier, '-'), p.stock_level, p.stock_current_timestamp
  FROM incoming_stock_position p
 WHERE p.discard_reason IS NULL
ON CONFLICT (item_cd, loc_cd, lot_no) DO UPDATE SET qty = EXCLUDED.qty, upd_ts = EXCLUDED.upd_ts;

UPDATE incoming_stock_movement SET discard_reason = 'holdings are checked against stock positions, not movements';
UPDATE incoming_material_issue SET discard_reason = 'holdings are checked against stock positions, not issues';
