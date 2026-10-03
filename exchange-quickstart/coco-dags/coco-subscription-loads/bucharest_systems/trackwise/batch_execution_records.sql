-- Subscription: buc_trackwise__batch_execution_records - Trackwise Digital (Bucharest) receives Batch Execution Records
-- Destination: bucharest_systems.trackwise (SoftwareServer::SYS-005::Trackwise Digital)
-- Why it subscribes: Deviations And CAPAs depends on it (raise deviation)
-- Trackwise handles EKG's audit, inspection and supplier quality events; manufacturing deviations from batch execution
-- are raised in Veeva QMS.  So EKG batch execution records are discarded for that reason and other companies' as Coco
-- group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_execution_step SET discard_reason = 'manufacturing deviations are raised in Veeva QMS, not Trackwise'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_execution_step SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_material_usage SET discard_reason = 'manufacturing deviations are raised in Veeva QMS, not Trackwise'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_material_usage SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_equipment_usage SET discard_reason = 'manufacturing deviations are raised in Veeva QMS, not Trackwise'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_equipment_usage SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
