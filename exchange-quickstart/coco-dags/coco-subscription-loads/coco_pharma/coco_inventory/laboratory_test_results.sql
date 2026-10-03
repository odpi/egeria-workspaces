-- Subscription: coco_inventory__laboratory_test_results - Coco Inventory (Coco core) receives Laboratory Test Results
-- Destination: coco_pharma.coco_inventory (System::coco-inventory)
-- Why it subscribes: Material Quarantine Dispositions depends on it (test results)
-- Keeps laboratory samples of lots held in Coco Inventory's quarantine (inv_qrn), their results and certificates
-- in inv_qc_smpl, inv_qc_res and inv_qc_coa (all NEW), which the quarantine decision refers to.  Discards
-- samples and certificates of lots it does not hold and batch samples (the control systems' business) - today
-- all rows, from the Austin and EKG LIMS; Coco's own QC laboratories are paper-based.

UPDATE incoming_sample s SET discard_reason = 'batch sample - for the batch record, not quarantine release'
 WHERE s.lot_identifier IS NULL;
UPDATE incoming_sample s SET discard_reason = 'lot not held in Coco Inventory'
 WHERE s.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM coco_inventory.inv_qrn q WHERE q.lot_no = s.lot_identifier);

INSERT INTO coco_inventory.inv_qc_smpl (smpl_ref, lot_no, coll_ts, smpl_sts)
SELECT s.sample_identifier, s.lot_identifier, s.sample_collection_timestamp, s.sample_current_status
  FROM incoming_sample s
 WHERE s.discard_reason IS NULL
ON CONFLICT (smpl_ref) DO UPDATE SET lot_no = EXCLUDED.lot_no, coll_ts = EXCLUDED.coll_ts, smpl_sts = EXCLUDED.smpl_sts;

UPDATE incoming_test_result r SET discard_reason = 'result of a sample Coco Inventory does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_inventory.inv_qc_smpl s WHERE s.smpl_ref = r.sample_identifier);

INSERT INTO coco_inventory.inv_qc_res (res_ref, smpl_ref, test_cd, res_val, res_uom, pass_yn, done_ts)
SELECT r.test_result_identifier, r.sample_identifier, r.test_code, r.test_value, r.test_unit,
       (CASE WHEN r.test_conformity_flag THEN 'Y' ELSE 'N' END), r.test_completed_timestamp
  FROM incoming_test_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (res_ref) DO UPDATE SET smpl_ref = EXCLUDED.smpl_ref, test_cd = EXCLUDED.test_cd, res_val = EXCLUDED.res_val,
       res_uom = EXCLUDED.res_uom, pass_yn = EXCLUDED.pass_yn, done_ts = EXCLUDED.done_ts;

UPDATE incoming_certificate_of_analysis c SET discard_reason = 'certificate not for a lot held in Coco Inventory'
 WHERE c.lot_identifier IS NULL OR NOT EXISTS (SELECT 1 FROM coco_inventory.inv_qrn q WHERE q.lot_no = c.lot_identifier);

INSERT INTO coco_inventory.inv_qc_coa (coa_ref, lot_no, coa_dt, pass_yn, approver)
SELECT c.certificate_identifier, c.lot_identifier, c.certificate_date, (CASE WHEN c.certificate_conformity_flag THEN 'Y' ELSE 'N' END),
       c.certificate_approver_identifier
  FROM incoming_certificate_of_analysis c
 WHERE c.discard_reason IS NULL
ON CONFLICT (coa_ref) DO UPDATE SET lot_no = EXCLUDED.lot_no, coa_dt = EXCLUDED.coa_dt, pass_yn = EXCLUDED.pass_yn, approver = EXCLUDED.approver;
