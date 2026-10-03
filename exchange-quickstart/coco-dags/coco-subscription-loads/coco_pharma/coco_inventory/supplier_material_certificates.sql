-- Subscription: coco_inventory__supplier_material_certificates - Coco Inventory (Coco core) receives Supplier Material Certificates
-- Destination: coco_pharma.coco_inventory (System::coco-inventory)
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps certificates from Coco suppliers (numeric ids below 100000) and their stated test results in inv_supp_coa
-- and inv_supp_coa_tst (both NEW, type COA or COC), checked at receipt and quarantine release.  Discards
-- certificates of Austin (100xxx) and EKG (700xxx) suppliers' lots - today all rows.

UPDATE incoming_certificate_of_analysis SET discard_reason = 'Austin or EKG supplier''s lot - not received at Coco locations'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO coco_inventory.inv_supp_coa (cert_ref, supp_no, item_cd, lot_no, cert_typ, cert_dt, ok_yn)
SELECT c.certificate_identifier, c.supplier_identifier, c.raw_material_code, c.lot_identifier,
       (CASE WHEN c.certificate_type ILIKE '%conformity%' THEN 'COC' ELSE 'COA' END), c.certificate_date,
       (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END)
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (cert_ref) DO UPDATE SET supp_no = EXCLUDED.supp_no, item_cd = EXCLUDED.item_cd, lot_no = EXCLUDED.lot_no,
       cert_typ = EXCLUDED.cert_typ, cert_dt = EXCLUDED.cert_dt, ok_yn = EXCLUDED.ok_yn;

UPDATE incoming_certificate_test_result t SET discard_reason = 'result on a certificate Coco Inventory does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_inventory.inv_supp_coa c WHERE c.cert_ref = t.certificate_identifier);

INSERT INTO coco_inventory.inv_supp_coa_tst (cert_ref, test_cd, tst_val, tst_uom, spec_lo, spec_hi)
SELECT t.certificate_identifier, t.test_code, t.test_value, t.test_unit, t.specification_minimum_value, t.specification_maximum_value
  FROM incoming_certificate_test_result t
 WHERE t.discard_reason IS NULL
ON CONFLICT (cert_ref, test_cd) DO UPDATE SET tst_val = EXCLUDED.tst_val, tst_uom = EXCLUDED.tst_uom, spec_lo = EXCLUDED.spec_lo,
       spec_hi = EXCLUDED.spec_hi;
