-- Subscription: coco_winch_mfg_control__deviations_and_capas - Winchester Manufacturing Control System (Coco core) receives Deviations And CAPAs
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (deviation disposition)
-- Keeps deviations raised against Winchester batches, with their investigation outcome and disposition, in wdev
-- (NEW), which the QP checks before certifying.  Discards corrective actions (followed up in the QMS, not part
-- of the batch record) and deviations of other factories' batches or with no Winchester batch - today all of
-- them, raised in the Austin and EKG quality systems.

UPDATE incoming_deviation d SET discard_reason = 'not against a Winchester batch'
 WHERE d.batch_identifier IS NULL
    OR NOT (EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = d.batch_identifier) OR d.batch_identifier ~ '^W[0-9]{2}-');

INSERT INTO winch_mfg_control.wdev (dev_ref, batch_no, prd_cd, raised_ts, src_typ, dev_txt, sev, dev_sts)
SELECT d.deviation_identifier, d.batch_identifier, d.product_code, d.deviation_raised_timestamp, d.deviation_source_type,
       d.deviation_description, d.deviation_severity, d.deviation_current_status
  FROM incoming_deviation d
 WHERE d.discard_reason IS NULL
ON CONFLICT (dev_ref) DO UPDATE SET batch_no = EXCLUDED.batch_no, prd_cd = EXCLUDED.prd_cd, raised_ts = EXCLUDED.raised_ts,
       src_typ = EXCLUDED.src_typ, dev_txt = EXCLUDED.dev_txt, sev = EXCLUDED.sev, dev_sts = EXCLUDED.dev_sts;

UPDATE incoming_investigation i SET discard_reason = 'investigation of a deviation not against a Winchester batch'
 WHERE NOT EXISTS (SELECT 1 FROM winch_mfg_control.wdev w WHERE w.dev_ref = i.deviation_identifier);

UPDATE winch_mfg_control.wdev w
   SET inv_by = i.deviation_investigator_identifier, inv_dt = i.deviation_investigation_completed_date,
       root_cause = i.deviation_root_cause_description, impact = i.deviation_impact_description,
       disp = i.deviation_disposition_status
  FROM incoming_investigation i
 WHERE i.discard_reason IS NULL AND i.deviation_identifier = w.dev_ref;

UPDATE incoming_corrective_action SET discard_reason = 'corrective actions are followed up in the QMS, not the batch record';
