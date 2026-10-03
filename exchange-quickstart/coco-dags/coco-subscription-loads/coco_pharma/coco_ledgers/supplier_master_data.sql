-- Subscription: coco_ledgers__supplier_master_data - Coco Ledgers (Coco core) receives Supplier Master Data
-- Destination: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Why it subscribes: Supplier Payments depends on it (supplier and payment details)
-- Keeps Coco suppliers (numeric ids below 100000, the procurement01 vendor numbers) in the payables vendor master
-- ap_vendor (NEW): status, screening status in the ledger's CLR/REV/BLK codes, rating, open anomaly and the
-- verified payee account.  Discards Austin (100xxx) and EKG (700xxx) suppliers, paid by their own payables.

UPDATE incoming_supplier SET discard_reason = 'Austin or EKG supplier - paid by the acquired estate''s own payables'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';
UPDATE incoming_supplier_risk_status SET discard_reason = 'Austin or EKG supplier - paid by the acquired estate''s own payables'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';
UPDATE incoming_supplier_payment_details SET discard_reason = 'Austin or EKG supplier - paid by the acquired estate''s own payables'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO coco_ledgers.ap_vendor (vendor_no, vendor_name, vendor_type, country, approved_yn, approved_on, vendor_status)
SELECT s.supplier_identifier::integer, s.supplier_name, s.supplier_type, s.supplier_country,
       (CASE WHEN s.supplier_approved_flag THEN 'Y' ELSE 'N' END), s.supplier_approved_date, s.supplier_current_status
  FROM incoming_supplier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (vendor_no) DO UPDATE SET vendor_name = EXCLUDED.vendor_name, vendor_type = EXCLUDED.vendor_type,
       country = EXCLUDED.country, approved_yn = EXCLUDED.approved_yn, approved_on = EXCLUDED.approved_on,
       vendor_status = EXCLUDED.vendor_status;

UPDATE incoming_supplier_risk_status r SET discard_reason = 'supplier not yet in the payables vendor master'
 WHERE r.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ledgers.ap_vendor v WHERE v.vendor_no::text = r.supplier_identifier);
UPDATE incoming_supplier_payment_details p SET discard_reason = 'supplier not yet in the payables vendor master'
 WHERE p.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ledgers.ap_vendor v WHERE v.vendor_no::text = p.supplier_identifier);

UPDATE coco_ledgers.ap_vendor v
   SET screen_status = (CASE r.supplier_screened_status WHEN 'clear' THEN 'CLR' WHEN 'match under review' THEN 'REV' ELSE 'BLK' END),
       screened_on = r.supplier_screened_date, risk_rating = r.supplier_rating, screen_ref = r.screening_identifier,
       anomaly_ref = r.anomaly_identifier
  FROM incoming_supplier_risk_status r
 WHERE r.discard_reason IS NULL AND r.supplier_identifier = v.vendor_no::text;

UPDATE coco_ledgers.ap_vendor v
   SET payee_acct_masked = p.bank_account_current_identifier, payee_bank = p.bank_account_provider_name,
       payee_bank_country = p.bank_account_country, bank_change_ref = p.payment_detail_change_identifier,
       bank_verified_on = p.payment_detail_verified_date
  FROM incoming_supplier_payment_details p
 WHERE p.discard_reason IS NULL AND p.supplier_identifier = v.vendor_no::text;
