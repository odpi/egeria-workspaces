-- Subscription: coco_inventory__supplier_master_data - Coco Inventory (Coco core) receives Supplier Master Data
-- Destination: coco_pharma.coco_inventory (System::coco-inventory)
-- Why it subscribes: Goods Receipts depends on it (approved supplier)
-- Keeps Coco suppliers (numeric ids below 100000) in inv_supp (NEW) with the approved flag and status a receipt
-- is checked against.  Discards Austin (100xxx) and EKG (700xxx) suppliers, which never deliver to Coco
-- locations, and the screening and bank details, which are procurement's and payables' business.

UPDATE incoming_supplier SET discard_reason = 'Austin or EKG supplier - does not deliver to Coco locations'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO coco_inventory.inv_supp (supp_no, supp_nm, appr_yn, supp_sts)
SELECT s.supplier_identifier, s.supplier_name, (CASE WHEN s.supplier_approved_flag THEN 'Y' ELSE 'N' END),
       (CASE s.supplier_current_status WHEN 'active' THEN 'A' WHEN 'suspended' THEN 'S' ELSE 'C' END)
  FROM incoming_supplier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (supp_no) DO UPDATE SET supp_nm = EXCLUDED.supp_nm, appr_yn = EXCLUDED.appr_yn, supp_sts = EXCLUDED.supp_sts;

UPDATE incoming_supplier_risk_status SET discard_reason = 'screening status is not used by inventory';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not used by inventory';
