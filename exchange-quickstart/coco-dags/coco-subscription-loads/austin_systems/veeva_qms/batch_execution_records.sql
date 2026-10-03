-- Subscription: aus_veeva_qms__batch_execution_records - Veeva Vault QMS (Austin) receives Batch Execution Records
-- Destination: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Why it subscribes: Deviations And CAPAs depends on it (raise deviation)
-- Keeps the exceptions a quality owner must consider raising a deviation for - Austin batch steps completed with a
-- deviation and equipment used when not qualified - as NEW mes_exception__c records; quality_event__qdm, which feeds
-- Deviations And CAPAs, is only written when the owner raises one. Steps completed normally, qualified equipment
-- use, material usage and other estates' batches are discarded.

UPDATE incoming_execution_step i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_execution_step i SET discard_reason = 'step completed without exception'
 WHERE i.discard_reason IS NULL AND i.execution_step_status = 'complete';
INSERT INTO veeva_qms.mes_exception__c
       (id, name__v, batch_number__c, step_number__c, exception_type__c, detail__c, occurred_datetime__c)
SELECT ('0MX' || upper(substr(md5(i.batch_identifier || '|' || i.execution_step_number || '|step'), 1, 11))),
       i.batch_identifier || '-' || lpad(i.execution_step_number::text, 2, '0'), i.batch_identifier,
       i.execution_step_number, 'step__c', i.execution_step_code || ': ' || i.execution_step_status,
       i.execution_step_end_timestamp
  FROM incoming_execution_step i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch_number__c = EXCLUDED.batch_number__c,
       step_number__c = EXCLUDED.step_number__c, exception_type__c = EXCLUDED.exception_type__c,
       detail__c = EXCLUDED.detail__c, occurred_datetime__c = EXCLUDED.occurred_datetime__c;

UPDATE incoming_equipment_usage i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_equipment_usage i SET discard_reason = 'equipment qualified at use'
 WHERE i.discard_reason IS NULL AND i.equipment_qualified_status = 'qualified';
INSERT INTO veeva_qms.mes_exception__c
       (id, name__v, batch_number__c, step_number__c, exception_type__c, detail__c, occurred_datetime__c)
SELECT ('0MX' || upper(substr(md5(i.batch_identifier || '|' || i.execution_step_number || '|' || i.equipment_identifier), 1, 11))),
       i.batch_identifier || '-' || lpad(i.execution_step_number::text, 2, '0') || '-' || i.equipment_identifier,
       i.batch_identifier, i.execution_step_number, 'equipment__c',
       i.equipment_identifier || ' used while ' || i.equipment_qualified_status
         || coalesce('; calibration due ' || i.equipment_calibration_end_date, ''), NULL
  FROM incoming_equipment_usage i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, batch_number__c = EXCLUDED.batch_number__c,
       step_number__c = EXCLUDED.step_number__c, exception_type__c = EXCLUDED.exception_type__c,
       detail__c = EXCLUDED.detail__c, occurred_datetime__c = EXCLUDED.occurred_datetime__c;

UPDATE incoming_material_usage SET discard_reason = 'material usage not needed for deviation intake';
