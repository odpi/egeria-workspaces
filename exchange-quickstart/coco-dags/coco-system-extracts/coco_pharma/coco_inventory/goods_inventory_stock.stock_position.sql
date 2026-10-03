-- Extract: Coco Inventory (Coco core) -> Goods Inventory Stock / stock_position
-- Source: coco_pharma.coco_inventory (System::coco-inventory)
-- Target: coco_data_hub.goods_inventory_stock.stock_position
-- inv_bal summed per item and location; lot reported only where a single lot is held; min/max taken from whichever lot row carries them.
SELECT
  b.item_cd::varchar(20)              AS product_code,
  b.loc_cd::varchar(20)               AS warehouse_code,
  (CASE WHEN count(DISTINCT b.lot_no) = 1 THEN nullif(min(b.lot_no), '-') END)::varchar(40) AS lot_identifier,
  sum(b.on_hand)::integer             AS stock_level,
  max(b.min_lvl)::integer             AS stock_minimum_level,
  max(b.max_lvl)::integer             AS stock_maximum_level,
  max(b.upd_ts)                       AS stock_current_timestamp
FROM coco_inventory.inv_bal b
GROUP BY b.item_cd, b.loc_cd
