-- Extract: Kansas City Depot Management System (Coco core) -> Goods Receipts / goods_receipt
-- Source: coco_pharma.kcdepot01 (System::KCDEPOT01)
-- Target: coco_data_hub.goods_receipts.goods_receipt
-- inbound_receipt; sku upper-cased, warehouse prefixed with the site.
SELECT
  r.rcpt_nbr::varchar(40)             AS goods_receipt_identifier,
  r.po_nbr::varchar(40)               AS order_identifier,
  r.vendor_id::varchar(40)            AS supplier_identifier,
  upper(r.sku)::varchar(20)           AS raw_material_code,
  r.lot_nbr::varchar(40)              AS lot_identifier,
  r.rcpt_dt                           AS goods_receipt_date,
  r.rcpt_qty::integer                 AS goods_receipt_quantity,
  ('KC-' || r.whse_cd)::varchar(20)   AS warehouse_code,
  r.cert_nbr::varchar(40)             AS certificate_identifier
FROM kcdepot01.inbound_receipt r
