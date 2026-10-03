-- Extract: Coco Ledgers (Coco core) -> Treatment Invoices / revenue_recognition
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.treatment_invoices.revenue_recognition
-- ar_invoice revenue recognition columns.
SELECT
  a.inv_no::varchar(40)          AS invoice_number,
  a.rev_rec_date                 AS revenue_recognition_date,
  a.rev_amount::numeric(18,2)    AS revenue_amount,
  a.delivery_date                AS order_delivery_date,
  a.rev_acct::varchar(20)        AS ledger_account_code
FROM coco_ledgers.ar_invoice a
