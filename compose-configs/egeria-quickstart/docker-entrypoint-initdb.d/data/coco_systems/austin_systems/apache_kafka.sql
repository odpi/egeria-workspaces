-- system-qualified-name: SoftwareServer::AUS-SYS-007::KAFKA-AUS-001
-- Apache Kafka - Austin.  The Austin shop-floor streaming cluster.  Edge gateways on the sterile filling line and the
-- cell therapy suite publish telemetry straight to Kafka (not through the Historian); the landing table of those
-- topics feeds Process Parameter Time Series.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS apache_kafka;
COMMENT ON SCHEMA apache_kafka IS 'Apache Kafka (Austin): landing table for the OT telemetry topics (one row per consumed record).';

CREATE TABLE IF NOT EXISTS apache_kafka.topic_record (
  topic            varchar(120) NOT NULL,
  kafka_partition  integer NOT NULL,
  kafka_offset     bigint NOT NULL,
  record_key       varchar(200),
  record_value     jsonb NOT NULL,
  record_timestamp timestamptz NOT NULL,
  ingested_at      timestamptz NOT NULL,
  CONSTRAINT topic_record_pk PRIMARY KEY (topic, kafka_partition, kafka_offset)
);
COMMENT ON TABLE apache_kafka.topic_record IS 'Records consumed from the OT telemetry topics (value is the JSON payload).';

INSERT INTO apache_kafka.topic_record (topic, kafka_partition, kafka_offset, record_key, record_value, record_timestamp, ingested_at) VALUES
('aus.ot.filling.telemetry', 0, 18269, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-09-02T03:21:00Z", "value": 50.74, "uom": "g", "batchId": "A26-9000-0019", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-09-02 03:21:00.350000+00', '2026-09-02 03:21:02+00'),
('aus.ot.filling.telemetry', 0, 18294, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-09-02T05:27:00Z", "value": 49.95, "uom": "g", "batchId": "A26-9000-0019", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-09-02 05:27:00.350000+00', '2026-09-02 05:27:02+00'),
('aus.ot.filling.telemetry', 0, 18322, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-09-02T07:33:00Z", "value": 50.37, "uom": "g", "batchId": "A26-9000-0019", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-09-02 07:33:00.350000+00', '2026-09-02 07:33:02+00'),
('aus.ot.filling.telemetry', 0, 18351, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-09-02T03:21:00Z", "value": 44.01, "uom": "Pa", "batchId": "A26-9000-0019", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-09-02 03:21:00.350000+00', '2026-09-02 03:21:02+00'),
('aus.ot.filling.telemetry', 0, 18376, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-09-02T05:27:00Z", "value": 45.99, "uom": "Pa", "batchId": "A26-9000-0019", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-09-02 05:27:00.350000+00', '2026-09-02 05:27:02+00'),
('aus.ot.filling.telemetry', 0, 18404, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-09-02T07:33:00Z", "value": 38.52, "uom": "Pa", "batchId": "A26-9000-0019", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-09-02 07:33:00.350000+00', '2026-09-02 07:33:02+00'),
('aus.ot.filling.telemetry', 0, 18436, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-07-21T02:30:00Z", "value": 50.81, "uom": "g", "batchId": "A26-4410-0052", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-07-21 02:30:00.350000+00', '2026-07-21 02:30:02+00'),
('aus.ot.filling.telemetry', 0, 18438, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-07-21T04:31:00Z", "value": 50.68, "uom": "g", "batchId": "A26-4410-0052", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-07-21 04:31:00.350000+00', '2026-07-21 04:31:02+00'),
('aus.ot.filling.telemetry', 0, 18477, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-07-21T06:31:00Z", "value": 50.52, "uom": "g", "batchId": "A26-4410-0052", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-07-21 06:31:00.350000+00', '2026-07-21 06:31:02+00'),
('aus.ot.filling.telemetry', 0, 18509, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-07-21T02:30:00Z", "value": 40.5, "uom": "Pa", "batchId": "A26-4410-0052", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-07-21 02:30:00.350000+00', '2026-07-21 02:30:02+00'),
('aus.ot.filling.telemetry', 0, 18511, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-07-21T04:31:00Z", "value": 38.52, "uom": "Pa", "batchId": "A26-4410-0052", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-07-21 04:31:00.350000+00', '2026-07-21 04:31:02+00'),
('aus.ot.filling.telemetry', 0, 18550, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-07-21T06:31:00Z", "value": 44.73, "uom": "Pa", "batchId": "A26-4410-0052", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-07-21 06:31:00.350000+00', '2026-07-21 06:31:02+00'),
('aus.ot.filling.telemetry', 0, 18560, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-09-15T01:40:00Z", "value": 50.58, "uom": "g", "batchId": "A26-4630-0017", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-09-15 01:40:00.350000+00', '2026-09-15 01:40:02+00'),
('aus.ot.filling.telemetry', 0, 18575, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-09-15T03:35:00Z", "value": 50.66, "uom": "g", "batchId": "A26-4630-0017", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-09-15 03:35:00.350000+00', '2026-09-15 03:35:02+00'),
('aus.ot.filling.telemetry', 0, 18582, 'US10-FIL-01|FW401', '{"assetId": "US10-FIL-01", "signal": "FW401", "ts": "2026-09-15T05:30:00Z", "value": 50.79, "uom": "g", "batchId": "A26-4630-0017", "limits": {"lo": 50.2, "hi": 51.0}}', '2026-09-15 05:30:00.350000+00', '2026-09-15 05:30:02+00'),
('aus.ot.filling.telemetry', 0, 18592, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-09-15T01:40:00Z", "value": 52.2, "uom": "Pa", "batchId": "A26-4630-0017", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-09-15 01:40:00.350000+00', '2026-09-15 01:40:02+00'),
('aus.ot.filling.telemetry', 0, 18607, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-09-15T03:35:00Z", "value": 53.55, "uom": "Pa", "batchId": "A26-4630-0017", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-09-15 03:35:00.350000+00', '2026-09-15 03:35:02+00'),
('aus.ot.filling.telemetry', 0, 18614, 'US10-FIL-01|DP402', '{"assetId": "US10-FIL-01", "signal": "DP402", "ts": "2026-09-15T05:30:00Z", "value": 41.31, "uom": "Pa", "batchId": "A26-4630-0017", "limits": {"lo": 30.0, "hi": 60.0}}', '2026-09-15 05:30:00.350000+00', '2026-09-15 05:30:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20217, 'US10-INC-02|CO2501', '{"assetId": "US10-INC-02", "signal": "CO2501", "ts": "2026-09-02T05:30:00Z", "value": 5.18, "uom": "%", "batchId": "A26-7710-P017", "limits": {"lo": 4.5, "hi": 5.5}}', '2026-09-02 05:30:00.350000+00', '2026-09-02 05:30:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20231, 'US10-INC-02|CO2501', '{"assetId": "US10-INC-02", "signal": "CO2501", "ts": "2026-09-03T04:00:00Z", "value": 5.02, "uom": "%", "batchId": "A26-7710-P017", "limits": {"lo": 4.5, "hi": 5.5}}', '2026-09-03 04:00:00.350000+00', '2026-09-03 04:00:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20260, 'US10-INC-02|CO2501', '{"assetId": "US10-INC-02", "signal": "CO2501", "ts": "2026-09-04T02:30:00Z", "value": 4.91, "uom": "%", "batchId": "A26-7710-P017", "limits": {"lo": 4.5, "hi": 5.5}}', '2026-09-04 02:30:00.350000+00', '2026-09-04 02:30:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20283, 'US10-INC-02|TT502', '{"assetId": "US10-INC-02", "signal": "TT502", "ts": "2026-09-02T05:30:00Z", "value": 36.86, "uom": "degC", "batchId": "A26-7710-P017", "limits": {"lo": 36.5, "hi": 37.5}}', '2026-09-02 05:30:00.350000+00', '2026-09-02 05:30:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20297, 'US10-INC-02|TT502', '{"assetId": "US10-INC-02", "signal": "TT502", "ts": "2026-09-03T04:00:00Z", "value": 37.28, "uom": "degC", "batchId": "A26-7710-P017", "limits": {"lo": 36.5, "hi": 37.5}}', '2026-09-03 04:00:00.350000+00', '2026-09-03 04:00:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20326, 'US10-INC-02|TT502', '{"assetId": "US10-INC-02", "signal": "TT502", "ts": "2026-09-04T02:30:00Z", "value": 37.27, "uom": "degC", "batchId": "A26-7710-P017", "limits": {"lo": 36.5, "hi": 37.5}}', '2026-09-04 02:30:00.350000+00', '2026-09-04 02:30:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20358, 'US10-INC-02|CO2501', '{"assetId": "US10-INC-02", "signal": "CO2501", "ts": "2026-09-16T05:35:00Z", "value": 4.89, "uom": "%", "batchId": "A26-7710-P018", "limits": {"lo": 4.5, "hi": 5.5}}', '2026-09-16 05:35:00.350000+00', '2026-09-16 05:35:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20390, 'US10-INC-02|CO2501', '{"assetId": "US10-INC-02", "signal": "CO2501", "ts": "2026-09-17T04:10:00Z", "value": 5.28, "uom": "%", "batchId": "A26-7710-P018", "limits": {"lo": 4.5, "hi": 5.5}}', '2026-09-17 04:10:00.350000+00', '2026-09-17 04:10:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20429, 'US10-INC-02|CO2501', '{"assetId": "US10-INC-02", "signal": "CO2501", "ts": "2026-09-18T02:45:00Z", "value": 4.76, "uom": "%", "batchId": "A26-7710-P018", "limits": {"lo": 4.5, "hi": 5.5}}', '2026-09-18 02:45:00.350000+00', '2026-09-18 02:45:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20461, 'US10-INC-02|TT502', '{"assetId": "US10-INC-02", "signal": "TT502", "ts": "2026-09-16T05:35:00Z", "value": 36.93, "uom": "degC", "batchId": "A26-7710-P018", "limits": {"lo": 36.5, "hi": 37.5}}', '2026-09-16 05:35:00.350000+00', '2026-09-16 05:35:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20493, 'US10-INC-02|TT502', '{"assetId": "US10-INC-02", "signal": "TT502", "ts": "2026-09-17T04:10:00Z", "value": 37.07, "uom": "degC", "batchId": "A26-7710-P018", "limits": {"lo": 36.5, "hi": 37.5}}', '2026-09-17 04:10:00.350000+00', '2026-09-17 04:10:02+00'),
('aus.ot.cellsuite.telemetry', 2, 20532, 'US10-INC-02|TT502', '{"assetId": "US10-INC-02", "signal": "TT502", "ts": "2026-09-18T02:45:00Z", "value": 36.99, "uom": "degC", "batchId": "A26-7710-P018", "limits": {"lo": 36.5, "hi": 37.5}}', '2026-09-18 02:45:00.350000+00', '2026-09-18 02:45:02+00')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA apache_kafka TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA apache_kafka TO egeria_user, airflow_user;
