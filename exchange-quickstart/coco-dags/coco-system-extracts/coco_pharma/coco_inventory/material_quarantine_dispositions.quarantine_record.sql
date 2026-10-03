-- Extract: Coco Inventory (Coco core) -> Material Quarantine Dispositions / quarantine_record
-- Source: coco_pharma.coco_inventory (System::coco-inventory)
-- Target: coco_data_hub.material_quarantine_dispositions.quarantine_record
-- inv_qrn; H/R/X status codes expanded.
SELECT
  q.lot_no::varchar(40)               AS lot_identifier,
  q.item_cd::varchar(20)              AS raw_material_code,
  q.grn_ref::varchar(40)              AS goods_receipt_identifier,
  q.q_start_ts                        AS lot_quarantine_start_timestamp,
  q.loc_cd::varchar(20)               AS warehouse_code,
  q.qty::integer                      AS lot_quantity,
  q.smpl_ref::varchar(40)             AS sample_identifier,
  (CASE q.q_sts WHEN 'R' THEN 'released' WHEN 'X' THEN 'rejected' ELSE 'held' END)::varchar(20) AS lot_quarantine_status
FROM coco_inventory.inv_qrn q
