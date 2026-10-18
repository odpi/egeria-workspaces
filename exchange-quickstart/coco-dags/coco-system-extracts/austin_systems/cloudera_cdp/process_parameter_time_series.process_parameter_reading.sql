-- Extract: Cloudera Data Platform (Primary Cluster) (Austin) -> Process Parameter Time Series / process_parameter_reading
-- Source: austin_systems.cloudera_cdp (SoftwareServer::AUS-SYS-001::CDH-AUS-7X-00142)
-- Target: coco_data_hub.process_parameter_time_series.process_parameter_reading
-- mfg_curated.sensor_telemetry; epoch milliseconds converted to timestamptz; limited to readings before the
-- Historian/Kafka era (dt < 2026-08-01).
SELECT
  t.equipment_id::varchar(40) AS equipment_identifier,
  t.tag_name::varchar(40) AS process_parameter_code,
  to_timestamp(t.event_ts / 1000.0) AS process_parameter_timestamp,
  t.batch_id::varchar(40) AS batch_identifier,
  t.reading AS process_parameter_value,
  t.uom::varchar(20) AS process_parameter_unit,
  t.spec_lo AS process_parameter_minimum_value,
  t.spec_hi AS process_parameter_maximum_value
FROM cloudera_cdp.sensor_telemetry t
WHERE t.dt < '2026-08-01'
