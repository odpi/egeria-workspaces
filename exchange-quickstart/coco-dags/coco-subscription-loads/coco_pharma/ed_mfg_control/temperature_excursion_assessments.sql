-- Subscription: coco_ed_mfg_control__temperature_excursion_assessments - Edmonton Manufacturing Control System (Coco core) receives Temperature Excursion Assessments
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (disposition recorded)
-- Keeps excursion assessments of shipments from Edmonton lots in excursion_review (NEW, reviewed as local text).
-- Discards assessments of other factories' batches.  No system supplies this product yet.

UPDATE incoming_excursion_assessment x SET discard_reason = 'not an Edmonton lot' WHERE NOT (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = x.batch_identifier) OR x.batch_identifier ~ '^E[0-9]{2}-');

INSERT INTO ed_mfg_control.excursion_review (excursion_no, shipment_no, item_no, lot_id, reviewer, reviewed, stability_ref,
       disposition, notes)
SELECT x.excursion_identifier, x.shipment_identifier, x.product_code, x.batch_identifier, x.excursion_assessor_identifier,
       to_char(x.excursion_assessment_timestamp AT TIME ZONE 'America/Edmonton', 'YYYY-MM-DD HH24:MI'),
       x.excursion_stability_reference_identifier, x.excursion_disposition_status, x.excursion_assessment_notes
  FROM incoming_excursion_assessment x
 WHERE x.discard_reason IS NULL
ON CONFLICT (excursion_no) DO UPDATE SET shipment_no = EXCLUDED.shipment_no, item_no = EXCLUDED.item_no, lot_id = EXCLUDED.lot_id,
       reviewer = EXCLUDED.reviewer, reviewed = EXCLUDED.reviewed, stability_ref = EXCLUDED.stability_ref,
       disposition = EXCLUDED.disposition, notes = EXCLUDED.notes;
