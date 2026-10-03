-- Subscription: coco_winchdepot01__supplier_master_data - Winchester Depot Management System (Coco core) receives Supplier Master Data
-- Destination: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Why it subscribes: Goods Receipts depends on it (approved supplier)
-- Keeps Coco suppliers (numeric ids below 100000) in supp_mstr (NEW, supp_no as in gr_hdr) with the approved
-- flag and status checked at goods in.  Discards Austin (100xxx) and EKG (700xxx) suppliers, which never deliver
-- to Winchester, and the screening and bank details.

UPDATE incoming_supplier SET discard_reason = 'Austin or EKG supplier - does not deliver to the Winchester depot'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO winchdepot01.supp_mstr (supp_no, supp_nm, appr_flg, supp_sts)
SELECT s.supplier_identifier::integer, s.supplier_name, (CASE WHEN s.supplier_approved_flag THEN 'Y' ELSE 'N' END),
       upper(s.supplier_current_status)
  FROM incoming_supplier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (supp_no) DO UPDATE SET supp_nm = EXCLUDED.supp_nm, appr_flg = EXCLUDED.appr_flg, supp_sts = EXCLUDED.supp_sts;

UPDATE incoming_supplier_risk_status SET discard_reason = 'screening status is not used at goods in';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not used at goods in';
