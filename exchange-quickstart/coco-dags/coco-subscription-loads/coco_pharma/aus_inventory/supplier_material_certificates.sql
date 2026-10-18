-- Subscription: coco_aus_inventory__supplier_material_certificates - Austin Inventory (Coco core) receives Supplier Material Certificates
-- Destination: coco_pharma.aus_inventory (System::aus-inventory)
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps certificates from Coco suppliers (numeric ids below 100000) and their stated results in vendor_coa and
-- vendor_coa_test (both NEW, item lower case and date as text MM/DD/YYYY in this system's style), matched to
-- receiving_log.coa_no at receipt.  Discards Austin's own suppliers' (100xxx) and EKG's (700xxx) certificates -
-- today all rows.

UPDATE incoming_certificate_of_analysis SET discard_reason = 'Austin or EKG supplier''s lot - not received by Austin Inventory'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO aus_inventory.vendor_coa (coa_no, vendor_no, item_no, vendor_lot, cert_type, cert_date, conforms)
SELECT c.certificate_identifier, c.supplier_identifier::integer, lower(c.raw_material_code), c.lot_identifier,
       (CASE WHEN c.certificate_type ILIKE '%conformity%' THEN 'Conformity' ELSE 'Analysis' END),
       to_char(c.certificate_date, 'MM/DD/YYYY'), (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END)
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa_no) DO UPDATE SET vendor_no = EXCLUDED.vendor_no, item_no = EXCLUDED.item_no, vendor_lot = EXCLUDED.vendor_lot,
       cert_type = EXCLUDED.cert_type, cert_date = EXCLUDED.cert_date, conforms = EXCLUDED.conforms;

UPDATE incoming_certificate_test_result t SET discard_reason = 'result on a certificate Austin Inventory does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM aus_inventory.vendor_coa c WHERE c.coa_no = t.certificate_identifier);

INSERT INTO aus_inventory.vendor_coa_test (coa_no, test_code, test_value, test_unit, spec_min, spec_max)
SELECT t.certificate_identifier, t.test_code, t.test_value, t.test_unit, t.specification_minimum_value, t.specification_maximum_value
  FROM incoming_certificate_test_result t
 WHERE t.discard_reason IS NULL
ON CONFLICT (coa_no, test_code) DO UPDATE SET test_value = EXCLUDED.test_value, test_unit = EXCLUDED.test_unit,
       spec_min = EXCLUDED.spec_min, spec_max = EXCLUDED.spec_max;
