-- Subscription: coco_eddepot01__supplier_master_data - Edmonton Depot Management System (Coco core) receives Supplier Master Data
-- Destination: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Why it subscribes: Goods Receipts depends on it (approved supplier)
-- Keeps Coco suppliers (numeric ids below 100000) in vendor_master (NEW, keyed 'V' + supplier id as in
-- receipt.vendor) with the approved flag and status checked at goods in.  Discards Austin (100xxx) and EKG
-- (700xxx) suppliers, which never deliver to Edmonton, and the screening and bank details.

UPDATE incoming_supplier SET discard_reason = 'Austin or EKG supplier - does not deliver to the Edmonton depot'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO eddepot01.vendor_master (vendor, vendor_name, approved, vendor_status)
SELECT 'V' || s.supplier_identifier, s.supplier_name, (CASE WHEN s.supplier_approved_flag THEN 'Y' ELSE 'N' END),
       upper(s.supplier_current_status)
  FROM incoming_supplier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (vendor) DO UPDATE SET vendor_name = EXCLUDED.vendor_name, approved = EXCLUDED.approved,
       vendor_status = EXCLUDED.vendor_status;

UPDATE incoming_supplier_risk_status SET discard_reason = 'screening status is not used at goods in';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not used at goods in';
