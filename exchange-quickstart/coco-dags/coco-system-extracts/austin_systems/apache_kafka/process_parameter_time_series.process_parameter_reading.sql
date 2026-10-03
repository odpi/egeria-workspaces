-- Extract: Apache Kafka (Austin) -> Process Parameter Time Series / process_parameter_reading
-- Source: austin_systems.apache_kafka (SoftwareServer::AUS-SYS-007::KAFKA-AUS-001)
-- Target: coco_data_hub.process_parameter_time_series.process_parameter_reading
-- topic_record JSON payloads from the aus.ot.* telemetry topics; limits carried in the payload.
SELECT
  (r.record_value ->> 'assetId')::varchar(40) AS equipment_identifier,
  (r.record_value ->> 'signal')::varchar(40) AS process_parameter_code,
  (r.record_value ->> 'ts')::timestamptz AS process_parameter_timestamp,
  (r.record_value ->> 'batchId')::varchar(40) AS batch_identifier,
  (r.record_value ->> 'value')::double precision AS process_parameter_value,
  (r.record_value ->> 'uom')::varchar(20) AS process_parameter_unit,
  (r.record_value -> 'limits' ->> 'lo')::double precision AS process_parameter_minimum_value,
  (r.record_value -> 'limits' ->> 'hi')::double precision AS process_parameter_maximum_value
FROM apache_kafka.topic_record r
WHERE r.topic LIKE 'aus.ot.%.telemetry'
