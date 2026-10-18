-- Subscription: coco_ed_mfg_control__equipment_qualification_status - Edmonton Manufacturing Control System (Coco core) receives Equipment Qualification Status
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Batch Execution Records depends on it (qualification status)
-- Keeps the Edmonton factory's equipment (EDM- asset tags) with its qualification and calibration status in
-- equipment_status (NEW, calibration expiry as text DD/MM/YYYY as in equip_log).  Discards other sites'
-- equipment - today all of it, from the Austin (US10) and EKG (RO10) maintenance systems.

UPDATE incoming_equipment SET discard_reason = 'not Edmonton equipment' WHERE equipment_identifier NOT LIKE 'EDM-%';
UPDATE incoming_qualification_status SET discard_reason = 'not Edmonton equipment' WHERE equipment_identifier NOT LIKE 'EDM-%';

INSERT INTO ed_mfg_control.equipment_status (asset_tag, asset_name, asset_type, asset_status)
SELECT e.equipment_identifier, e.equipment_name, e.equipment_type, e.equipment_current_status
  FROM incoming_equipment e
 WHERE e.discard_reason IS NULL
ON CONFLICT (asset_tag) DO UPDATE SET asset_name = EXCLUDED.asset_name, asset_type = EXCLUDED.asset_type,
       asset_status = EXCLUDED.asset_status;

INSERT INTO ed_mfg_control.equipment_status (asset_tag, qual_state, qualified_on, requal_due, calibrated_on, cal_exp)
SELECT q.equipment_identifier, q.equipment_qualified_status, q.equipment_qualified_date, q.equipment_qualified_end_date,
       q.equipment_calibration_date, to_char(q.equipment_calibration_end_date, 'DD/MM/YYYY')
  FROM incoming_qualification_status q
 WHERE q.discard_reason IS NULL
ON CONFLICT (asset_tag) DO UPDATE SET qual_state = EXCLUDED.qual_state, qualified_on = EXCLUDED.qualified_on,
       requal_due = EXCLUDED.requal_due, calibrated_on = EXCLUDED.calibrated_on, cal_exp = EXCLUDED.cal_exp;
