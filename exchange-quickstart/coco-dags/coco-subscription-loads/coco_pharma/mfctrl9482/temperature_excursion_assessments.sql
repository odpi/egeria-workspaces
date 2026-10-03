-- Subscription: coco_mfctrl9482__temperature_excursion_assessments - Austin Manufacturing Control System (Coco core) receives Temperature Excursion Assessments
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Electronic Batch Records depends on it (disposition recorded)
-- Keeps excursion assessments of shipments from the shared Coco batches made at the Austin site in mfc_excursion
-- (NEW).  Discards assessments of other batches.  No system supplies this product yet.

UPDATE incoming_excursion_assessment x SET discard_reason = 'not a shared Coco batch made at the Austin site' WHERE NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = x.batch_identifier) OR x.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_excursion (excursion_id, shipment_id, product_cd, batch_id, assessor, assessed_utc, stability_ref,
       disposition, notes)
SELECT x.excursion_identifier, x.shipment_identifier, x.product_code, x.batch_identifier, x.excursion_assessor_identifier,
       x.excursion_assessment_timestamp, x.excursion_stability_reference_identifier, x.excursion_disposition_status,
       x.excursion_assessment_notes
  FROM incoming_excursion_assessment x
 WHERE x.discard_reason IS NULL
ON CONFLICT (excursion_id) DO UPDATE SET shipment_id = EXCLUDED.shipment_id, product_cd = EXCLUDED.product_cd,
       batch_id = EXCLUDED.batch_id, assessor = EXCLUDED.assessor, assessed_utc = EXCLUDED.assessed_utc,
       stability_ref = EXCLUDED.stability_ref, disposition = EXCLUDED.disposition, notes = EXCLUDED.notes;
