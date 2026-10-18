-- Subscription: coco_ed_mfg_control__batch_execution_records - Edmonton Manufacturing Control System (Coco core) receives Batch Execution Records
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (execution record)
-- Keeps nothing: the execution records of Edmonton lots are this system's own (op_log, consumption,
-- equip_log), so they come back as rows it already holds; the rest are other factories' batches (Winchester,
-- the Austin site, EKG), recorded by their own control systems.

UPDATE incoming_execution_step s SET discard_reason = 'Edmonton lot - execution recorded in this system' WHERE (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = s.batch_identifier) OR s.batch_identifier ~ '^E[0-9]{2}-');
UPDATE incoming_execution_step SET discard_reason = 'not an Edmonton lot' WHERE discard_reason IS NULL;

UPDATE incoming_material_usage m SET discard_reason = 'Edmonton lot - execution recorded in this system' WHERE (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = m.batch_identifier) OR m.batch_identifier ~ '^E[0-9]{2}-');
UPDATE incoming_material_usage SET discard_reason = 'not an Edmonton lot' WHERE discard_reason IS NULL;

UPDATE incoming_equipment_usage e SET discard_reason = 'Edmonton lot - execution recorded in this system' WHERE (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = e.batch_identifier) OR e.batch_identifier ~ '^E[0-9]{2}-');
UPDATE incoming_equipment_usage SET discard_reason = 'not an Edmonton lot' WHERE discard_reason IS NULL;
