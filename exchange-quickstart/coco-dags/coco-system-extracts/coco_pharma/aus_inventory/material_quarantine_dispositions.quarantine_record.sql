-- Extract: Austin Inventory (Coco core) -> Material Quarantine Dispositions / quarantine_record
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.material_quarantine_dispositions.quarantine_record
-- lot_status; item upper-cased, status words normalised.
SELECT
  l.lot_no::varchar(40)               AS lot_identifier,
  upper(l.item_no)::varchar(20)       AS raw_material_code,
  l.rcv_no::varchar(40)               AS goods_receipt_identifier,
  l.quar_start                        AS lot_quarantine_start_timestamp,
  l.loc_id::varchar(20)               AS warehouse_code,
  round(l.qty)::integer               AS lot_quantity,
  l.sample_no::varchar(40)            AS sample_identifier,
  (CASE l.status WHEN 'RELEASED' THEN 'released' WHEN 'REJECTED' THEN 'rejected' ELSE 'held' END)::varchar(20) AS lot_quarantine_status
FROM aus_inventory.lot_status l
