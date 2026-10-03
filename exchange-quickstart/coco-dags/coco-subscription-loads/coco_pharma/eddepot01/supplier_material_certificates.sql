-- Subscription: coco_eddepot01__supplier_material_certificates - Edmonton Depot Management System (Coco core) receives Supplier Material Certificates
-- Destination: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps certificates from Coco suppliers (numeric ids below 100000) and their stated results in coa_cert and
-- coa_cert_test (both NEW; vendor 'V' + id and issue date as text YYYYMMDD in this system's style), matched to
-- receipt.coa at goods in.  Discards Austin (100xxx) and EKG (700xxx) suppliers' certificates - today all rows.

UPDATE incoming_certificate_of_analysis SET discard_reason = 'Austin or EKG supplier''s lot - not received at the Edmonton depot'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO eddepot01.coa_cert (coa, vendor, item, vendor_lot, cert_kind, issued, conforms)
SELECT c.certificate_identifier, 'V' || c.supplier_identifier, c.raw_material_code, c.lot_identifier, c.certificate_type,
       to_char(c.certificate_date, 'YYYYMMDD'), (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END)
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa) DO UPDATE SET vendor = EXCLUDED.vendor, item = EXCLUDED.item, vendor_lot = EXCLUDED.vendor_lot,
       cert_kind = EXCLUDED.cert_kind, issued = EXCLUDED.issued, conforms = EXCLUDED.conforms;

UPDATE incoming_certificate_test_result t SET discard_reason = 'result on a certificate the depot does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM eddepot01.coa_cert c WHERE c.coa = t.certificate_identifier);

INSERT INTO eddepot01.coa_cert_test (coa, test_code, test_value, test_unit, spec_min, spec_max)
SELECT t.certificate_identifier, t.test_code, t.test_value, t.test_unit, t.specification_minimum_value, t.specification_maximum_value
  FROM incoming_certificate_test_result t
 WHERE t.discard_reason IS NULL
ON CONFLICT (coa, test_code) DO UPDATE SET test_value = EXCLUDED.test_value, test_unit = EXCLUDED.test_unit,
       spec_min = EXCLUDED.spec_min, spec_max = EXCLUDED.spec_max;
