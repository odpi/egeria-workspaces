-- system-qualified-name: SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004
-- Oracle TMS - Austin.  Oracle Transportation Management for Austin outbound freight and patient therapy courier
-- shipments: shipments with reference numbers, dangerous goods declaration attributes and tracking events.  Its tables
-- feed Therapy Delivery Events and Dangerous Goods Consignment Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS oracle_tms;
COMMENT ON SCHEMA oracle_tms IS 'Oracle Transportation Management (domain AUS): location, shipment, shipment_refnum and ie_shipmentstatus.';

CREATE TABLE IF NOT EXISTS oracle_tms.location (
  location_gid      varchar(101) NOT NULL,
  location_xid      varchar(50) NOT NULL,
  location_name     varchar(120) NOT NULL,
  address_line1     varchar(120),
  city              varchar(60),
  province_code     varchar(10),
  postal_code       varchar(15),
  country_code3_gid varchar(3) NOT NULL,
  CONSTRAINT location_pk PRIMARY KEY (location_gid)
);
COMMENT ON TABLE oracle_tms.location IS 'Ship-from and ship-to locations.';

INSERT INTO oracle_tms.location (location_gid, location_xid, location_name, address_line1, city, province_code, postal_code, country_code3_gid) VALUES
('AUS.US10_PLANT', 'US10_PLANT', 'Austin Pharmaceuticals - Austin Plant', '9200 Research Blvd', 'Austin', 'TX', '78758', 'USA'),
('AUS.US20_DC', 'US20_DC', 'Austin Pharmaceuticals - Distribution Center', '2400 Greenlawn Blvd', 'Round Rock', 'TX', '78664', 'USA'),
('AUS.C200010', 'C200010', 'McKesson DC Fort Worth', '4200 Mark IV Pkwy', 'Fort Worth', 'TX', '76106', 'USA'),
('AUS.C200020', 'C200020', 'Cardinal Health DC Houston', '9005 Fairbanks N Houston Rd', 'Houston', 'TX', '77064', 'USA'),
('AUS.C200030', 'C200030', 'Cencora DC Carrollton', '1085 N Stemmons Fwy', 'Carrollton', 'TX', '75006', 'USA'),
('AUS.C200080', 'C200080', 'McKesson Canada DC Mississauga', '6355 Viscount Rd', 'Mississauga', 'ON', 'L4V 1W2', 'CAN'),
('AUS.C200040', 'C200040', 'MD Anderson Cell Therapy Lab', '1515 Holcombe Blvd', 'Houston', 'TX', '77030', 'USA'),
('AUS.C200050', 'C200050', 'BSW Temple Cellular Therapy', '2401 S 31st St', 'Temple', 'TX', '76508', 'USA'),
('AUS.C200060', 'C200060', 'UTSW Cellular Therapy Lab', '5323 Harry Hines Blvd', 'Dallas', 'TX', '75390', 'USA'),
('AUS.C200070', 'C200070', 'Dell Seton Infusion Center', '1500 Red River St', 'Austin', 'TX', '78701', 'USA')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_tms.shipment (
  shipment_gid              varchar(101) NOT NULL,
  shipment_xid              varchar(50) NOT NULL,
  servprov_gid              varchar(101) NOT NULL,
  source_location_gid       varchar(101) NOT NULL,
  dest_location_gid         varchar(101) NOT NULL,
  start_time                timestamptz NOT NULL,
  end_time                  timestamptz,
  total_weight              numeric(12,2),
  total_weight_uom_code     varchar(10),
  total_net_volume          numeric(12,3),
  total_net_volume_uom_code varchar(10),
  transport_mode_gid        varchar(20),
  attribute1                varchar(50),
  attribute2                varchar(50),
  attribute_date1           timestamptz,
  CONSTRAINT shipment_pk PRIMARY KEY (shipment_gid)
);
COMMENT ON TABLE oracle_tms.shipment IS 'Shipments; attribute1/attribute2/attribute_date1 hold the dangerous goods declaration signatory, their hazmat training certificate and the signing time.';

INSERT INTO oracle_tms.shipment (shipment_gid, shipment_xid, servprov_gid, source_location_gid, dest_location_gid, start_time, end_time, total_weight, total_weight_uom_code, total_net_volume, total_net_volume_uom_code, transport_mode_gid, attribute1, attribute2, attribute_date1) VALUES
('AUS.SH-26-00412', 'SH-26-00412', 'AUS.FEDEX_FREIGHT', 'AUS.US20_DC', 'AUS.C200010', '2026-08-06 14:00:00+00', '2026-08-07 18:00:00+00', 165.0, 'KG', 67.5, 'L', 'LTL', 'sadeyemi', 'CERT-DGR-300-260301', '2026-08-06 11:45:00+00'),
('AUS.SH-26-00428', 'SH-26-00428', 'AUS.FEDEX_FREIGHT', 'AUS.US20_DC', 'AUS.C200010', '2026-08-20 13:30:00+00', '2026-08-21 17:30:00+00', 252.0, 'KG', NULL, NULL, 'LTL', NULL, NULL, NULL),
('AUS.SH-26-00433', 'SH-26-00433', 'AUS.UPS_HEALTHCARE', 'AUS.US20_DC', 'AUS.C200020', '2026-08-27 15:10:00+00', '2026-08-28 19:10:00+00', 504.0, 'KG', NULL, NULL, 'LTL', NULL, NULL, NULL),
('AUS.SH-26-00447', 'SH-26-00447', 'AUS.FEDEX_FREIGHT', 'AUS.US20_DC', 'AUS.C200030', '2026-09-15 12:45:00+00', '2026-09-16 16:45:00+00', 88.0, 'KG', 40.0, 'L', 'LTL', 'sadeyemi', 'CERT-DGR-300-260301', '2026-09-15 10:30:00+00'),
('AUS.SH-26-00451', 'SH-26-00451', 'AUS.UPS_HEALTHCARE', 'AUS.US20_DC', 'AUS.C200080', '2026-09-18 11:20:00+00', '2026-09-19 15:20:00+00', 71.5, 'KG', 32.5, 'L', 'LTL', 'sadeyemi', 'CERT-DGR-300-260301', '2026-09-18 09:05:00+00'),
('AUS.SH-26-00458', 'SH-26-00458', 'AUS.UPS_HEALTHCARE', 'AUS.US20_DC', 'AUS.C200040', '2026-09-24 09:40:00+00', '2026-09-25 13:40:00+00', 44.0, 'KG', 4.0, 'L', 'LTL', 'sadeyemi', 'CERT-DGR-300-260301', '2026-09-24 07:25:00+00'),
('AUS.SH-26-TX0015', 'SH-26-TX0015', 'AUS.LIFELINE_BIO', 'AUS.US10_PLANT', 'AUS.C200040', '2026-07-28 16:30:00+00', '2026-07-29 10:15:00+00', 18.5, 'KG', NULL, NULL, 'COURIER', NULL, NULL, NULL),
('AUS.SH-26-TX0016', 'SH-26-TX0016', 'AUS.LSCCC', 'AUS.US10_PLANT', 'AUS.C200070', '2026-08-25 13:00:00+00', '2026-08-25 17:20:00+00', 18.5, 'KG', NULL, NULL, 'COURIER', NULL, NULL, NULL),
('AUS.SH-26-TX0017', 'SH-26-TX0017', 'AUS.LSCCC', 'AUS.US10_PLANT', 'AUS.C200040', '2026-09-15 15:00:00+00', '2026-09-16 09:45:00+00', 18.5, 'KG', NULL, NULL, 'COURIER', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_tms.shipment_refnum (
  shipment_gid             varchar(101) NOT NULL,
  shipment_refnum_qual_gid varchar(101) NOT NULL,
  shipment_refnum_value    varchar(240) NOT NULL,
  CONSTRAINT shipment_refnum_pk PRIMARY KEY (shipment_gid, shipment_refnum_qual_gid, shipment_refnum_value)
);
COMMENT ON TABLE oracle_tms.shipment_refnum IS 'Shipment reference numbers (order, batch, patient, UN number, BOL, storage).';

INSERT INTO oracle_tms.shipment_refnum (shipment_gid, shipment_refnum_qual_gid, shipment_refnum_value) VALUES
('AUS.SH-26-00412', 'AUS.BATCH_NO', 'A26-4410-0052'),
('AUS.SH-26-00412', 'AUS.BOL', 'BOL-26-00412'),
('AUS.SH-26-00412', 'AUS.UN_NUMBER', 'UN1851'),
('AUS.SH-26-00428', 'AUS.BATCH_NO', 'A26-3000-0141'),
('AUS.SH-26-00428', 'AUS.BOL', 'BOL-26-00428'),
('AUS.SH-26-00433', 'AUS.BATCH_NO', 'A26-2050-0087'),
('AUS.SH-26-00433', 'AUS.BOL', 'BOL-26-00433'),
('AUS.SH-26-00447', 'AUS.BATCH_NO', 'A26-9000-0019'),
('AUS.SH-26-00447', 'AUS.BOL', 'BOL-26-00447'),
('AUS.SH-26-00447', 'AUS.UN_NUMBER', 'UN1851'),
('AUS.SH-26-00451', 'AUS.BATCH_NO', 'A26-9000-0019'),
('AUS.SH-26-00451', 'AUS.BOL', 'BOL-26-00451'),
('AUS.SH-26-00451', 'AUS.UN_NUMBER', 'UN1851'),
('AUS.SH-26-00458', 'AUS.BATCH_NO', 'A26-4630-0017'),
('AUS.SH-26-00458', 'AUS.BOL', 'BOL-26-00458'),
('AUS.SH-26-00458', 'AUS.UN_NUMBER', 'UN1851'),
('AUS.SH-26-TX0015', 'AUS.ORDER_NO', 'TO-26-0015'),
('AUS.SH-26-TX0015', 'AUS.BATCH_NO', 'A26-7710-P015'),
('AUS.SH-26-TX0015', 'AUS.PATIENT_REF', 'PP-FA1AF588F5B4'),
('AUS.SH-26-TX0015', 'AUS.CLINICIAN_NPI', '1487621930'),
('AUS.SH-26-TX0015', 'AUS.STORAGE', 'LN2 vapour-phase dry shipper, at or below -150 C; do not X-ray'),
('AUS.SH-26-TX0016', 'AUS.ORDER_NO', 'TO-26-0016'),
('AUS.SH-26-TX0016', 'AUS.BATCH_NO', 'A26-7710-P016'),
('AUS.SH-26-TX0016', 'AUS.PATIENT_REF', 'PP-CCD4B098EAFF'),
('AUS.SH-26-TX0016', 'AUS.CLINICIAN_NPI', '1609273354'),
('AUS.SH-26-TX0016', 'AUS.STORAGE', 'LN2 vapour-phase dry shipper, at or below -150 C; do not X-ray'),
('AUS.SH-26-TX0017', 'AUS.ORDER_NO', 'TO-26-0017'),
('AUS.SH-26-TX0017', 'AUS.BATCH_NO', 'A26-7710-P017'),
('AUS.SH-26-TX0017', 'AUS.PATIENT_REF', 'PP-08BA47CBA05B'),
('AUS.SH-26-TX0017', 'AUS.CLINICIAN_NPI', '1932045718'),
('AUS.SH-26-TX0017', 'AUS.STORAGE', 'LN2 vapour-phase dry shipper, at or below -150 C; do not X-ray')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_tms.ie_shipmentstatus (
  i_transaction_no    bigint NOT NULL,
  shipment_gid        varchar(101) NOT NULL,
  status_code_gid     varchar(101) NOT NULL,
  event_date          timestamptz NOT NULL,
  status_location_gid varchar(101),
  ss_remark           varchar(240),
  CONSTRAINT ie_shipmentstatus_pk PRIMARY KEY (i_transaction_no)
);
COMMENT ON TABLE oracle_tms.ie_shipmentstatus IS 'Tracking events received against shipments.';

INSERT INTO oracle_tms.ie_shipmentstatus (i_transaction_no, shipment_gid, status_code_gid, event_date, status_location_gid, ss_remark) VALUES
(7700001, 'AUS.SH-26-00412', 'AUS.PICKED_UP', '2026-08-06 14:00:00+00', 'AUS.US20_DC', NULL),
(7700002, 'AUS.SH-26-00412', 'AUS.DELIVERED', '2026-08-07 17:00:00+00', 'AUS.C200010', NULL),
(7700003, 'AUS.SH-26-00428', 'AUS.PICKED_UP', '2026-08-20 13:30:00+00', 'AUS.US20_DC', NULL),
(7700004, 'AUS.SH-26-00428', 'AUS.DELIVERED', '2026-08-21 16:30:00+00', 'AUS.C200010', NULL),
(7700005, 'AUS.SH-26-00433', 'AUS.PICKED_UP', '2026-08-27 15:10:00+00', 'AUS.US20_DC', NULL),
(7700006, 'AUS.SH-26-00433', 'AUS.DELIVERED', '2026-08-28 18:10:00+00', 'AUS.C200020', NULL),
(7700007, 'AUS.SH-26-00447', 'AUS.PICKED_UP', '2026-09-15 12:45:00+00', 'AUS.US20_DC', NULL),
(7700008, 'AUS.SH-26-00447', 'AUS.DELIVERED', '2026-09-16 15:45:00+00', 'AUS.C200030', NULL),
(7700009, 'AUS.SH-26-00451', 'AUS.PICKED_UP', '2026-09-18 11:20:00+00', 'AUS.US20_DC', NULL),
(7700010, 'AUS.SH-26-00451', 'AUS.DELIVERED', '2026-09-19 14:20:00+00', 'AUS.C200080', NULL),
(7700011, 'AUS.SH-26-00458', 'AUS.PICKED_UP', '2026-09-24 09:40:00+00', 'AUS.US20_DC', NULL),
(7700012, 'AUS.SH-26-00458', 'AUS.DELIVERED', '2026-09-25 12:40:00+00', 'AUS.C200040', NULL),
(7700013, 'AUS.SH-26-TX0015', 'AUS.RELEASED', '2026-07-28 11:00:00+00', 'AUS.US10_PLANT', 'Released for shipment by QA'),
(7700014, 'AUS.SH-26-TX0015', 'AUS.PICKED_UP', '2026-07-28 16:30:00+00', 'AUS.US10_PLANT', NULL),
(7700015, 'AUS.SH-26-TX0015', 'AUS.DELIVERED', '2026-07-29 10:15:00+00', 'AUS.C200040', 'Received by cell therapy lab; seal intact'),
(7700016, 'AUS.SH-26-TX0015', 'AUS.ADMINISTERED', '2026-07-30 09:40:00+00', 'AUS.C200040', 'Infusion confirmed by treating clinician'),
(7700017, 'AUS.SH-26-TX0016', 'AUS.RELEASED', '2026-08-25 10:30:00+00', 'AUS.US10_PLANT', 'Released for shipment by QA'),
(7700018, 'AUS.SH-26-TX0016', 'AUS.PICKED_UP', '2026-08-25 13:00:00+00', 'AUS.US10_PLANT', NULL),
(7700019, 'AUS.SH-26-TX0016', 'AUS.DELIVERED', '2026-08-25 17:20:00+00', 'AUS.C200070', 'Received by cell therapy lab; seal intact'),
(7700020, 'AUS.SH-26-TX0016', 'AUS.ADMINISTERED', '2026-08-27 08:55:00+00', 'AUS.C200070', 'Infusion confirmed by treating clinician'),
(7700021, 'AUS.SH-26-TX0017', 'AUS.RELEASED', '2026-09-15 09:30:00+00', 'AUS.US10_PLANT', 'Released for shipment by QA'),
(7700022, 'AUS.SH-26-TX0017', 'AUS.PICKED_UP', '2026-09-15 15:00:00+00', 'AUS.US10_PLANT', NULL),
(7700023, 'AUS.SH-26-TX0017', 'AUS.DELIVERED', '2026-09-16 09:45:00+00', 'AUS.C200040', 'Received by cell therapy lab; seal intact'),
(7700024, 'AUS.SH-26-TX0017', 'AUS.ADMINISTERED', '2026-09-17 10:05:00+00', 'AUS.C200040', 'Infusion confirmed by treating clinician')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/oracle_tms).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS oracle_tms.ie_batch_release (
  batch_no             varchar(40) NOT NULL,
  market_code          varchar(8) NOT NULL,
  release_status       varchar(20) NOT NULL,
  release_date         date NOT NULL,
  released_qty         integer,
  record_complete      char(1) NOT NULL,
  deviation_ref        varchar(40),
  storage_instructions text,
  CONSTRAINT ie_batch_release_pk PRIMARY KEY (batch_no, market_code)
);
COMMENT ON TABLE oracle_tms.ie_batch_release IS 'Inbound batch release status: a shipment carrying the batch may be tendered once certified for its market.  From Batch Certification Decisions.';

CREATE TABLE IF NOT EXISTS oracle_tms.hazmat_item (
  hazmat_item_gid  varchar(101) NOT NULL,
  substance_code   varchar(20),
  product_code     varchar(20),
  item_description text NOT NULL,
  un_number        varchar(20) NOT NULL,
  packing_group    varchar(5),
  hazard_class     varchar(10) NOT NULL,
  labels           text NOT NULL,
  documentation    text NOT NULL,
  effective_date   date NOT NULL,
  CONSTRAINT hazmat_item_pk PRIMARY KEY (hazmat_item_gid)
);
COMMENT ON TABLE oracle_tms.hazmat_item IS 'Hazardous material item classifications used when building shipments, from Transport Classifications.';

CREATE TABLE IF NOT EXISTS oracle_tms.dg_signatory_qualification (
  worker_ref           varchar(40) NOT NULL,
  competency_code      varchar(40) NOT NULL,
  certificate_number   varchar(40),
  valid_from           date NOT NULL,
  valid_to             date NOT NULL,
  qualification_status varchar(20) NOT NULL,
  role_code            varchar(40) NOT NULL,
  CONSTRAINT dg_signatory_qualification_pk PRIMARY KEY (worker_ref, competency_code)
);
COMMENT ON TABLE oracle_tms.dg_signatory_qualification IS 'Dangerous goods training qualifications of declaration signatories (by worker pseudonym), from Worker Qualifications.';

GRANT USAGE ON SCHEMA oracle_tms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA oracle_tms TO egeria_user, airflow_user;
