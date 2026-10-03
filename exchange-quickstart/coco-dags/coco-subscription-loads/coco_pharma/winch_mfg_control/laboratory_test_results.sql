-- Subscription: coco_winch_mfg_control__laboratory_test_results - Winchester Manufacturing Control System (Coco core) receives Laboratory Test Results
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Batch Execution Records (in-process results) and Electronic Batch Records (finished product results) depend on it
-- Keeps in-process and finished product samples of Winchester batches, their results and certificates of
-- analysis in wlab_smpl, wlab_res and wlab_coa (all NEW).  Discards raw material samples (they decide quarantine
-- release in inventory, not the batch record) and other factories' batches - today all rows, because the
-- Winchester QC laboratory is paper-based and only the Austin and EKG LIMS supply the product.

UPDATE incoming_sample SET discard_reason = 'raw material sample - decides quarantine release, not the batch record'
 WHERE batch_identifier IS NULL;
UPDATE incoming_sample s SET discard_reason = 'sample of a batch of another factory'
 WHERE s.discard_reason IS NULL
   AND NOT (EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = s.batch_identifier) OR s.batch_identifier ~ '^W[0-9]{2}-');

INSERT INTO winch_mfg_control.wlab_smpl (smpl_ref, smpl_typ, batch_no, coll_ts, smpl_sts)
SELECT s.sample_identifier, s.sample_type, s.batch_identifier, s.sample_collection_timestamp, s.sample_current_status
  FROM incoming_sample s
 WHERE s.discard_reason IS NULL
ON CONFLICT (smpl_ref) DO UPDATE SET smpl_typ = EXCLUDED.smpl_typ, batch_no = EXCLUDED.batch_no, coll_ts = EXCLUDED.coll_ts,
       smpl_sts = EXCLUDED.smpl_sts;

UPDATE incoming_test_result r SET discard_reason = 'result of a sample not of a Winchester batch'
 WHERE NOT EXISTS (SELECT 1 FROM winch_mfg_control.wlab_smpl s WHERE s.smpl_ref = r.sample_identifier);

INSERT INTO winch_mfg_control.wlab_res (res_ref, smpl_ref, test_cd, res_val, res_uom, spec_lo, spec_hi, pass_flg, done_ts, analyst)
SELECT r.test_result_identifier, r.sample_identifier, r.test_code, r.test_value, r.test_unit, r.specification_minimum_value,
       r.specification_maximum_value, (CASE WHEN r.test_conformity_flag THEN 'Y' ELSE 'N' END), r.test_completed_timestamp,
       r.test_analyst_identifier
  FROM incoming_test_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (res_ref) DO UPDATE SET smpl_ref = EXCLUDED.smpl_ref, test_cd = EXCLUDED.test_cd, res_val = EXCLUDED.res_val,
       res_uom = EXCLUDED.res_uom, spec_lo = EXCLUDED.spec_lo, spec_hi = EXCLUDED.spec_hi, pass_flg = EXCLUDED.pass_flg,
       done_ts = EXCLUDED.done_ts, analyst = EXCLUDED.analyst;

UPDATE incoming_certificate_of_analysis c SET discard_reason = 'certificate not for a Winchester batch'
 WHERE c.batch_identifier IS NULL
    OR NOT (EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = c.batch_identifier) OR c.batch_identifier ~ '^W[0-9]{2}-');

INSERT INTO winch_mfg_control.wlab_coa (coa_ref, batch_no, coa_dt, conform_flg, approver)
SELECT c.certificate_identifier, c.batch_identifier, c.certificate_date, (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END),
       c.certificate_approver_identifier
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa_ref) DO UPDATE SET batch_no = EXCLUDED.batch_no, coa_dt = EXCLUDED.coa_dt, conform_flg = EXCLUDED.conform_flg,
       approver = EXCLUDED.approver;
