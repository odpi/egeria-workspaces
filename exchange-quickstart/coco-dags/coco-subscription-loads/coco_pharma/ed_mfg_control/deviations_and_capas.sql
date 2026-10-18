-- Subscription: coco_ed_mfg_control__deviations_and_capas - Edmonton Manufacturing Control System (Coco core) receives Deviations And CAPAs
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (deviation disposition)
-- Keeps deviations raised against Edmonton lots, with their investigation outcome and disposition, in
-- lot_deviation (NEW, raised as local text like the rest of this system), which QA checks before approving the
-- lot.  Discards corrective actions (followed up in the QMS) and deviations of other factories' batches or with
-- no Edmonton lot - today all of them, raised in the Austin and EKG quality systems.

UPDATE incoming_deviation d SET discard_reason = 'not against an Edmonton lot'
 WHERE d.batch_identifier IS NULL OR NOT (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = d.batch_identifier) OR d.batch_identifier ~ '^E[0-9]{2}-');

INSERT INTO ed_mfg_control.lot_deviation (deviation_no, lot_id, item_no, raised, source_type, description, severity, dev_status)
SELECT d.deviation_identifier, d.batch_identifier, d.product_code,
       to_char(d.deviation_raised_timestamp AT TIME ZONE 'America/Edmonton', 'YYYY-MM-DD HH24:MI'), d.deviation_source_type,
       d.deviation_description, d.deviation_severity, d.deviation_current_status
  FROM incoming_deviation d
 WHERE d.discard_reason IS NULL
ON CONFLICT (deviation_no) DO UPDATE SET lot_id = EXCLUDED.lot_id, item_no = EXCLUDED.item_no, raised = EXCLUDED.raised,
       source_type = EXCLUDED.source_type, description = EXCLUDED.description, severity = EXCLUDED.severity,
       dev_status = EXCLUDED.dev_status;

UPDATE incoming_investigation i SET discard_reason = 'investigation of a deviation not against an Edmonton lot'
 WHERE NOT EXISTS (SELECT 1 FROM ed_mfg_control.lot_deviation l WHERE l.deviation_no = i.deviation_identifier);

UPDATE ed_mfg_control.lot_deviation l
   SET investigator = i.deviation_investigator_identifier, investigated_on = i.deviation_investigation_completed_date,
       root_cause = i.deviation_root_cause_description, impact = i.deviation_impact_description,
       disposition = i.deviation_disposition_status
  FROM incoming_investigation i
 WHERE i.discard_reason IS NULL AND i.deviation_identifier = l.deviation_no;

UPDATE incoming_corrective_action SET discard_reason = 'corrective actions are followed up in the QMS, not the batch record';
