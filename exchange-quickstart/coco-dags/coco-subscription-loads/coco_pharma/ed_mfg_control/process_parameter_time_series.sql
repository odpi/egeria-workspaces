-- Subscription: coco_ed_mfg_control__process_parameter_time_series - Edmonton Manufacturing Control System (Coco core) receives Process Parameter Time Series
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (process parameters)
-- Keeps readings from Edmonton equipment (EDM- asset tags) in process_reading (NEW, read_at as local text) for
-- the process parameters section of the EBR.  Discards other sites' readings - today all of them, from the
-- Austin and EKG historians.

UPDATE incoming_process_parameter_reading SET discard_reason = 'reading from another site''s equipment'
 WHERE equipment_identifier NOT LIKE 'EDM-%';

INSERT INTO ed_mfg_control.process_reading (asset_tag, parameter, read_at, lot_id, reading, unit, low_limit, high_limit)
SELECT r.equipment_identifier, r.process_parameter_code,
       to_char(r.process_parameter_timestamp AT TIME ZONE 'America/Edmonton', 'YYYY-MM-DD HH24:MI'), r.batch_identifier,
       r.process_parameter_value, r.process_parameter_unit, r.process_parameter_minimum_value, r.process_parameter_maximum_value
  FROM incoming_process_parameter_reading r
 WHERE r.discard_reason IS NULL
ON CONFLICT (asset_tag, parameter, read_at) DO UPDATE SET lot_id = EXCLUDED.lot_id, reading = EXCLUDED.reading, unit = EXCLUDED.unit,
       low_limit = EXCLUDED.low_limit, high_limit = EXCLUDED.high_limit;
