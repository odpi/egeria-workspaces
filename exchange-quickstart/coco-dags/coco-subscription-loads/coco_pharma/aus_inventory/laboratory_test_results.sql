-- Subscription: coco_aus_inventory__laboratory_test_results - Austin Inventory (Coco core) receives Laboratory Test Results
-- Destination: coco_pharma.aus_inventory (System::aus-inventory)
-- Why it subscribes: Material Quarantine Dispositions depends on it (test results)
-- Keeps laboratory samples of lots in Austin Inventory's quarantine (lot_status), their results and certificates
-- in lab_sample_in, lab_result_in and lab_coa_in (all NEW, certificate date as text MM/DD/YYYY), which the lot
-- disposition refers to.  Discards samples and certificates of lots it does not hold - today all rows: the Austin
-- LIMS tests the Austin site's own SAP lots (RM26-) and the shared batches, and EKG's are another estate's.

UPDATE incoming_sample s SET discard_reason = 'batch sample - for the batch record, not quarantine release'
 WHERE s.lot_identifier IS NULL;
UPDATE incoming_sample s SET discard_reason = 'lot not held in Austin Inventory'
 WHERE s.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM aus_inventory.lot_status l WHERE l.lot_no = s.lot_identifier);

INSERT INTO aus_inventory.lab_sample_in (sample_no, lot_no, collected_utc, sample_status)
SELECT s.sample_identifier, s.lot_identifier, s.sample_collection_timestamp, upper(s.sample_current_status)
  FROM incoming_sample s
 WHERE s.discard_reason IS NULL
ON CONFLICT (sample_no) DO UPDATE SET lot_no = EXCLUDED.lot_no, collected_utc = EXCLUDED.collected_utc,
       sample_status = EXCLUDED.sample_status;

UPDATE incoming_test_result r SET discard_reason = 'result of a sample Austin Inventory does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM aus_inventory.lab_sample_in s WHERE s.sample_no = r.sample_identifier);

INSERT INTO aus_inventory.lab_result_in (result_no, sample_no, test_code, result_value, result_unit, pass_fail, completed_utc)
SELECT r.test_result_identifier, r.sample_identifier, r.test_code, r.test_value, r.test_unit,
       (CASE WHEN r.test_conformity_flag THEN 'P' ELSE 'F' END), r.test_completed_timestamp
  FROM incoming_test_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (result_no) DO UPDATE SET sample_no = EXCLUDED.sample_no, test_code = EXCLUDED.test_code,
       result_value = EXCLUDED.result_value, result_unit = EXCLUDED.result_unit, pass_fail = EXCLUDED.pass_fail,
       completed_utc = EXCLUDED.completed_utc;

UPDATE incoming_certificate_of_analysis c SET discard_reason = 'certificate not for a lot held in Austin Inventory'
 WHERE c.lot_identifier IS NULL OR NOT EXISTS (SELECT 1 FROM aus_inventory.lot_status l WHERE l.lot_no = c.lot_identifier);

INSERT INTO aus_inventory.lab_coa_in (coa_no, lot_no, coa_date, pass_fail, approver)
SELECT c.certificate_identifier, c.lot_identifier, to_char(c.certificate_date, 'MM/DD/YYYY'),
       (CASE WHEN c.certificate_conformity_flag THEN 'P' ELSE 'F' END), c.certificate_approver_identifier
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa_no) DO UPDATE SET lot_no = EXCLUDED.lot_no, coa_date = EXCLUDED.coa_date, pass_fail = EXCLUDED.pass_fail,
       approver = EXCLUDED.approver;
