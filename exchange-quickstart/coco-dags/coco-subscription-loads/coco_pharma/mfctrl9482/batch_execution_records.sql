-- Subscription: coco_mfctrl9482__batch_execution_records - Austin Manufacturing Control System (Coco core) receives Batch Execution Records
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Electronic Batch Records depends on it (execution record)
-- Keeps what the Austin site's own MES recorded for the shared Coco batches (A26- batches of products 3000, 2050
-- and 9000 - the Coco/Austin manufacturing integration) that MFCTRL9482 does not hold itself: steps, the
-- Austin-sourced material lots and the site's US10- equipment, in mfc_mes_operation, mfc_mes_consumption and
-- mfc_mes_equipment_use (all NEW) for the batch record review.  Discards the rows MFCTRL9482 supplied (same
-- batch, step and lot or equipment), Austin's own products' batches (AU- products) and other factories' batches.

UPDATE incoming_execution_step s SET discard_reason = 'step recorded in MFCTRL9482 - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM mfctrl9482.mfc_operation o WHERE o.batch_id = s.batch_identifier AND o.op_seq = s.execution_step_number * 10);
UPDATE incoming_execution_step s SET discard_reason = 'not a shared Coco batch made at the Austin site'
 WHERE s.discard_reason IS NULL AND NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = s.batch_identifier) OR s.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_mes_operation (batch_id, step_no, op_code, start_utc, end_utc, mes_signer, mes_signature, step_status)
SELECT s.batch_identifier, s.execution_step_number, s.execution_step_code, s.execution_step_start_timestamp,
       s.execution_step_end_timestamp, s.worker_pseudonym_identifier, s.execution_step_signature, s.execution_step_status
  FROM incoming_execution_step s
 WHERE s.discard_reason IS NULL
ON CONFLICT (batch_id, step_no) DO UPDATE SET op_code = EXCLUDED.op_code, start_utc = EXCLUDED.start_utc, end_utc = EXCLUDED.end_utc,
       mes_signer = EXCLUDED.mes_signer, mes_signature = EXCLUDED.mes_signature, step_status = EXCLUDED.step_status;

UPDATE incoming_material_usage m SET discard_reason = 'consumption recorded in MFCTRL9482 - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM mfctrl9482.mfc_consumption c
                WHERE c.batch_id = m.batch_identifier AND c.op_seq = m.execution_step_number * 10 AND c.lot_no = m.lot_identifier);
UPDATE incoming_material_usage m SET discard_reason = 'not a shared Coco batch made at the Austin site'
 WHERE m.discard_reason IS NULL AND NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = m.batch_identifier) OR m.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_mes_consumption (batch_id, step_no, lot_no, item_cd, qty_consumed, uom)
SELECT m.batch_identifier, m.execution_step_number, m.lot_identifier, m.raw_material_code, m.raw_material_used_quantity,
       upper(m.raw_material_used_unit)
  FROM incoming_material_usage m
 WHERE m.discard_reason IS NULL
ON CONFLICT (batch_id, step_no, lot_no) DO UPDATE SET item_cd = EXCLUDED.item_cd, qty_consumed = EXCLUDED.qty_consumed, uom = EXCLUDED.uom;

UPDATE incoming_equipment_usage e SET discard_reason = 'equipment use recorded in MFCTRL9482 - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM mfctrl9482.mfc_equipment_use u
                WHERE u.batch_id = e.batch_identifier AND u.op_seq = e.execution_step_number * 10 AND u.equip_id = e.equipment_identifier);
UPDATE incoming_equipment_usage e SET discard_reason = 'not a shared Coco batch made at the Austin site'
 WHERE e.discard_reason IS NULL AND NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = e.batch_identifier) OR e.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_mes_equipment_use (batch_id, step_no, equip_id, qual_status, cal_expiry)
SELECT e.batch_identifier, e.execution_step_number, e.equipment_identifier, upper(e.equipment_qualified_status),
       e.equipment_calibration_end_date
  FROM incoming_equipment_usage e
 WHERE e.discard_reason IS NULL
ON CONFLICT (batch_id, step_no, equip_id) DO UPDATE SET qual_status = EXCLUDED.qual_status, cal_expiry = EXCLUDED.cal_expiry;
