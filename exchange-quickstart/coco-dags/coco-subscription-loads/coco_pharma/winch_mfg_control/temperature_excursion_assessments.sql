-- Subscription: coco_winch_mfg_control__temperature_excursion_assessments - Winchester Manufacturing Control System (Coco core) receives Temperature Excursion Assessments
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (disposition recorded)
-- Keeps excursion assessments of shipments from Winchester batches in wexc (NEW), recorded in the EXC section of
-- the batch record.  Discards assessments of other factories' batches.  No system supplies this product yet.

UPDATE incoming_excursion_assessment x SET discard_reason = 'not a Winchester batch'
 WHERE NOT (EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = x.batch_identifier) OR x.batch_identifier ~ '^W[0-9]{2}-');

INSERT INTO winch_mfg_control.wexc (exc_ref, ship_ref, prd_cd, batch_no, assessor, assess_ts, stab_ref, disp, notes)
SELECT x.excursion_identifier, x.shipment_identifier, x.product_code, x.batch_identifier, x.excursion_assessor_identifier,
       x.excursion_assessment_timestamp, x.excursion_stability_reference_identifier, x.excursion_disposition_status,
       x.excursion_assessment_notes
  FROM incoming_excursion_assessment x
 WHERE x.discard_reason IS NULL
ON CONFLICT (exc_ref) DO UPDATE SET ship_ref = EXCLUDED.ship_ref, prd_cd = EXCLUDED.prd_cd, batch_no = EXCLUDED.batch_no,
       assessor = EXCLUDED.assessor, assess_ts = EXCLUDED.assess_ts, stab_ref = EXCLUDED.stab_ref, disp = EXCLUDED.disp,
       notes = EXCLUDED.notes;
