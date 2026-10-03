-- Extract: Coco Inventory (Coco core) -> Goods Receipts / receipt_inspection
-- Source: coco_pharma.coco_inventory (System::coco-inventory)
-- Target: coco_data_hub.goods_receipts.receipt_inspection
-- inv_insp; inspector is the worker pseudonym, result codes expanded.
SELECT
  i.grn_ref::varchar(40)              AS goods_receipt_identifier,
  i.insp_dt                           AS goods_receipt_inspection_date,
  i.inspector::varchar(40)            AS goods_receipt_inspector_identifier,
  (CASE i.result WHEN 'ACC' THEN 'accepted' WHEN 'REJ' THEN 'rejected' ELSE 'held' END)::varchar(20) AS goods_receipt_inspection_status,
  i.notes                             AS goods_receipt_inspection_notes
FROM coco_inventory.inv_insp i
