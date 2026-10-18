-- Subscription: coco_winch_mfg_control__batch_execution_records - Winchester Manufacturing Control System (Coco core) receives Batch Execution Records
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (execution record)
-- Keeps nothing: the execution records of Winchester batches are this system's own (wstep, wmatl, wstep_eq), so
-- they come back as rows it already holds; the rest are other factories' batches (Edmonton, the Austin site,
-- EKG), whose execution is recorded by their own control systems.

UPDATE incoming_execution_step s SET discard_reason = 'Winchester batch - execution recorded in this system'
 WHERE EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = s.batch_identifier) OR s.batch_identifier ~ '^W[0-9]{2}-';
UPDATE incoming_execution_step SET discard_reason = 'not a Winchester batch' WHERE discard_reason IS NULL;

UPDATE incoming_material_usage m SET discard_reason = 'Winchester batch - execution recorded in this system'
 WHERE EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = m.batch_identifier) OR m.batch_identifier ~ '^W[0-9]{2}-';
UPDATE incoming_material_usage SET discard_reason = 'not a Winchester batch' WHERE discard_reason IS NULL;

UPDATE incoming_equipment_usage e SET discard_reason = 'Winchester batch - execution recorded in this system'
 WHERE EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = e.batch_identifier) OR e.batch_identifier ~ '^W[0-9]{2}-';
UPDATE incoming_equipment_usage SET discard_reason = 'not a Winchester batch' WHERE discard_reason IS NULL;
