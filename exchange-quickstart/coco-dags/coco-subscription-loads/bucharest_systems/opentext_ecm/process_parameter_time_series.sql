-- Subscription: buc_opentext_ecm__process_parameter_time_series - OpenText ECM (Bucharest) receives Process Parameter Time Series
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (process parameters)
-- The process parameters of a batch are part of the signed batch record PDF archived from the MES (its FactoryTalk data
-- set), so EKG readings (RO10 equipment) are discarded; other sites' readings are discarded as Coco group data (EKG is
-- not yet integrated).  Nothing is written.
UPDATE incoming_process_parameter_reading SET discard_reason = 'parameters are in the signed batch record PDF'
 WHERE equipment_identifier LIKE 'RO10-%';
UPDATE incoming_process_parameter_reading SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
