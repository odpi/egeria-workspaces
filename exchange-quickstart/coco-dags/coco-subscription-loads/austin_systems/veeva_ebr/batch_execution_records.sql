-- Subscription: aus_veeva_ebr__batch_execution_records - Veeva Vault EBR (Austin) receives Batch Execution Records
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (execution record)
-- Keeps the executed steps, material consumption and equipment use of the Austin site's batches (including the Coco
-- products made at Austin) that have a batch record in the vault, as NEW execution_step__c, material_consumption__c
-- and equipment_use__c records for review by exception. batch_record_section__c, which the extracts read, is not
-- written. Coco Winchester/Edmonton batches and EKG batches are discarded.

UPDATE incoming_execution_step i SET discard_reason = CASE
       WHEN i.batch_identifier ~ '^[WE][0-9]{2}-' THEN 'other estate: Coco factory batch'
       WHEN i.batch_identifier ~ '^A[0-9]{2}-' THEN 'no batch record in this vault'
       ELSE 'other estate: not an Austin batch' END
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.execution_step__c
       (id, name__v, batch__c, step_number__c, step_code__c, start_datetime__c, end_datetime__c,
        performer_pseudonym__c, signature__c, step_status__c)
SELECT ('0ES' || upper(substr(md5(i.batch_identifier || '|' || i.execution_step_number), 1, 11))),
       i.batch_identifier || '-' || lpad(i.execution_step_number::text, 2, '0'), b.id, i.execution_step_number,
       i.execution_step_code, i.execution_step_start_timestamp, i.execution_step_end_timestamp,
       i.worker_pseudonym_identifier, i.execution_step_signature, i.execution_step_status
  FROM incoming_execution_step i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch__c = EXCLUDED.batch__c, step_number__c = EXCLUDED.step_number__c,
       step_code__c = EXCLUDED.step_code__c, start_datetime__c = EXCLUDED.start_datetime__c,
       end_datetime__c = EXCLUDED.end_datetime__c, performer_pseudonym__c = EXCLUDED.performer_pseudonym__c,
       signature__c = EXCLUDED.signature__c, step_status__c = EXCLUDED.step_status__c;

UPDATE incoming_material_usage i SET discard_reason = CASE
       WHEN i.batch_identifier ~ '^[WE][0-9]{2}-' THEN 'other estate: Coco factory batch'
       WHEN i.batch_identifier ~ '^A[0-9]{2}-' THEN 'no batch record in this vault'
       ELSE 'other estate: not an Austin batch' END
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.material_consumption__c
       (id, batch__c, step_number__c, lot__c, material_code__c, quantity__c, unit__c)
SELECT ('0MC' || upper(substr(md5(i.batch_identifier || '|' || i.execution_step_number || '|' || i.lot_identifier), 1, 11))),
       b.id, i.execution_step_number, i.lot_identifier, i.raw_material_code, i.raw_material_used_quantity,
       i.raw_material_used_unit
  FROM incoming_material_usage i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       batch__c = EXCLUDED.batch__c, step_number__c = EXCLUDED.step_number__c, lot__c = EXCLUDED.lot__c,
       material_code__c = EXCLUDED.material_code__c, quantity__c = EXCLUDED.quantity__c, unit__c = EXCLUDED.unit__c;

UPDATE incoming_equipment_usage i SET discard_reason = CASE
       WHEN i.batch_identifier ~ '^[WE][0-9]{2}-' THEN 'other estate: Coco factory batch'
       WHEN i.batch_identifier ~ '^A[0-9]{2}-' THEN 'no batch record in this vault'
       ELSE 'other estate: not an Austin batch' END
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.equipment_use__c
       (id, batch__c, step_number__c, equipment__c, qualification_status__c, calibration_due__c)
SELECT ('0EU' || upper(substr(md5(i.batch_identifier || '|' || i.execution_step_number || '|' || i.equipment_identifier), 1, 11))),
       b.id, i.execution_step_number, i.equipment_identifier, i.equipment_qualified_status,
       i.equipment_calibration_end_date
  FROM incoming_equipment_usage i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       batch__c = EXCLUDED.batch__c, step_number__c = EXCLUDED.step_number__c, equipment__c = EXCLUDED.equipment__c,
       qualification_status__c = EXCLUDED.qualification_status__c, calibration_due__c = EXCLUDED.calibration_due__c;
