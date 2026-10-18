-- system-qualified-name: SoftwareServer::AUS-SYS-015::SN-EDI-AU-20190620
-- OpenText Trading Grid EDI - Austin.  The Austin B2B gateway: interchanges and documents exchanged with carriers,
-- 3PLs and customers, including load tenders, advance ship notices, dangerous goods notifications, transport
-- instructions and safety data sheets.  Its tables feed Dangerous Goods Consignment Records (consignment documents).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS opentext_edi;
COMMENT ON SCHEMA opentext_edi IS 'OpenText Trading Grid (Austin): interchange and document tracking tables as landed by the Trading Grid message tracking export.';

CREATE TABLE IF NOT EXISTS opentext_edi.tg_interchange (
  interchange_id   bigint NOT NULL,
  control_number   varchar(20) NOT NULL,
  sender_qualifier varchar(4),
  sender_id        varchar(40) NOT NULL,
  receiver_id      varchar(40) NOT NULL,
  interchange_ts   timestamptz NOT NULL,
  direction        varchar(3) NOT NULL,
  standard         varchar(10) NOT NULL,
  CONSTRAINT tg_interchange_pk PRIMARY KEY (interchange_id)
);
COMMENT ON TABLE opentext_edi.tg_interchange IS 'Interchanges (envelopes) sent and received.';

INSERT INTO opentext_edi.tg_interchange (interchange_id, control_number, sender_qualifier, sender_id, receiver_id, interchange_ts, direction, standard) VALUES
(410201, '000410201', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-08-05 14:00:00+00', 'OUT', 'X12'),
(410202, '000410202', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-08-06 12:00:00+00', 'OUT', 'EDIFACT'),
(410203, '000410203', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-08-06 12:00:00+00', 'OUT', 'EDIFACT'),
(410204, '000410204', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-08-06 12:00:00+00', 'OUT', 'PDF'),
(410205, '000410205', 'ZZ', 'AUSTINPHARMA', 'C200010', '2026-08-06 14:30:00+00', 'OUT', 'X12'),
(410206, '000410206', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-09-14 12:45:00+00', 'OUT', 'X12'),
(410207, '000410207', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-09-15 10:45:00+00', 'OUT', 'EDIFACT'),
(410208, '000410208', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-09-15 10:45:00+00', 'OUT', 'EDIFACT'),
(410209, '000410209', 'ZZ', 'AUSTINPHARMA', 'FEDEX_FREIGHT', '2026-09-15 10:45:00+00', 'OUT', 'PDF'),
(410210, '000410210', 'ZZ', 'AUSTINPHARMA', 'C200030', '2026-09-15 13:15:00+00', 'OUT', 'X12'),
(410211, '000410211', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-17 11:20:00+00', 'OUT', 'X12'),
(410212, '000410212', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-18 09:20:00+00', 'OUT', 'EDIFACT'),
(410213, '000410213', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-18 09:20:00+00', 'OUT', 'EDIFACT'),
(410214, '000410214', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-18 09:20:00+00', 'OUT', 'PDF'),
(410215, '000410215', 'ZZ', 'AUSTINPHARMA', 'C200080', '2026-09-18 11:50:00+00', 'OUT', 'X12'),
(410216, '000410216', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-23 09:40:00+00', 'OUT', 'X12'),
(410217, '000410217', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-24 07:40:00+00', 'OUT', 'EDIFACT'),
(410218, '000410218', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-24 07:40:00+00', 'OUT', 'EDIFACT'),
(410219, '000410219', 'ZZ', 'AUSTINPHARMA', 'UPS_HEALTHCARE', '2026-09-24 07:40:00+00', 'OUT', 'PDF'),
(410220, '000410220', 'ZZ', 'AUSTINPHARMA', 'C200040', '2026-09-24 10:10:00+00', 'OUT', 'X12')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS opentext_edi.tg_document (
  document_id         bigint NOT NULL,
  interchange_id      bigint NOT NULL,
  doc_type            varchar(10) NOT NULL,
  doc_control_number  varchar(20),
  business_ref        varchar(40) NOT NULL,
  document_ref_number varchar(60) NOT NULL,
  document_date       date NOT NULL,
  tracking_status     varchar(20) NOT NULL,
  CONSTRAINT tg_document_pk PRIMARY KEY (document_id)
);
COMMENT ON TABLE opentext_edi.tg_document IS 'Documents within interchanges (business_ref = shipment number); doc types 204 load tender, 856 ASN, IFTDGN dangerous goods notification, IFTMIN transport instruction, SDS attachment.';

INSERT INTO opentext_edi.tg_document (document_id, interchange_id, doc_type, doc_control_number, business_ref, document_ref_number, document_date, tracking_status) VALUES
(9300001, 410201, '204', '4010', 'SH-26-00412', 'LT-26-00412', '2026-08-05', 'ACCEPTED'),
(9300002, 410202, 'IFTDGN', '5342', 'SH-26-00412', 'DGN-26-00412', '2026-08-06', 'ACCEPTED'),
(9300003, 410203, 'IFTMIN', '3756', 'SH-26-00412', 'TI-26-00412', '2026-08-06', 'ACCEPTED'),
(9300004, 410204, 'SDS', '2395', 'SH-26-00412', 'SDS-AU-4410-R4', '2026-08-06', 'ACCEPTED'),
(9300005, 410205, '856', '8238', 'SH-26-00412', 'ASN-26-00412', '2026-08-06', 'DELIVERED'),
(9300006, 410206, '204', '2364', 'SH-26-00447', 'LT-26-00447', '2026-09-14', 'ACCEPTED'),
(9300007, 410207, 'IFTDGN', '0380', 'SH-26-00447', 'DGN-26-00447', '2026-09-15', 'ACCEPTED'),
(9300008, 410208, 'IFTMIN', '8178', 'SH-26-00447', 'TI-26-00447', '2026-09-15', 'ACCEPTED'),
(9300009, 410209, 'SDS', '1706', 'SH-26-00447', 'SDS-9000-R5', '2026-09-15', 'ACCEPTED'),
(9300010, 410210, '856', '2794', 'SH-26-00447', 'ASN-26-00447', '2026-09-15', 'DELIVERED'),
(9300011, 410211, '204', '9089', 'SH-26-00451', 'LT-26-00451', '2026-09-17', 'ACCEPTED'),
(9300012, 410212, 'IFTDGN', '9952', 'SH-26-00451', 'DGN-26-00451', '2026-09-18', 'ACCEPTED'),
(9300013, 410213, 'IFTMIN', '8827', 'SH-26-00451', 'TI-26-00451', '2026-09-18', 'ACCEPTED'),
(9300014, 410214, 'SDS', '1706', 'SH-26-00451', 'SDS-9000-R5', '2026-09-18', 'ACCEPTED'),
(9300015, 410215, '856', '9949', 'SH-26-00451', 'ASN-26-00451', '2026-09-18', 'DELIVERED'),
(9300016, 410216, '204', '6774', 'SH-26-00458', 'LT-26-00458', '2026-09-23', 'ACCEPTED'),
(9300017, 410217, 'IFTDGN', '5891', 'SH-26-00458', 'DGN-26-00458', '2026-09-24', 'ACCEPTED'),
(9300018, 410218, 'IFTMIN', '3756', 'SH-26-00458', 'TI-26-00458', '2026-09-24', 'ACCEPTED'),
(9300019, 410219, 'SDS', '4908', 'SH-26-00458', 'SDS-AU-4630-R6', '2026-09-24', 'ACCEPTED'),
(9300020, 410220, '856', '5455', 'SH-26-00458', 'ASN-26-00458', '2026-09-24', 'DELIVERED')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/opentext_edi).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS opentext_edi.tg_xref_dg_class (
  xref_key       varchar(40) NOT NULL,
  substance_ref  varchar(20),
  product_ref    varchar(20),
  un_number      varchar(20) NOT NULL,
  hazard_class   varchar(10) NOT NULL,
  packing_group  varchar(5),
  label_text     text NOT NULL,
  document_text  text NOT NULL,
  effective_date date NOT NULL,
  CONSTRAINT tg_xref_dg_class_pk PRIMARY KEY (xref_key)
);
COMMENT ON TABLE opentext_edi.tg_xref_dg_class IS 'Cross-reference table used by the IFTDGN map for dangerous goods segments, from Transport Classifications.';

CREATE TABLE IF NOT EXISTS opentext_edi.tg_xref_signatory (
  signatory_ref      varchar(40) NOT NULL,
  competency_code    varchar(40) NOT NULL,
  certificate_number varchar(40),
  valid_from         date NOT NULL,
  valid_to           date NOT NULL,
  status             varchar(20) NOT NULL,
  CONSTRAINT tg_xref_signatory_pk PRIMARY KEY (signatory_ref, competency_code)
);
COMMENT ON TABLE opentext_edi.tg_xref_signatory IS 'Cross-reference of qualified dangerous goods signatories checked by the IFTDGN map, from Worker Qualifications.';

GRANT USAGE ON SCHEMA opentext_edi TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA opentext_edi TO egeria_user, airflow_user;
