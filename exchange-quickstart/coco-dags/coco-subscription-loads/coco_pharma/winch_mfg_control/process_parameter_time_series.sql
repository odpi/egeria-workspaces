-- Subscription: coco_winch_mfg_control__process_parameter_time_series - Winchester Manufacturing Control System (Coco core) receives Process Parameter Time Series
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (process parameters)
-- Keeps readings from Winchester equipment (WIN- asset numbers) in wparam (NEW) for the PARAM section of the batch
-- record.  Discards other sites' readings - today all of them, from the Austin and EKG historians.

UPDATE incoming_process_parameter_reading SET discard_reason = 'reading from another site''s equipment'
 WHERE equipment_identifier NOT LIKE 'WIN-%';

INSERT INTO winch_mfg_control.wparam (eq_id, param_cd, read_ts, batch_no, val, uom, lo, hi)
SELECT r.equipment_identifier, r.process_parameter_code, r.process_parameter_timestamp, r.batch_identifier,
       r.process_parameter_value, r.process_parameter_unit, r.process_parameter_minimum_value, r.process_parameter_maximum_value
  FROM incoming_process_parameter_reading r
 WHERE r.discard_reason IS NULL
ON CONFLICT (eq_id, param_cd, read_ts) DO UPDATE SET batch_no = EXCLUDED.batch_no, val = EXCLUDED.val, uom = EXCLUDED.uom,
       lo = EXCLUDED.lo, hi = EXCLUDED.hi;
