-- Extract: Edmonton Depot Management System (Coco core) -> Goods Receipts / goods_receipt
-- Source: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Target: coco_data_hub.goods_receipts.goods_receipt
-- receipt; vendor prefix stripped to the Coco supplier id, text date parsed, bin prefixed with the site.
SELECT
  r.receipt_id::varchar(40)                 AS goods_receipt_identifier,
  r.po_number::varchar(40)                  AS order_identifier,
  ltrim(r.vendor, 'V')::varchar(40)         AS supplier_identifier,
  upper(r.item)::varchar(20)                AS raw_material_code,
  r.vendor_lot::varchar(40)                 AS lot_identifier,
  to_date(r.received, 'YYYYMMDD')           AS goods_receipt_date,
  round(r.qty)::integer                     AS goods_receipt_quantity,
  ('EDM-' || r.bin)::varchar(20)            AS warehouse_code,
  r.coa::varchar(40)                        AS certificate_identifier
FROM eddepot01.receipt r
