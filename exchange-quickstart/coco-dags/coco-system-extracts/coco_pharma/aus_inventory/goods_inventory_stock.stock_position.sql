-- Extract: Austin Inventory (Coco core) -> Goods Inventory Stock / stock_position
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.goods_inventory_stock.stock_position
-- on_hand summed per item and location; lot reported only where one lot is held.
SELECT
  upper(o.item_no)::varchar(20)       AS product_code,
  o.loc_id::varchar(20)               AS warehouse_code,
  (CASE WHEN count(DISTINCT o.lot_no) = 1 THEN min(o.lot_no) END)::varchar(40) AS lot_identifier,
  round(sum(o.qty))::integer          AS stock_level,
  round(max(o.min_qty))::integer      AS stock_minimum_level,
  round(max(o.max_qty))::integer      AS stock_maximum_level,
  max(o.as_of)                        AS stock_current_timestamp
FROM aus_inventory.on_hand o
GROUP BY upper(o.item_no), o.loc_id
