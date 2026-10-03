-- Subscription: aus_veeva_ebr__process_parameter_time_series - Veeva Vault EBR (Austin) receives Process Parameter Time Series
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (process parameters)
-- Keeps the readings taken on Austin equipment in the context of a batch that has a record in this vault, as NEW
-- process_parameter__c records (the reviewer checks them against the proven acceptable range). Readings with no
-- batch context (idle equipment) and EKG's RO10 readings are discarded.

UPDATE incoming_process_parameter_reading i SET discard_reason = 'other estate: not Austin equipment'
 WHERE i.equipment_identifier !~ '^US[0-9]{2}-';
UPDATE incoming_process_parameter_reading i SET discard_reason = 'no batch context'
 WHERE i.discard_reason IS NULL AND i.batch_identifier IS NULL;
UPDATE incoming_process_parameter_reading i SET discard_reason = 'no batch record in this vault'
 WHERE i.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM veeva_ebr.batch__v b WHERE b.name__v = i.batch_identifier);
INSERT INTO veeva_ebr.process_parameter__c
       (id, batch__c, equipment__c, parameter__c, reading_datetime__c, reading_value__c, unit__c, range_min__c,
        range_max__c)
SELECT ('0PP' || upper(substr(md5(i.equipment_identifier || '|' || i.process_parameter_code || '|' || i.process_parameter_timestamp), 1, 11))),
       b.id, i.equipment_identifier, i.process_parameter_code, i.process_parameter_timestamp,
       i.process_parameter_value, i.process_parameter_unit, i.process_parameter_minimum_value,
       i.process_parameter_maximum_value
  FROM incoming_process_parameter_reading i JOIN veeva_ebr.batch__v b ON b.name__v = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       batch__c = EXCLUDED.batch__c, equipment__c = EXCLUDED.equipment__c, parameter__c = EXCLUDED.parameter__c,
       reading_datetime__c = EXCLUDED.reading_datetime__c, reading_value__c = EXCLUDED.reading_value__c,
       unit__c = EXCLUDED.unit__c, range_min__c = EXCLUDED.range_min__c, range_max__c = EXCLUDED.range_max__c;
