-- Subscription: buc_veeva_qms__batch_execution_records - Veeva Vault QMS (Bucharest) receives Batch Execution Records
-- Destination: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Why it subscribes: Deviations And CAPAs depends on it (raise deviation)
-- Vault QMS needs from batch execution only the steps completed with an exception, which must have a deviation: for an
-- EKG batch the deviation is raised in Vault from the MES exception report, so an exception step whose batch already
-- has a Vault quality event is discarded as already raised, one without as awaiting QA's deviation (creating a quality
-- event here would feed back into Deviations And CAPAs).  Normal steps and material/equipment use are not kept.  Other
-- companies' batches are discarded (Coco group data - EKG is not yet integrated).
UPDATE incoming_execution_step SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE batch_identifier !~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_execution_step SET discard_reason = 'step completed normally - no quality event'
 WHERE discard_reason IS NULL AND execution_step_status IS DISTINCT FROM 'complete with deviation';
UPDATE incoming_execution_step i SET discard_reason = 'deviation already raised in Vault'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM veeva_qms.quality_event__qdm q WHERE q.object_type__v = 'deviation__c' AND q.batch_number__c = i.batch_identifier);
UPDATE incoming_execution_step SET discard_reason = 'exception awaiting a deviation from QA (raised in Vault from the MES report)'
 WHERE discard_reason IS NULL;
UPDATE incoming_material_usage SET discard_reason = 'execution detail is not kept in the QMS'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_material_usage SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_equipment_usage SET discard_reason = 'execution detail is not kept in the QMS'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_equipment_usage SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
