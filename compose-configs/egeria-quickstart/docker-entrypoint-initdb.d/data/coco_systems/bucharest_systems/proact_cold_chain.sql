-- system-qualified-name: SoftwareServer::SYS-022::Proact Cold Chain Monitor
-- Proact Cold Chain Monitor - Bucharest.  Proact IoT temperature monitoring: fixed sensors in the cold room and
-- freezers, and (since a July 2026 pilot) loggers and 4G live monitors travelling with cold chain despatches, with
-- their trips, trip events and alarms.  Its tables feed In-Transit Temperature Readings, Cold Chain Transit Records
-- (excursion detection) and Carrier Transit Events (tracked trip events).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS proact_cold_chain;
COMMENT ON SCHEMA proact_cold_chain IS 'Proact Cold Chain Monitor 3.4 (EKG): device registry, MQTT measurements, trips, trip events and alarms as stored by the Proact server (UTC).';

CREATE TABLE IF NOT EXISTS proact_cold_chain.device (
  device_id    varchar(20) NOT NULL,
  serial_no    varchar(20) NOT NULL,
  model        varchar(40) NOT NULL,
  device_class varchar(10) NOT NULL,
  battery      varchar(40),
  fixed_asset  varchar(20),
  status       varchar(10) NOT NULL,
  CONSTRAINT device_pk PRIMARY KEY (device_id)
);
COMMENT ON TABLE proact_cold_chain.device IS 'Registered devices (loggers and live monitors are lithium-battery powered and travel as UN3481 equipment).';

INSERT INTO proact_cold_chain.device (device_id, serial_no, model, device_class, battery, fixed_asset, status) VALUES
('PCM-T20-00417', 'T20-00417', 'Proact T20 logger', 'LOGGER', 'Li-SOCl2 3,6 V', NULL, 'ACTIVE'),
('PCM-T20-00422', 'T20-00422', 'Proact T20 logger', 'LOGGER', 'Li-SOCl2 3,6 V', NULL, 'ACTIVE'),
('PCM-L4G-00031', 'L4G-00031', 'Proact Live 4G/GPS', 'LIVE', 'Li-ion 3,7 V 5200 mAh', NULL, 'ACTIVE'),
('PCM-L4G-00034', 'L4G-00034', 'Proact Live 4G/GPS', 'LIVE', 'Li-ion 3,7 V 5200 mAh', NULL, 'ACTIVE'),
('PCM-FX-00101', 'FX-00101', 'Proact FX fixed sensor', 'FIXED', 'Rețea 230 V', 'RO10-CRF-01', 'ACTIVE'),
('PCM-FX-00102', 'FX-00102', 'Proact FX fixed sensor', 'FIXED', 'Rețea 230 V', 'RO10-FRZ-01', 'ACTIVE')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS proact_cold_chain.trip (
  trip_id      varchar(20) NOT NULL,
  shipment_ref varchar(40) NOT NULL,
  device_id    varchar(20) NOT NULL,
  carrier_ref  varchar(10) NOT NULL,
  carrier_name varchar(120),
  started_at   timestamptz NOT NULL,
  ended_at     timestamptz,
  status       varchar(10) NOT NULL,
  CONSTRAINT trip_pk PRIMARY KEY (trip_id)
);
COMMENT ON TABLE proact_cold_chain.trip IS 'Trips: a device assigned to a despatch (shipment_ref = WMS despatch number; carrier_ref = SAP vendor number, typed in by logistics).';

INSERT INTO proact_cold_chain.trip (trip_id, shipment_ref, device_id, carrier_ref, carrier_name, started_at, ended_at, status) VALUES
('TRP-2603', 'EXP-26-0391', 'PCM-T20-00417', '700250', 'Urgent Medical Curier', '2026-07-17 08:30:00+00', '2026-07-17 11:05:00+00', 'CLOSED'),
('TRP-2606', 'EXP-26-0396', 'PCM-T20-00422', '700220', 'Carpatica Logistic Frig', '2026-07-27 07:00:00+00', '2026-07-27 10:40:00+00', 'CLOSED'),
('TRP-2609', 'EXP-26-0403', 'PCM-T20-00417', '700250', 'Urgent Medical Curier', '2026-08-07 08:15:00+00', '2026-08-07 10:50:00+00', 'CLOSED'),
('TRP-2612', 'EXP-26-0407', 'PCM-L4G-00031', '700220', 'Carpatica Logistic Frig', '2026-08-12 05:30:00+00', '2026-08-13 14:20:00+00', 'CLOSED'),
('TRP-2615', 'EXP-26-0409', 'PCM-T20-00422', '700220', 'Carpatica Logistic Frig', '2026-08-24 07:10:00+00', '2026-08-24 09:55:00+00', 'CLOSED'),
('TRP-2618', 'EXP-26-0411', 'PCM-L4G-00034', '700250', 'Urgent Medical Curier', '2026-08-28 07:40:00+00', '2026-08-28 17:25:00+00', 'CLOSED'),
('TRP-2621', 'EXP-26-0418', 'PCM-L4G-00031', '700220', 'Carpatica Logistic Frig', '2026-09-15 05:30:00+00', '2026-09-16 16:10:00+00', 'CLOSED'),
('TRP-2624', 'EXP-26-0420', 'PCM-L4G-00034', '700250', 'Urgent Medical Curier', '2026-09-18 07:30:00+00', '2026-09-18 18:40:00+00', 'CLOSED')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS proact_cold_chain.measurement (
  device_id      varchar(20) NOT NULL,
  measured_at    timestamptz NOT NULL,
  temp_c         numeric(6,1) NOT NULL,
  rh_pct         numeric(5,1),
  location_label varchar(120),
  trip_id        varchar(20),
  CONSTRAINT measurement_pk PRIMARY KEY (device_id, measured_at)
);
COMMENT ON TABLE proact_cold_chain.measurement IS 'Measurements (trip_id null = fixed sensor or unassigned logger; location only from live GPS monitors).';

INSERT INTO proact_cold_chain.measurement (device_id, measured_at, temp_c, rh_pct, location_label, trip_id) VALUES
('PCM-T20-00417', '2026-07-17 08:30:00+00', -68.9, NULL, NULL, 'TRP-2603'),
('PCM-T20-00417', '2026-07-17 09:21:00+00', -68.3, NULL, NULL, 'TRP-2603'),
('PCM-T20-00417', '2026-07-17 10:13:00+00', -69.3, NULL, NULL, 'TRP-2603'),
('PCM-T20-00417', '2026-07-17 11:05:00+00', -67.5, NULL, NULL, 'TRP-2603'),
('PCM-T20-00422', '2026-07-27 07:00:00+00', 6.1, 55, NULL, 'TRP-2606'),
('PCM-T20-00422', '2026-07-27 08:13:00+00', 4.3, 54, NULL, 'TRP-2606'),
('PCM-T20-00422', '2026-07-27 09:26:00+00', 6.9, 50, NULL, 'TRP-2606'),
('PCM-T20-00422', '2026-07-27 10:40:00+00', 4.3, 46, NULL, 'TRP-2606'),
('PCM-T20-00417', '2026-08-07 08:15:00+00', -69.9, NULL, NULL, 'TRP-2609'),
('PCM-T20-00417', '2026-08-07 09:06:00+00', -66.2, NULL, NULL, 'TRP-2609'),
('PCM-T20-00417', '2026-08-07 09:58:00+00', -67.2, NULL, NULL, 'TRP-2609'),
('PCM-T20-00417', '2026-08-07 10:50:00+00', -69.6, NULL, NULL, 'TRP-2609'),
('PCM-L4G-00031', '2026-08-12 05:30:00+00', 3.3, 43, 'București, rampa EKG', 'TRP-2612'),
('PCM-L4G-00031', '2026-08-12 12:04:00+00', 4.0, 40, 'A2 Autostrada Soarelui', 'TRP-2612'),
('PCM-L4G-00031', '2026-08-12 18:38:00+00', 5.4, 41, 'Focșani, DN2', 'TRP-2612'),
('PCM-L4G-00031', '2026-08-13 01:12:00+00', 4.0, 40, 'Vama Albița (RO-MD)', 'TRP-2612'),
('PCM-L4G-00031', '2026-08-13 07:46:00+00', 5.0, 58, 'Hîncești, R1', 'TRP-2612'),
('PCM-L4G-00031', '2026-08-13 14:20:00+00', 4.3, 54, 'Chișinău, depozit Moldfarm', 'TRP-2612'),
('PCM-T20-00422', '2026-08-24 07:10:00+00', 5.4, 57, NULL, 'TRP-2615'),
('PCM-T20-00422', '2026-08-24 08:05:00+00', 5.4, 47, NULL, 'TRP-2615'),
('PCM-T20-00422', '2026-08-24 09:00:00+00', 5.2, 42, NULL, 'TRP-2615'),
('PCM-T20-00422', '2026-08-24 09:55:00+00', 4.8, 55, NULL, 'TRP-2615'),
('PCM-L4G-00034', '2026-08-28 07:40:00+00', -69.7, NULL, 'București, rampa EKG', 'TRP-2618'),
('PCM-L4G-00034', '2026-08-28 09:37:00+00', -68.9, NULL, 'DN7 Valea Oltului', 'TRP-2618'),
('PCM-L4G-00034', '2026-08-28 11:34:00+00', -67.7, NULL, 'Sibiu, A1', 'TRP-2618'),
('PCM-L4G-00034', '2026-08-28 13:31:00+00', -67.7, NULL, 'Alba Iulia, A1', 'TRP-2618'),
('PCM-L4G-00034', '2026-08-28 15:28:00+00', -67.4, NULL, 'Cluj-Napoca, Spitalul Clinic Județean', 'TRP-2618'),
('PCM-L4G-00034', '2026-08-28 17:25:00+00', -69.1, NULL, 'Cluj-Napoca, Spitalul Clinic Județean', 'TRP-2618'),
('PCM-L4G-00031', '2026-09-15 05:30:00+00', 5.8, 54, 'București, rampa EKG', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-15 12:26:00+00', 4.4, 42, 'A2 Autostrada Soarelui', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-15 19:22:00+00', 3.1, 44, 'Focșani, DN2', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-16 02:18:00+00', 4.1, 48, 'Vama Albița (RO-MD)', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-16 07:15:00+00', 8.6, 47, 'Vama Albița (RO-MD)', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-16 07:40:00+00', 9.4, 49, 'Vama Albița (RO-MD)', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-16 09:14:00+00', 3.6, 58, 'Hîncești, R1', 'TRP-2621'),
('PCM-L4G-00031', '2026-09-16 16:10:00+00', 6.9, 42, 'Chișinău, depozit Moldfarm', 'TRP-2621'),
('PCM-L4G-00034', '2026-09-18 07:30:00+00', -69.7, NULL, 'București, rampa EKG', 'TRP-2624'),
('PCM-L4G-00034', '2026-09-18 09:44:00+00', -68.2, NULL, 'DN2 Urziceni', 'TRP-2624'),
('PCM-L4G-00034', '2026-09-18 11:58:00+00', -69.3, NULL, 'Buzău, E85', 'TRP-2624'),
('PCM-L4G-00034', '2026-09-18 14:12:00+00', -66.4, NULL, 'Bacău, E85', 'TRP-2624'),
('PCM-L4G-00034', '2026-09-18 16:26:00+00', -67.5, NULL, 'Iași, Spitalul Sf. Spiridon', 'TRP-2624'),
('PCM-L4G-00034', '2026-09-18 18:40:00+00', -66.7, NULL, 'Iași, Spitalul Sf. Spiridon', 'TRP-2624'),
('PCM-FX-00101', '2026-09-29 00:00:00+00', 4.8, 55.0, 'Cameră frigorifică RO10-CRF-01', NULL),
('PCM-FX-00101', '2026-09-29 04:00:00+00', 5.0, 55.0, 'Cameră frigorifică RO10-CRF-01', NULL),
('PCM-FX-00101', '2026-09-29 08:00:00+00', 5.0, 55.0, 'Cameră frigorifică RO10-CRF-01', NULL),
('PCM-FX-00101', '2026-09-29 12:00:00+00', 4.8, 55.0, 'Cameră frigorifică RO10-CRF-01', NULL),
('PCM-FX-00101', '2026-09-29 16:00:00+00', 5.1, 55.0, 'Cameră frigorifică RO10-CRF-01', NULL),
('PCM-FX-00101', '2026-09-29 20:00:00+00', 5.3, 55.0, 'Cameră frigorifică RO10-CRF-01', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS proact_cold_chain.trip_event (
  event_id       varchar(24) NOT NULL,
  trip_id        varchar(20) NOT NULL,
  event_code     varchar(20) NOT NULL,
  event_at       timestamptz NOT NULL,
  location_label varchar(120),
  message        text,
  CONSTRAINT trip_event_pk PRIMARY KEY (event_id)
);
COMMENT ON TABLE proact_cold_chain.trip_event IS 'Trip events (geofence departure/arrival, delay, signal loss, logger start/stop).';

INSERT INTO proact_cold_chain.trip_event (event_id, trip_id, event_code, event_at, location_label, message) VALUES
('TRP-2603-E1', 'TRP-2603', 'LOGGER_STARTED', '2026-07-17 08:20:00+00', 'București, rampa EKG', NULL),
('TRP-2603-E9', 'TRP-2603', 'LOGGER_STOPPED', '2026-07-17 11:10:00+00', NULL, 'Descărcat la destinație'),
('TRP-2606-E1', 'TRP-2606', 'LOGGER_STARTED', '2026-07-27 06:50:00+00', 'București, rampa EKG', NULL),
('TRP-2606-E9', 'TRP-2606', 'LOGGER_STOPPED', '2026-07-27 10:45:00+00', NULL, 'Descărcat la destinație'),
('TRP-2609-E1', 'TRP-2609', 'LOGGER_STARTED', '2026-08-07 08:05:00+00', 'București, rampa EKG', NULL),
('TRP-2609-E9', 'TRP-2609', 'LOGGER_STOPPED', '2026-08-07 10:55:00+00', NULL, 'Descărcat la destinație'),
('TRP-2612-E1', 'TRP-2612', 'DEPARTED', '2026-08-12 05:34:00+00', 'București, rampa EKG', NULL),
('TRP-2612-E9', 'TRP-2612', 'ARRIVED', '2026-08-13 14:17:00+00', 'Chișinău, depozit Moldfarm', NULL),
('TRP-2615-E1', 'TRP-2615', 'LOGGER_STARTED', '2026-08-24 07:00:00+00', 'București, rampa EKG', NULL),
('TRP-2615-E9', 'TRP-2615', 'LOGGER_STOPPED', '2026-08-24 10:00:00+00', NULL, 'Descărcat la destinație'),
('TRP-2618-E1', 'TRP-2618', 'DEPARTED', '2026-08-28 07:44:00+00', 'București, rampa EKG', NULL),
('TRP-2618-E9', 'TRP-2618', 'ARRIVED', '2026-08-28 17:22:00+00', 'Cluj-Napoca, Spitalul Clinic Județean', NULL),
('TRP-2618-E4', 'TRP-2618', 'SIGNAL_LOST', '2026-08-28 09:05:00+00', 'DN7 Valea Oltului', 'Pierdere semnal 4G 26 min; înregistrările nu au fost stocate local'),
('TRP-2621-E1', 'TRP-2621', 'DEPARTED', '2026-09-15 05:34:00+00', 'București, rampa EKG', NULL),
('TRP-2621-E9', 'TRP-2621', 'ARRIVED', '2026-09-16 16:07:00+00', 'Chișinău, depozit Moldfarm', NULL),
('TRP-2621-E5', 'TRP-2621', 'DELAYED', '2026-09-16 06:40:00+00', 'Vama Albița (RO-MD)', 'Staționare > 45 min la frontieră (coadă control vamal)'),
('TRP-2624-E1', 'TRP-2624', 'DEPARTED', '2026-09-18 07:34:00+00', 'București, rampa EKG', NULL),
('TRP-2624-E9', 'TRP-2624', 'ARRIVED', '2026-09-18 18:37:00+00', 'Iași, Spitalul Sf. Spiridon', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS proact_cold_chain.alarm (
  alarm_id        varchar(20) NOT NULL,
  device_id       varchar(20) NOT NULL,
  trip_id         varchar(20),
  alarm_type      varchar(20) NOT NULL,
  started_at      timestamptz NOT NULL,
  ended_at        timestamptz,
  peak_value      numeric(6,1),
  acknowledged_by varchar(20),
  CONSTRAINT alarm_pk PRIMARY KEY (alarm_id)
);
COMMENT ON TABLE proact_cold_chain.alarm IS 'Alarms (TEMP_HIGH, TEMP_LOW, SIGNAL_LOST); acknowledged_by = AD login.';

INSERT INTO proact_cold_chain.alarm (alarm_id, device_id, trip_id, alarm_type, started_at, ended_at, peak_value, acknowledged_by) VALUES
('ALM-26-00212', 'PCM-L4G-00034', 'TRP-2618', 'SIGNAL_LOST', '2026-08-28 09:05:00+00', '2026-08-28 09:31:00+00', -66.8, 'renache'),
('ALM-26-00237', 'PCM-L4G-00031', 'TRP-2621', 'TEMP_HIGH', '2026-09-16 07:02:00+00', '2026-09-16 07:52:00+00', 9.4, 'renache'),
('ALM-26-00241', 'PCM-FX-00101', NULL, 'TEMP_HIGH', '2026-09-22 13:10:00+00', '2026-09-22 13:24:00+00', 8.7, 'dilie')
ON CONFLICT DO NOTHING;

-- Shipment data received from EKG's other systems (subscription apply scripts buc_proact_cold_chain__*).
CREATE TABLE IF NOT EXISTS proact_cold_chain.shipment_manifest (
  shipment_ref      varchar(40) NOT NULL,
  direction         varchar(10) NOT NULL,
  carrier_ref       varchar(10),
  dispatch_date     date,
  ship_to           text,
  un_number         varchar(20),
  dg_quantity       numeric(12,3),
  dg_unit           varchar(20),
  order_ref         varchar(40),
  patient_ref       varchar(40),
  viable_hours      integer,
  updated_at        timestamptz NOT NULL,
  CONSTRAINT shipment_manifest_pk PRIMARY KEY (shipment_ref)
);
COMMENT ON TABLE proact_cold_chain.shipment_manifest IS 'Shipment manifest: what a trip carries (outbound despatch with its dry-ice UN number, or inbound patient material with its viability window), used to set up the trip and its alarm profile.';

CREATE TABLE IF NOT EXISTS proact_cold_chain.partner_event (
  shipment_ref      varchar(40) NOT NULL,
  event_code        varchar(30) NOT NULL,
  event_at          timestamptz NOT NULL,
  carrier_ref       varchar(10),
  location_label    varchar(120),
  message           text,
  source            varchar(20) NOT NULL,
  CONSTRAINT partner_event_pk PRIMARY KEY (shipment_ref, event_code, event_at)
);
COMMENT ON TABLE proact_cold_chain.partner_event IS 'Custody events reported by partner systems (handover to carrier, proof of delivery) shown on the trip timeline alongside the monitor''s own trip_event rows.';

GRANT USAGE ON SCHEMA proact_cold_chain TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA proact_cold_chain TO egeria_user, airflow_user;
