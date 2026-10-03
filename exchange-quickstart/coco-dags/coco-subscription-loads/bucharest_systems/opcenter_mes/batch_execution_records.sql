-- Subscription: buc_opcenter_mes__batch_execution_records - Siemens Opcenter MES (Bucharest) receives Batch Execution Records
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Electronic Batch Records depends on it (execution record)
-- Opcenter is the source of EKG's batch execution records (historymainline, componentissuehistory,
-- resourceusagehistory), so every step, material and equipment use of an EKG batch (a container of this MES) is already
-- held here and is discarded (no feedback loop); other batches are discarded as Coco group data (EKG is not yet
-- integrated).  Nothing is written.
UPDATE incoming_execution_step i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_material_usage i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_equipment_usage i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_execution_step SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_material_usage SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_equipment_usage SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
