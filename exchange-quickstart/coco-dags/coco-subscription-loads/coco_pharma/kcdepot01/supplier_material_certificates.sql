-- Subscription: coco_kcdepot01__supplier_material_certificates - Kansas City Depot Management System (Coco core) receives Supplier Material Certificates
-- Destination: coco_pharma.kcdepot01 (System::KCDEPOT01)
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps certificates from Coco suppliers (numeric ids below 100000) and their stated results in lot_cert and
-- lot_cert_test (both NEW; sku lower case, type COA or COC), matched to inbound_receipt.cert_nbr.  Discards
-- Austin (100xxx) and EKG (700xxx) suppliers' certificates - today all rows.

UPDATE incoming_certificate_of_analysis SET discard_reason = 'Austin or EKG supplier''s lot - not received at Kansas City'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO kcdepot01.lot_cert (cert_nbr, vendor_id, sku, lot_nbr, cert_type_cd, cert_dt, conforms_flag)
SELECT c.certificate_identifier, c.supplier_identifier::integer, lower(c.raw_material_code), c.lot_identifier,
       (CASE WHEN c.certificate_type ILIKE '%conformity%' THEN 'COC' ELSE 'COA' END), c.certificate_date,
       (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END)
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (cert_nbr) DO UPDATE SET vendor_id = EXCLUDED.vendor_id, sku = EXCLUDED.sku, lot_nbr = EXCLUDED.lot_nbr,
       cert_type_cd = EXCLUDED.cert_type_cd, cert_dt = EXCLUDED.cert_dt, conforms_flag = EXCLUDED.conforms_flag;

UPDATE incoming_certificate_test_result t SET discard_reason = 'result on a certificate the depot does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM kcdepot01.lot_cert c WHERE c.cert_nbr = t.certificate_identifier);

INSERT INTO kcdepot01.lot_cert_test (cert_nbr, test_cd, test_val, test_uom, spec_min, spec_max)
SELECT t.certificate_identifier, t.test_code, t.test_value, t.test_unit, t.specification_minimum_value, t.specification_maximum_value
  FROM incoming_certificate_test_result t
 WHERE t.discard_reason IS NULL
ON CONFLICT (cert_nbr, test_cd) DO UPDATE SET test_val = EXCLUDED.test_val, test_uom = EXCLUDED.test_uom,
       spec_min = EXCLUDED.spec_min, spec_max = EXCLUDED.spec_max;
