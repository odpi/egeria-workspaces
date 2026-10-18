-- Extract: Austin Inventory (Coco core) -> Goods Receipts / receipt_inspection
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.goods_receipts.receipt_inspection
-- rcv_inspection; badge to pseudonym via badge, outcome words normalised.
SELECT
  i.rcv_no::varchar(40)               AS goods_receipt_identifier,
  i.insp_date                         AS goods_receipt_inspection_date,
  b.worker_psn::varchar(40)           AS goods_receipt_inspector_identifier,
  (CASE lower(i.outcome) WHEN 'accepted' THEN 'accepted' WHEN 'rejected' THEN 'rejected' ELSE 'held' END)::varchar(20) AS goods_receipt_inspection_status,
  i.remarks                           AS goods_receipt_inspection_notes
FROM aus_inventory.rcv_inspection i
JOIN aus_inventory.badge b ON b.badge_no = i.inspector_badge
