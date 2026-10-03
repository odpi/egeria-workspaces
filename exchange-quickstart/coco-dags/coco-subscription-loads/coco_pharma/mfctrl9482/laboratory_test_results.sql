-- Subscription: coco_mfctrl9482__laboratory_test_results - Austin Manufacturing Control System (Coco core) receives Laboratory Test Results
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Batch Execution Records (in-process results) and Electronic Batch Records (finished product results) depend on it
-- Keeps the Austin LIMS samples of the shared Coco batches (A26- batches of 3000, 2050 and 9000), their results
-- and certificates of analysis in mfc_lab_sample, mfc_lab_result and mfc_lab_coa (all NEW) for the LAB section of
-- the batch record.  Discards raw material samples (quarantine release is the inventory systems' business),
-- samples of Austin's own products and EKG's laboratory data.

UPDATE incoming_sample SET discard_reason = 'raw material sample - decides quarantine release, not the batch record'
 WHERE batch_identifier IS NULL;
UPDATE incoming_sample s SET discard_reason = 'sample of a batch that is not a shared Coco batch'
 WHERE s.discard_reason IS NULL AND NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = s.batch_identifier) OR s.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_lab_sample (sample_id, sample_type, batch_id, collected_utc, sample_status)
SELECT s.sample_identifier, upper(s.sample_type), s.batch_identifier, s.sample_collection_timestamp, upper(s.sample_current_status)
  FROM incoming_sample s
 WHERE s.discard_reason IS NULL
ON CONFLICT (sample_id) DO UPDATE SET sample_type = EXCLUDED.sample_type, batch_id = EXCLUDED.batch_id,
       collected_utc = EXCLUDED.collected_utc, sample_status = EXCLUDED.sample_status;

UPDATE incoming_test_result r SET discard_reason = 'result of a sample not of a shared Coco batch'
 WHERE NOT EXISTS (SELECT 1 FROM mfctrl9482.mfc_lab_sample s WHERE s.sample_id = r.sample_identifier);

INSERT INTO mfctrl9482.mfc_lab_result (result_id, sample_id, test_code, result_value, result_unit, spec_min, spec_max, conforms,
       completed_utc, analyst)
SELECT r.test_result_identifier, r.sample_identifier, r.test_code, r.test_value, r.test_unit, r.specification_minimum_value,
       r.specification_maximum_value, r.test_conformity_flag, r.test_completed_timestamp, r.test_analyst_identifier
  FROM incoming_test_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (result_id) DO UPDATE SET sample_id = EXCLUDED.sample_id, test_code = EXCLUDED.test_code,
       result_value = EXCLUDED.result_value, result_unit = EXCLUDED.result_unit, spec_min = EXCLUDED.spec_min,
       spec_max = EXCLUDED.spec_max, conforms = EXCLUDED.conforms, completed_utc = EXCLUDED.completed_utc,
       analyst = EXCLUDED.analyst;

UPDATE incoming_certificate_of_analysis c SET discard_reason = 'certificate not for a shared Coco batch'
 WHERE c.batch_identifier IS NULL OR NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = c.batch_identifier) OR c.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_lab_coa (coa_id, batch_id, coa_date, conforms, approver)
SELECT c.certificate_identifier, c.batch_identifier, c.certificate_date, c.certificate_conformity_flag, c.certificate_approver_identifier
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa_id) DO UPDATE SET batch_id = EXCLUDED.batch_id, coa_date = EXCLUDED.coa_date, conforms = EXCLUDED.conforms,
       approver = EXCLUDED.approver;
