-- Subscription: coco_aus_inventory__supplier_master_data - Austin Inventory (Coco core) receives Supplier Master Data
-- Destination: coco_pharma.aus_inventory (System::aus-inventory)
-- Why it subscribes: Goods Receipts depends on it (approved supplier)
-- Keeps Coco suppliers (numeric ids below 100000 - the vendor numbers in receiving_log) in vendor (NEW) with the
-- approved flag and status a receipt is checked against.  Discards Austin's own suppliers (100xxx, who deliver
-- into Austin's SAP stores) and EKG's (700xxx), and the screening and bank details (procurement's and payables').

UPDATE incoming_supplier SET discard_reason = 'Austin or EKG supplier - does not deliver Coco material to the Austin site'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO aus_inventory.vendor (vendor_no, vendor_name, approved, vendor_status)
SELECT s.supplier_identifier::integer, s.supplier_name, (CASE WHEN s.supplier_approved_flag THEN 'Y' ELSE 'N' END),
       upper(s.supplier_current_status)
  FROM incoming_supplier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (vendor_no) DO UPDATE SET vendor_name = EXCLUDED.vendor_name, approved = EXCLUDED.approved,
       vendor_status = EXCLUDED.vendor_status;

UPDATE incoming_supplier_risk_status SET discard_reason = 'screening status is not used by inventory';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not used by inventory';
