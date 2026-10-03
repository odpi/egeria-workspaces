-- Extract: Coco Ledgers (Coco core) -> Supplier Payments / payment_instruction
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.supplier_payments.payment_instruction
-- ap_payment; approver to pseudonym, screening status codes expanded.
SELECT
  p.pay_id::varchar(40)          AS payment_identifier,
  p.vendor_no::varchar(40)       AS supplier_identifier,
  p.vendor_inv_no::varchar(40)   AS invoice_number,
  p.pay_amount::numeric(18,2)    AS payment_amount,
  p.ccy::varchar(3)              AS payment_currency_code,
  u.worker_ref::varchar(40)      AS payment_authoriser_identifier,
  p.approved_at                  AS payment_authorised_timestamp,
  (CASE p.vendor_screen_status WHEN 'CLR' THEN 'clear' WHEN 'REV' THEN 'match under review' ELSE 'blocked' END)::varchar(20) AS supplier_screened_status,
  p.payee_acct_masked::varchar(40) AS bank_account_current_identifier,
  p.gl_acct::varchar(20)         AS ledger_account_code
FROM coco_ledgers.ap_payment p
JOIN coco_ledgers.fm_user u ON u.user_email = p.approved_by
