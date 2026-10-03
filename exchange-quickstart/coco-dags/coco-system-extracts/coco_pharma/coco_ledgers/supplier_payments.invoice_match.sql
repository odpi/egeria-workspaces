-- Extract: Coco Ledgers (Coco core) -> Supplier Payments / invoice_match
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.supplier_payments.invoice_match
-- ap_invoice; match codes expanded.
SELECT
  i.vendor_inv_no::varchar(40)   AS invoice_number,
  i.vendor_no::varchar(40)       AS supplier_identifier,
  i.po_no::varchar(40)           AS order_identifier,
  i.grn_ref::varchar(40)         AS goods_receipt_identifier,
  i.inv_amount::numeric(18,2)    AS invoice_total_amount,
  i.ccy::varchar(3)              AS invoice_currency_code,
  (CASE i.match_status WHEN 'M' THEN 'matched' WHEN 'V' THEN 'variance' ELSE 'unmatched' END)::varchar(20) AS invoice_match_status
FROM coco_ledgers.ap_invoice i
