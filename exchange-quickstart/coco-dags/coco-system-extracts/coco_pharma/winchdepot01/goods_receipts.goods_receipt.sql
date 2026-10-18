-- Extract: Winchester Depot Management System (Coco core) -> Goods Receipts / goods_receipt
-- Source: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Target: coco_data_hub.goods_receipts.goods_receipt
-- gr_hdr joined to gr_line; receipt id is GRN/line, depot bay prefixed with the site.
SELECT
  (h.grn_no || '/' || l.ln_no)::varchar(40) AS goods_receipt_identifier,
  h.po_ref::varchar(40)                     AS order_identifier,
  h.supp_no::varchar(40)                    AS supplier_identifier,
  l.item_cd::varchar(20)                    AS raw_material_code,
  l.supp_lot::varchar(40)                   AS lot_identifier,
  h.rcv_dt                                  AS goods_receipt_date,
  round(l.qty)::integer                     AS goods_receipt_quantity,
  ('WIN-' || h.whs)::varchar(20)            AS warehouse_code,
  l.coa_ref::varchar(40)                    AS certificate_identifier
FROM winchdepot01.gr_hdr h
JOIN winchdepot01.gr_line l ON l.grn_no = h.grn_no
