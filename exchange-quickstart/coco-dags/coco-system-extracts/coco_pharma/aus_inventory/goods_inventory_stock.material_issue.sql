-- Extract: Austin Inventory (Coco core) -> Goods Inventory Stock / material_issue
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.goods_inventory_stock.material_issue
-- inv_transaction issues to a batch; lot status at issue expanded.
SELECT
  t.trans_no::varchar(40)             AS stock_movement_identifier,
  t.batch_id::varchar(40)             AS batch_identifier,
  upper(t.item_no)::varchar(20)       AS raw_material_code,
  t.lot_no::varchar(40)               AS lot_identifier,
  round(abs(t.qty))::integer          AS raw_material_issued_quantity,
  (CASE t.lot_status_at_trans WHEN 'R' THEN 'released' WHEN 'X' THEN 'rejected' ELSE 'held' END)::varchar(20) AS lot_quarantine_status
FROM aus_inventory.inv_transaction t
WHERE t.trans_code = 'I' AND t.batch_id IS NOT NULL
