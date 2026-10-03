-- Extract: SAP Ariba SRM (Austin) -> Supplier Payments / invoice_match
-- Source: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Target: coco_data_hub.supplier_payments.invoice_match
-- invoice_reconciliation; Reconciled/Paid -> matched, price exceptions -> variance, receipt exceptions -> unmatched.
SELECT
  r.supplier_invoice_number::varchar(40) AS invoice_number,
  r.erp_vendor_id::varchar(40) AS supplier_identifier,
  r.po_number::varchar(40) AS order_identifier,
  r.receipt_id::varchar(40) AS goods_receipt_identifier,
  r.total_amount::numeric(18,2) AS invoice_total_amount,
  r.currency::varchar(3) AS invoice_currency_code,
  (CASE WHEN r.reconciliation_status IN ('Reconciled', 'Paying', 'Paid') THEN 'matched'
        WHEN r.exception_type LIKE '%Variance' THEN 'variance' ELSE 'unmatched' END)::varchar(20) AS invoice_match_status
FROM sap_ariba.invoice_reconciliation r
