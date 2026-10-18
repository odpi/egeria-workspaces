-- Extract: Austin Inventory (Coco core) -> Goods Receipts / goods_receipt
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.goods_receipts.goods_receipt
-- receiving_log; item upper-cased, MM/DD/YYYY text date parsed.
SELECT
  r.rcv_no::varchar(40)               AS goods_receipt_identifier,
  r.po_no::varchar(40)                AS order_identifier,
  r.vendor_no::varchar(40)            AS supplier_identifier,
  upper(r.item_no)::varchar(20)       AS raw_material_code,
  r.vendor_lot::varchar(40)           AS lot_identifier,
  to_date(r.rcv_date, 'MM/DD/YYYY')   AS goods_receipt_date,
  round(r.rcv_qty)::integer           AS goods_receipt_quantity,
  r.loc_id::varchar(20)               AS warehouse_code,
  r.coa_no::varchar(40)               AS certificate_identifier
FROM aus_inventory.receiving_log r
