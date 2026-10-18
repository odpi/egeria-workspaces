-- Subscription: coco_ed_mfg_control__laboratory_test_results - Edmonton Manufacturing Control System (Coco core) receives Laboratory Test Results
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Batch Execution Records (in-process results) and Electronic Batch Records (finished product results) depend on it
-- Keeps in-process and finished product samples of Edmonton lots, their results and certificates of analysis in
-- qc_sample, qc_result and qc_certificate (all NEW, times as local text, conformity 1/0).  Discards raw material
-- samples (they decide quarantine release in inventory) and other factories' batches - today all rows, because
-- the Edmonton QC laboratory is paper-based and only the Austin and EKG LIMS supply the product.

UPDATE incoming_sample SET discard_reason = 'raw material sample - decides quarantine release, not the batch record'
 WHERE batch_identifier IS NULL;
UPDATE incoming_sample s SET discard_reason = 'sample of a batch of another factory'
 WHERE s.discard_reason IS NULL AND NOT (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = s.batch_identifier) OR s.batch_identifier ~ '^E[0-9]{2}-');

INSERT INTO ed_mfg_control.qc_sample (sample_no, sample_kind, lot_id, collected, sample_status)
SELECT s.sample_identifier, s.sample_type, s.batch_identifier,
       to_char(s.sample_collection_timestamp AT TIME ZONE 'America/Edmonton', 'YYYY-MM-DD HH24:MI'), s.sample_current_status
  FROM incoming_sample s
 WHERE s.discard_reason IS NULL
ON CONFLICT (sample_no) DO UPDATE SET sample_kind = EXCLUDED.sample_kind, lot_id = EXCLUDED.lot_id, collected = EXCLUDED.collected,
       sample_status = EXCLUDED.sample_status;

UPDATE incoming_test_result r SET discard_reason = 'result of a sample not of an Edmonton lot'
 WHERE NOT EXISTS (SELECT 1 FROM ed_mfg_control.qc_sample s WHERE s.sample_no = r.sample_identifier);

INSERT INTO ed_mfg_control.qc_result (result_no, sample_no, test_code, result_value, result_unit, spec_low, spec_high, conforms,
       completed, analyst)
SELECT r.test_result_identifier, r.sample_identifier, r.test_code, r.test_value, r.test_unit, r.specification_minimum_value,
       r.specification_maximum_value, (CASE WHEN r.test_conformity_flag THEN 1 ELSE 0 END),
       to_char(r.test_completed_timestamp AT TIME ZONE 'America/Edmonton', 'YYYY-MM-DD HH24:MI'), r.test_analyst_identifier
  FROM incoming_test_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (result_no) DO UPDATE SET sample_no = EXCLUDED.sample_no, test_code = EXCLUDED.test_code,
       result_value = EXCLUDED.result_value, result_unit = EXCLUDED.result_unit, spec_low = EXCLUDED.spec_low,
       spec_high = EXCLUDED.spec_high, conforms = EXCLUDED.conforms, completed = EXCLUDED.completed, analyst = EXCLUDED.analyst;

UPDATE incoming_certificate_of_analysis c SET discard_reason = 'certificate not for an Edmonton lot'
 WHERE c.batch_identifier IS NULL OR NOT (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = c.batch_identifier) OR c.batch_identifier ~ '^E[0-9]{2}-');

INSERT INTO ed_mfg_control.qc_certificate (certificate_no, lot_id, issued_on, conforms, approved_by)
SELECT c.certificate_identifier, c.batch_identifier, c.certificate_date, (CASE WHEN c.certificate_conformity_flag THEN 1 ELSE 0 END),
       c.certificate_approver_identifier
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (certificate_no) DO UPDATE SET lot_id = EXCLUDED.lot_id, issued_on = EXCLUDED.issued_on, conforms = EXCLUDED.conforms,
       approved_by = EXCLUDED.approved_by;
