-- Extract: Coco Inventory (Coco core) -> Goods Inventory Stock / material_issue
-- Source: coco_pharma.coco_inventory (System::coco-inventory)
-- Target: coco_data_hub.goods_inventory_stock.material_issue
-- inv_txn issues to a manufacturing batch; quarantine status code at issue expanded.
SELECT
  t.txn_id::varchar(40)               AS stock_movement_identifier,
  t.batch_ref::varchar(40)            AS batch_identifier,
  t.item_cd::varchar(20)              AS raw_material_code,
  t.lot_no::varchar(40)               AS lot_identifier,
  abs(t.qty)::integer                 AS raw_material_issued_quantity,
  (CASE t.q_sts_at_txn WHEN 'R' THEN 'released' WHEN 'X' THEN 'rejected' ELSE 'held' END)::varchar(20) AS lot_quarantine_status
FROM coco_inventory.inv_txn t
WHERE t.txn_typ = 'ISS' AND t.batch_ref IS NOT NULL
