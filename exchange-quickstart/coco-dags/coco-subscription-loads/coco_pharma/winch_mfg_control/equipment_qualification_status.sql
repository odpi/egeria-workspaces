-- Subscription: coco_winch_mfg_control__equipment_qualification_status - Winchester Manufacturing Control System (Coco core) receives Equipment Qualification Status
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Batch Execution Records depends on it (qualification status)
-- Keeps the Winchester factory's equipment (WIN- asset numbers) with its qualification and calibration status in
-- weq_qual (NEW), checked when a step starts; wstep_eq keeps the status read at use.  Discards other sites'
-- equipment - today all of it, from the Austin (US10) and EKG (RO10) maintenance systems.

UPDATE incoming_equipment SET discard_reason = 'not Winchester equipment' WHERE equipment_identifier NOT LIKE 'WIN-%';
UPDATE incoming_qualification_status SET discard_reason = 'not Winchester equipment' WHERE equipment_identifier NOT LIKE 'WIN-%';

INSERT INTO winch_mfg_control.weq_qual (eq_id, eq_nm, eq_typ, eq_sts)
SELECT e.equipment_identifier, e.equipment_name, e.equipment_type, e.equipment_current_status
  FROM incoming_equipment e
 WHERE e.discard_reason IS NULL
ON CONFLICT (eq_id) DO UPDATE SET eq_nm = EXCLUDED.eq_nm, eq_typ = EXCLUDED.eq_typ, eq_sts = EXCLUDED.eq_sts;

INSERT INTO winch_mfg_control.weq_qual (eq_id, qual_sts, qual_dt, qual_end, cal_dt, cal_end)
SELECT q.equipment_identifier, q.equipment_qualified_status, q.equipment_qualified_date, q.equipment_qualified_end_date,
       q.equipment_calibration_date, q.equipment_calibration_end_date
  FROM incoming_qualification_status q
 WHERE q.discard_reason IS NULL
ON CONFLICT (eq_id) DO UPDATE SET qual_sts = EXCLUDED.qual_sts, qual_dt = EXCLUDED.qual_dt, qual_end = EXCLUDED.qual_end,
       cal_dt = EXCLUDED.cal_dt, cal_end = EXCLUDED.cal_end;
