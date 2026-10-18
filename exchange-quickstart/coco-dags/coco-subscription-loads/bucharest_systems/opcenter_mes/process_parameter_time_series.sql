-- Subscription: buc_opcenter_mes__process_parameter_time_series - Siemens Opcenter MES (Bucharest) receives Process Parameter Time Series
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Electronic Batch Records depends on it (process parameters)
-- The EBR refers to FactoryTalk's batch data set (PROCESSDATA section, FTV-<batch>) rather than holding the readings, so
-- EKG readings (RO10 equipment) are discarded; other sites' readings are discarded as Coco group data (EKG is not yet
-- integrated).  Nothing is written.
UPDATE incoming_process_parameter_reading
   SET discard_reason = 'the EBR references the FactoryTalk batch data set, not individual readings'
 WHERE equipment_identifier LIKE 'RO10-%';
UPDATE incoming_process_parameter_reading SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
