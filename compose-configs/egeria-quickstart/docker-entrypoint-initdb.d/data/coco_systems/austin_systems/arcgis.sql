-- system-qualified-name: SoftwareServer::AUS-SYS-044::SN-GIS-AU-20230601
-- Esri ArcGIS Enterprise - Austin.  ArcGIS Enterprise for Austin cold-chain logistics: the hosted feature layer of
-- courier GPS/temperature fixes for patient therapy shipments.  Its layer table feeds Therapy Delivery Events (in-
-- transit positions).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS arcgis;
COMMENT ON SCHEMA arcgis IS 'Esri ArcGIS Enterprise (Austin): enterprise geodatabase table of the therapy_shipment_track_pts feature class (geometry as lat/lon).';

CREATE TABLE IF NOT EXISTS arcgis.therapy_shipment_track_pts (
  objectid      integer NOT NULL,
  globalid      uuid NOT NULL,
  shipment_id   varchar(40) NOT NULL,
  order_no      varchar(40),
  batch_no      varchar(40),
  patient_ref   varchar(40),
  fix_time      timestamptz NOT NULL,
  place_name    varchar(120),
  latitude      double precision NOT NULL,
  longitude     double precision NOT NULL,
  logger_temp_c double precision,
  created_user  varchar(40),
  created_date  timestamptz,
  CONSTRAINT therapy_shipment_track_pts_pk PRIMARY KEY (objectid)
);
COMMENT ON TABLE arcgis.therapy_shipment_track_pts IS 'Courier tracker fixes for therapy shipments (attributes joined from TMS on ingest; logger temperature from the dry shipper).';

INSERT INTO arcgis.therapy_shipment_track_pts (objectid, globalid, shipment_id, order_no, batch_no, patient_ref, fix_time, place_name, latitude, longitude, logger_temp_c, created_user, created_date) VALUES
(1201, 'ba1cceb2-e092-28a2-9dbe-bb45ae3301e7', 'SH-26-TX0015', 'TO-26-0015', 'A26-7710-P015', 'PP-FA1AF588F5B4', '2026-07-28 20:56:15+00', 'Bastrop, TX', 30.11, -97.32, -188.0, 'lscc_tracker', '2026-07-28 20:56:55+00'),
(1202, 'bd2f17bd-f6de-2ac9-7640-15c8c3589c1b', 'SH-26-TX0015', 'TO-26-0015', 'A26-7710-P015', 'PP-FA1AF588F5B4', '2026-07-29 01:22:30+00', 'Columbus, TX', 29.71, -96.54, -186.3, 'lscc_tracker', '2026-07-29 01:23:10+00'),
(1203, 'b893332f-cd10-09e5-bca2-63396ee1737d', 'SH-26-TX0015', 'TO-26-0015', 'A26-7710-P015', 'PP-FA1AF588F5B4', '2026-07-29 05:48:45+00', 'Katy, TX', 29.79, -95.82, -185.9, 'lscc_tracker', '2026-07-29 05:49:25+00'),
(1204, '3049ff2f-c636-deb0-4546-d5fe8b9517ae', 'SH-26-TX0016', 'TO-26-0016', 'A26-7710-P016', 'PP-CCD4B098EAFF', '2026-08-25 15:10:00+00', 'Austin, TX (I-35 at Riverside)', 30.24, -97.73, -187.0, 'lscc_tracker', '2026-08-25 15:10:40+00'),
(1205, '79ee9b56-fe28-b96a-3e9e-9a2f3fb3073e', 'SH-26-TX0017', 'TO-26-0017', 'A26-7710-P017', 'PP-08BA47CBA05B', '2026-09-15 19:41:15+00', 'Bastrop, TX', 30.11, -97.32, -187.3, 'lscc_tracker', '2026-09-15 19:41:55+00'),
(1206, '07fd521b-752c-07a2-cc5f-43b637b4b52b', 'SH-26-TX0017', 'TO-26-0017', 'A26-7710-P017', 'PP-08BA47CBA05B', '2026-09-16 00:22:30+00', 'Columbus, TX', 29.71, -96.54, -185.5, 'lscc_tracker', '2026-09-16 00:23:10+00'),
(1207, 'e58c56c7-1674-7485-17b4-58741efd1f19', 'SH-26-TX0017', 'TO-26-0017', 'A26-7710-P017', 'PP-08BA47CBA05B', '2026-09-16 05:03:45+00', 'Katy, TX', 29.79, -95.82, -184.4, 'lscc_tracker', '2026-09-16 05:04:25+00')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/arcgis).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS arcgis.therapy_release (
  batch_no        varchar(40) NOT NULL,
  market          varchar(8) NOT NULL,
  release_status  varchar(20) NOT NULL,
  release_date    date NOT NULL,
  released_qty    integer,
  record_complete boolean NOT NULL,
  deviation_ref   varchar(40),
  storage_text    text,
  CONSTRAINT therapy_release_pk PRIMARY KEY (batch_no, market)
);
COMMENT ON TABLE arcgis.therapy_release IS 'Hosted table of patient therapy batch release decisions joined to the track layer, from Batch Certification Decisions.';

GRANT USAGE ON SCHEMA arcgis TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA arcgis TO egeria_user, airflow_user;
