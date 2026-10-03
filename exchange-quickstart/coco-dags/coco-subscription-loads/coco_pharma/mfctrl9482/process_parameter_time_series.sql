-- Subscription: coco_mfctrl9482__process_parameter_time_series - Austin Manufacturing Control System (Coco core) receives Process Parameter Time Series
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Electronic Batch Records depends on it (process parameters)
-- Keeps the readings the Austin site historian recorded during the shared Coco batches (A26- batches of 3000, 2050
-- and 9000) in mfc_param_reading (NEW) for the PARAM section of the batch record.  Discards readings outside a
-- shared batch (Austin's own products, idle equipment) and EKG's readings.

UPDATE incoming_process_parameter_reading r SET discard_reason = 'not taken during a shared Coco batch'
 WHERE r.batch_identifier IS NULL OR NOT (EXISTS (SELECT 1 FROM mfctrl9482.mfc_batch b WHERE b.batch_id = r.batch_identifier) OR r.batch_identifier ~ '^A[0-9]{2}-(3000|2050|9000)-');

INSERT INTO mfctrl9482.mfc_param_reading (equip_id, param_code, reading_utc, batch_id, reading, unit, low_limit, high_limit)
SELECT r.equipment_identifier, r.process_parameter_code, r.process_parameter_timestamp, r.batch_identifier,
       r.process_parameter_value, r.process_parameter_unit, r.process_parameter_minimum_value, r.process_parameter_maximum_value
  FROM incoming_process_parameter_reading r
 WHERE r.discard_reason IS NULL
ON CONFLICT (equip_id, param_code, reading_utc) DO UPDATE SET batch_id = EXCLUDED.batch_id, reading = EXCLUDED.reading,
       unit = EXCLUDED.unit, low_limit = EXCLUDED.low_limit, high_limit = EXCLUDED.high_limit;
