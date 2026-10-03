-- Extract: Coco Inventory (Coco core) -> Goods Inventory Stock / stock_movement
-- Source: coco_pharma.coco_inventory (System::coco-inventory)
-- Target: coco_data_hub.goods_inventory_stock.stock_movement
-- inv_txn; type codes expanded, signed quantity made absolute.
SELECT
  t.txn_id::varchar(40)               AS stock_movement_identifier,
  t.item_cd::varchar(20)              AS product_code,
  t.lot_no::varchar(40)               AS lot_identifier,
  (CASE t.txn_typ WHEN 'RCPT' THEN 'receipt' WHEN 'ISS' THEN 'issue' WHEN 'XFR' THEN 'transfer'
                  WHEN 'ADJ' THEN 'adjustment' WHEN 'SHIP' THEN 'shipment' END)::varchar(20) AS stock_movement_type,
  abs(t.qty)::integer                 AS stock_movement_quantity,
  t.txn_ts                            AS stock_movement_timestamp,
  t.loc_cd::varchar(20)               AS warehouse_code
FROM coco_inventory.inv_txn t
