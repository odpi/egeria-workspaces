-- Subscription: coco_winchdepot01__supplier_material_certificates - Winchester Depot Management System (Coco core) receives Supplier Material Certificates
-- Destination: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps certificates from Coco suppliers (numeric ids below 100000) and their stated results in coa_hdr and
-- coa_line (both NEW, type COA or COC), matched to gr_line.coa_ref at goods in.  Discards Austin (100xxx) and
-- EKG (700xxx) suppliers' certificates - today all rows.

UPDATE incoming_certificate_of_analysis SET discard_reason = 'Austin or EKG supplier''s lot - not received at Winchester'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO winchdepot01.coa_hdr (coa_ref, supp_no, item_cd, supp_lot, coa_typ, coa_dt, conform_flg)
SELECT c.certificate_identifier, c.supplier_identifier::integer, c.raw_material_code, c.lot_identifier,
       (CASE WHEN c.certificate_type ILIKE '%conformity%' THEN 'COC' ELSE 'COA' END), c.certificate_date,
       (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END)
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa_ref) DO UPDATE SET supp_no = EXCLUDED.supp_no, item_cd = EXCLUDED.item_cd, supp_lot = EXCLUDED.supp_lot,
       coa_typ = EXCLUDED.coa_typ, coa_dt = EXCLUDED.coa_dt, conform_flg = EXCLUDED.conform_flg;

UPDATE incoming_certificate_test_result t SET discard_reason = 'result on a certificate the depot does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM winchdepot01.coa_hdr c WHERE c.coa_ref = t.certificate_identifier);

INSERT INTO winchdepot01.coa_line (coa_ref, test_cd, test_val, uom, spec_min, spec_max)
SELECT t.certificate_identifier, t.test_code, t.test_value, t.test_unit, t.specification_minimum_value, t.specification_maximum_value
  FROM incoming_certificate_test_result t
 WHERE t.discard_reason IS NULL
ON CONFLICT (coa_ref, test_cd) DO UPDATE SET test_val = EXCLUDED.test_val, uom = EXCLUDED.uom, spec_min = EXCLUDED.spec_min,
       spec_max = EXCLUDED.spec_max;
