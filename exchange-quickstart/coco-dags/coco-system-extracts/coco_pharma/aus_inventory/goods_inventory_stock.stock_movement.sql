-- Extract: Austin Inventory (Coco core) -> Goods Inventory Stock / stock_movement
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.goods_inventory_stock.stock_movement
-- inv_transaction; one-letter codes expanded, quantity made absolute.
SELECT
  t.trans_no::varchar(40)             AS stock_movement_identifier,
  upper(t.item_no)::varchar(20)       AS product_code,
  t.lot_no::varchar(40)               AS lot_identifier,
  (CASE t.trans_code WHEN 'R' THEN 'receipt' WHEN 'I' THEN 'issue' WHEN 'T' THEN 'transfer'
                     WHEN 'A' THEN 'adjustment' WHEN 'S' THEN 'shipment' END)::varchar(20) AS stock_movement_type,
  round(abs(t.qty))::integer          AS stock_movement_quantity,
  t.trans_utc                         AS stock_movement_timestamp,
  t.loc_id::varchar(20)               AS warehouse_code
FROM aus_inventory.inv_transaction t
