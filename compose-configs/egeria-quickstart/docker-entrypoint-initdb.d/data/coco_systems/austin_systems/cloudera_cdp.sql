-- system-qualified-name: SoftwareServer::AUS-SYS-001::CDH-AUS-7X-00142
-- Cloudera Data Platform (Primary Cluster) - Austin.  The Austin manufacturing data lake: five years of curated sensor
-- telemetry.  Readings older than the Historian's online archive (here January to July 2026) are only held here; its
-- curated telemetry table feeds Process Parameter Time Series.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS cloudera_cdp;
COMMENT ON SCHEMA cloudera_cdp IS 'Cloudera Data Platform primary cluster (Austin): Hive table mfg_curated.sensor_telemetry, partitioned by day.';

CREATE TABLE IF NOT EXISTS cloudera_cdp.sensor_telemetry (
  equipment_id varchar(40) NOT NULL,
  tag_name     varchar(40) NOT NULL,
  event_ts     bigint NOT NULL,
  reading      double precision NOT NULL,
  uom          varchar(20) NOT NULL,
  batch_id     varchar(40),
  spec_lo      double precision,
  spec_hi      double precision,
  dt           varchar(10) NOT NULL,
  CONSTRAINT sensor_telemetry_pk PRIMARY KEY (equipment_id, tag_name, event_ts)
);
COMMENT ON TABLE cloudera_cdp.sensor_telemetry IS 'Hive table mfg_curated.sensor_telemetry (event_ts = epoch milliseconds UTC; dt = partition column).';

INSERT INTO cloudera_cdp.sensor_telemetry (equipment_id, tag_name, event_ts, reading, uom, batch_id, spec_lo, spec_hi, dt) VALUES
('US10-CMX-01', 'TT601', 1776150000000, 21.03, 'degC', 'A26-4410-0041', 15.0, 25.0, '2026-04-14'),
('US10-CMX-01', 'TT601', 1776168000000, 20.01, 'degC', 'A26-4410-0041', 15.0, 25.0, '2026-04-14'),
('US10-CMX-01', 'TT601', 1776186000000, 19.53, 'degC', 'A26-4410-0041', 15.0, 25.0, '2026-04-14'),
('US10-CMX-01', 'TT601', 1776204000000, 19.08, 'degC', 'A26-4410-0041', 15.0, 25.0, '2026-04-14'),
('US10-CMX-01', 'TT601', 1776222000000, 18.87, 'degC', 'A26-4410-0041', 15.0, 25.0, '2026-04-15'),
('US10-CMX-01', 'TT601', 1776240000000, 18.48, 'degC', 'A26-4410-0041', 15.0, 25.0, '2026-04-15'),
('US10-CMX-01', 'TT601', 1779174000000, 17.37, 'degC', 'A26-4520-0023', 15.0, 25.0, '2026-05-19'),
('US10-CMX-01', 'TT601', 1779192000000, 22.68, 'degC', 'A26-4520-0023', 15.0, 25.0, '2026-05-19'),
('US10-CMX-01', 'TT601', 1779210000000, 17.85, 'degC', 'A26-4520-0023', 15.0, 25.0, '2026-05-19'),
('US10-CMX-01', 'TT601', 1779228000000, 20.49, 'degC', 'A26-4520-0023', 15.0, 25.0, '2026-05-19'),
('US10-CMX-01', 'TT601', 1779246000000, 22.23, 'degC', 'A26-4520-0023', 15.0, 25.0, '2026-05-20'),
('US10-CMX-01', 'TT601', 1779264000000, 20.85, 'degC', 'A26-4520-0023', 15.0, 25.0, '2026-05-20'),
('US10-INC-02', 'CO2501', 1773043200000, 4.95, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-09'),
('US10-INC-02', 'CO2501', 1773162000000, 4.97, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-10'),
('US10-INC-02', 'CO2501', 1773280800000, 4.84, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-12'),
('US10-INC-02', 'CO2501', 1773399600000, 4.82, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-13'),
('US10-INC-02', 'CO2501', 1773518400000, 4.83, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-14'),
('US10-INC-02', 'CO2501', 1773637200000, 5.13, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-16'),
('US10-INC-02', 'CO2501', 1773756000000, 5.1, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-17'),
('US10-INC-02', 'CO2501', 1773874800000, 4.99, '%', 'A26-7710-P009', 4.5, 5.5, '2026-03-18'),
('US10-INC-02', 'CO2501', 1777881600000, 5.25, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-04'),
('US10-INC-02', 'CO2501', 1778000400000, 4.79, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-05'),
('US10-INC-02', 'CO2501', 1778119200000, 4.85, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-07'),
('US10-INC-02', 'CO2501', 1778238000000, 5.25, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-08'),
('US10-INC-02', 'CO2501', 1778356800000, 5.07, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-09'),
('US10-INC-02', 'CO2501', 1778475600000, 4.76, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-11'),
('US10-INC-02', 'CO2501', 1778594400000, 4.94, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-12'),
('US10-INC-02', 'CO2501', 1778713200000, 5.01, '%', 'A26-7710-P011', 4.5, 5.5, '2026-05-13'),
('US10-INC-02', 'TT502', 1777881600000, 36.84, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-04'),
('US10-INC-02', 'TT502', 1778000400000, 37.29, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-05'),
('US10-INC-02', 'TT502', 1778119200000, 36.72, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-07'),
('US10-INC-02', 'TT502', 1778238000000, 37.1, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-08'),
('US10-INC-02', 'TT502', 1778356800000, 36.94, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-09'),
('US10-INC-02', 'TT502', 1778475600000, 37.25, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-11'),
('US10-INC-02', 'TT502', 1778594400000, 36.72, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-12'),
('US10-INC-02', 'TT502', 1778713200000, 37.21, 'degC', 'A26-7710-P011', 36.5, 37.5, '2026-05-13'),
('US10-CMX-01', 'TT601', 1784548800000, 17.01, 'degC', 'A26-4410-0052', 15.0, 25.0, '2026-07-20'),
('US10-CMX-01', 'TT601', 1784560800000, 22.5, 'degC', 'A26-4410-0052', 15.0, 25.0, '2026-07-20'),
('US10-CMX-01', 'TT601', 1784572800000, 21.21, 'degC', 'A26-4410-0052', 15.0, 25.0, '2026-07-20'),
('US10-CMX-01', 'TT601', 1784584800000, 21.24, 'degC', 'A26-4410-0052', 15.0, 25.0, '2026-07-20'),
('US10-CMX-01', 'TT601', 1784596800000, 19.77, 'degC', 'A26-4410-0052', 15.0, 25.0, '2026-07-21'),
('US10-CMX-01', 'TT601', 1784608800000, 20.1, 'degC', 'A26-4410-0052', 15.0, 25.0, '2026-07-21')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA cloudera_cdp TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA cloudera_cdp TO egeria_user, airflow_user;
