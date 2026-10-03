-- Subscription: coco_mfctrl9482__deviations_and_capas - Austin Manufacturing Control System (Coco core) receives Deviations And CAPAs
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Electronic Batch Records depends on it (deviation disposition)
-- Keeps deviations the Austin site's QMS raised against the shared Coco batches (A26- batches of 3000, 2050 and
-- 9000), with their investigation outcome and disposition, in mfc_deviation (NEW) - the release of a shared
-- batch waits on them.  Discards corrective actions (followed up in Austin's QMS), deviations on Austin's own
-- products or with no shared batch, and EKG's deviations.

UPDATE incoming_deviation d SET discard_reason = 'not against a shared Coco batch made at the Austin site'
 WHERE d.batch_identifier IS NULL OR NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = d.batch_identifier) OR d.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_deviation (deviation_id, batch_id, product_cd, raised_utc, source_type, description, severity, dev_status)
SELECT d.deviation_identifier, d.batch_identifier, d.product_code, d.deviation_raised_timestamp, d.deviation_source_type,
       d.deviation_description, d.deviation_severity, d.deviation_current_status
  FROM incoming_deviation d
 WHERE d.discard_reason IS NULL
ON CONFLICT (deviation_id) DO UPDATE SET batch_id = EXCLUDED.batch_id, product_cd = EXCLUDED.product_cd,
       raised_utc = EXCLUDED.raised_utc, source_type = EXCLUDED.source_type, description = EXCLUDED.description,
       severity = EXCLUDED.severity, dev_status = EXCLUDED.dev_status;

UPDATE incoming_investigation i SET discard_reason = 'investigation of a deviation not against a shared Coco batch'
 WHERE NOT EXISTS (SELECT 1 FROM mfctrl9482.mfc_deviation d WHERE d.deviation_id = i.deviation_identifier);

UPDATE mfctrl9482.mfc_deviation d
   SET investigator = i.deviation_investigator_identifier, investigated_on = i.deviation_investigation_completed_date,
       root_cause = i.deviation_root_cause_description, impact = i.deviation_impact_description,
       disposition = i.deviation_disposition_status
  FROM incoming_investigation i
 WHERE i.discard_reason IS NULL AND i.deviation_identifier = d.deviation_id;

UPDATE incoming_corrective_action SET discard_reason = 'corrective actions are followed up in the Austin QMS, not the batch record';
