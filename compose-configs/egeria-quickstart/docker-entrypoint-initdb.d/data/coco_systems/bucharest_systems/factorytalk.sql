-- system-qualified-name: SoftwareServer::SYS-015::Rockwell FactoryTalk
-- Rockwell FactoryTalk - Bucharest.  FactoryTalk View SE supervising the EKG sterile lines, with no process historian:
-- critical parameters are kept only in the HMI data log (local server time), the batch in progress is a logged string
-- tag, and the packaging line controller records serialisation events.  Its tables feed Process Parameter Time Series
-- and Commissioned Packs.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS factorytalk;
COMMENT ON SCHEMA factorytalk IS 'Rockwell FactoryTalk View SE (EKG): HMI tag database extract, the ODBC data log (FloatTable/StringTable/TagTable, local time Europe/Bucharest) and the packaging line serialisation events.';

CREATE TABLE IF NOT EXISTS factorytalk.tagtable (
  tagindex    smallint NOT NULL,
  tagname     varchar(255) NOT NULL,
  tagtype     smallint NOT NULL,
  tagdatatype smallint NOT NULL,
  CONSTRAINT tagtable_pk PRIMARY KEY (tagindex)
);
COMMENT ON TABLE factorytalk.tagtable IS 'Data log tag index (tagtype 1 analog, 3 string).';

INSERT INTO factorytalk.tagtable (tagindex, tagname, tagtype, tagdatatype) VALUES
(0, 'RO10-CMX-01\TT101', 1, 2),
(1, 'RO10-FLT-01\PDT201', 1, 2),
(2, 'RO10-AMP-01\FT302', 1, 2),
(3, 'RO10-VFL-01\WT501', 1, 2),
(4, 'RO10-AUT-01\TT401', 1, 2),
(5, 'RO10-AUT-02\TT401', 1, 2),
(6, 'RO10-CMX-01\BatchID', 3, 3),
(7, 'RO10-FLT-01\BatchID', 3, 3),
(8, 'RO10-AMP-01\BatchID', 3, 3),
(9, 'RO10-VFL-01\BatchID', 3, 3),
(10, 'RO10-AUT-01\BatchID', 3, 3),
(11, 'RO10-AUT-02\BatchID', 3, 3)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS factorytalk.hmitag (
  tagname     varchar(255) NOT NULL,
  description varchar(120),
  units       varchar(20),
  minimum     double precision,
  maximum     double precision,
  alarm_lo    double precision,
  alarm_hi    double precision,
  CONSTRAINT hmitag_pk PRIMARY KEY (tagname)
);
COMMENT ON TABLE factorytalk.hmitag IS 'HMI tag database export for the logged analog tags: engineering range and the alarm limits (= proven acceptable range).';

INSERT INTO factorytalk.hmitag (tagname, description, units, minimum, maximum, alarm_lo, alarm_hi) VALUES
('RO10-CMX-01\TT101', 'Temperatură soluție vas preparare', 'degC', 0.0, 150.0, 15.0, 25.0),
('RO10-FLT-01\PDT201', 'Presiune diferențială filtru steril', 'bar', 0.0, 6.0, 0.5, 2.5),
('RO10-AMP-01\FT302', 'Debit azot purjare fiole', 'L/min', 0.0, 30.0, 5.0, 15.0),
('RO10-VFL-01\WT501', 'Masă umplere pulbere (control gravimetric)', 'g', 0.0, 2.0, 1.19, 1.25),
('RO10-AUT-01\TT401', 'Temperatură cameră autoclavă 1', 'degC', 0.0, 150.0, 121.0, 124.0),
('RO10-AUT-02\TT401', 'Temperatură cameră autoclavă 2', 'degC', 0.0, 150.0, 121.0, 124.0)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS factorytalk.floattable (
  dateandtime timestamp NOT NULL,
  millitm     smallint NOT NULL,
  tagindex    smallint NOT NULL,
  val         double precision NOT NULL,
  status      char(1),
  marker      char(1),
  CONSTRAINT floattable_pk PRIMARY KEY (dateandtime, millitm, tagindex)
);
COMMENT ON TABLE factorytalk.floattable IS 'Data log analog values: DateAndTime is LOCAL server time (Europe/Bucharest, no zone); status A = alarm at the time of logging.';

INSERT INTO factorytalk.floattable (dateandtime, millitm, tagindex, val, status, marker) VALUES
('2026-07-07 04:23:00', 0, 0, 21.28, ' ', ' '),
('2026-07-07 09:01:00', 0, 0, 19.34, ' ', ' '),
('2026-07-07 04:23:00', 0, 1, 1.18, ' ', ' '),
('2026-07-07 09:01:00', 0, 1, 1.06, ' ', ' '),
('2026-07-07 17:43:00', 0, 2, 8.84, ' ', ' '),
('2026-07-07 21:12:00', 0, 2, 11.0, ' ', ' '),
('2026-07-08 00:41:00', 0, 2, 11.4, ' ', ' '),
('2026-07-21 08:26:00', 0, 3, 1.222, ' ', ' '),
('2026-07-21 12:57:00', 0, 3, 1.226, ' ', ' '),
('2026-07-21 17:28:00', 0, 3, 1.215, ' ', ' '),
('2026-08-04 04:03:00', 0, 0, 19.24, ' ', ' '),
('2026-08-04 08:36:00', 0, 0, 18.54, ' ', ' '),
('2026-08-04 04:03:00', 0, 1, 0.9, ' ', ' '),
('2026-08-04 08:36:00', 0, 1, 1.14, ' ', ' '),
('2026-08-04 17:10:00', 0, 2, 8.38, ' ', ' '),
('2026-08-04 20:35:00', 0, 2, 10.2, ' ', ' '),
('2026-08-05 00:00:00', 0, 2, 8.28, ' ', ' '),
('2026-08-18 04:23:00', 0, 0, 20.94, ' ', ' '),
('2026-08-18 09:01:00', 0, 0, 19.16, ' ', ' '),
('2026-08-18 04:23:00', 0, 1, 0.91, ' ', ' '),
('2026-08-18 09:01:00', 0, 1, 1.29, ' ', ' '),
('2026-08-18 17:43:00', 0, 2, 11.68, ' ', ' '),
('2026-08-18 21:12:00', 0, 2, 10.54, ' ', ' '),
('2026-08-19 00:41:00', 0, 2, 10.7, ' ', ' '),
('2026-08-18 20:27:00', 0, 2, 0.0, 'A', ' '),
('2026-09-01 00:31:00', 0, 0, 21.6, ' ', ' '),
('2026-09-01 04:11:00', 0, 0, 18.98, ' ', ' '),
('2026-09-01 00:31:00', 0, 1, 0.94, ' ', ' '),
('2026-09-01 04:11:00', 0, 1, 1.1, ' ', ' '),
('2026-09-01 11:12:00', 0, 2, 7.92, ' ', ' '),
('2026-09-01 13:57:00', 0, 2, 11.16, ' ', ' '),
('2026-09-01 16:42:00', 0, 2, 10.16, ' ', ' '),
('2026-09-01 22:48:00', 0, 5, 121.51, ' ', ' '),
('2026-09-02 01:33:00', 0, 5, 121.6, ' ', ' '),
('2026-09-02 04:18:00', 0, 5, 122.12, ' ', ' '),
('2026-09-15 00:15:00', 0, 0, 19.98, ' ', ' '),
('2026-09-15 03:51:00', 0, 0, 22.44, ' ', ' '),
('2026-09-15 00:15:00', 0, 1, 1.6, ' ', ' '),
('2026-09-15 03:51:00', 0, 1, 1.08, ' ', ' '),
('2026-09-15 10:45:00', 0, 2, 8.98, ' ', ' '),
('2026-09-15 13:27:00', 0, 2, 10.96, ' ', ' '),
('2026-09-15 16:09:00', 0, 2, 10.48, ' ', ' '),
('2026-09-15 22:09:00', 0, 4, 121.64, ' ', ' '),
('2026-09-16 00:51:00', 0, 4, 122.17, ' ', ' '),
('2026-09-16 03:33:00', 0, 4, 121.94, ' ', ' '),
('2026-09-29 09:16:00', 0, 3, 1.214, ' ', ' '),
('2026-09-29 13:57:00', 0, 3, 1.222, ' ', ' '),
('2026-09-29 18:38:00', 0, 3, 1.218, ' ', ' '),
('2026-08-31 12:00:00', 0, 4, 24.6, ' ', ' '),
('2026-09-21 12:00:00', 0, 0, 21.3, ' ', ' '),
('2026-09-21 12:00:00', 0, 2, 0.0, ' ', ' ')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS factorytalk.stringtable (
  dateandtime timestamp NOT NULL,
  millitm     smallint NOT NULL,
  tagindex    smallint NOT NULL,
  val         varchar(82),
  status      char(1),
  marker      char(1),
  CONSTRAINT stringtable_pk PRIMARY KEY (dateandtime, millitm, tagindex)
);
COMMENT ON TABLE factorytalk.stringtable IS 'Data log string values: the unit''s BatchID tag, set when the batch is loaded at the HMI and cleared at the end (marker B = begin, E = end); local server time.';

INSERT INTO factorytalk.stringtable (dateandtime, millitm, tagindex, val, status, marker) VALUES
('2026-07-06 23:45:00', 0, 6, 'EK26-0311', ' ', 'B'),
('2026-07-07 13:41:00', 0, 6, '', ' ', 'E'),
('2026-07-06 23:45:00', 0, 7, 'EK26-0311', ' ', 'B'),
('2026-07-07 13:41:00', 0, 7, '', ' ', 'E'),
('2026-07-07 14:15:00', 0, 8, 'EK26-0311', ' ', 'B'),
('2026-07-08 04:11:00', 0, 8, '', ' ', 'E'),
('2026-07-21 03:55:00', 0, 9, 'EK26-0318', ' ', 'B'),
('2026-07-21 22:01:00', 0, 9, '', ' ', 'E'),
('2026-08-03 23:30:00', 0, 6, 'EK26-0324', ' ', 'B'),
('2026-08-04 13:11:00', 0, 6, '', ' ', 'E'),
('2026-08-03 23:30:00', 0, 7, 'EK26-0324', ' ', 'B'),
('2026-08-04 13:11:00', 0, 7, '', ' ', 'E'),
('2026-08-04 13:45:00', 0, 8, 'EK26-0324', ' ', 'B'),
('2026-08-05 03:26:00', 0, 8, '', ' ', 'E'),
('2026-08-17 23:45:00', 0, 6, 'EK26-0329', ' ', 'B'),
('2026-08-18 13:41:00', 0, 6, '', ' ', 'E'),
('2026-08-17 23:45:00', 0, 7, 'EK26-0329', ' ', 'B'),
('2026-08-18 13:41:00', 0, 7, '', ' ', 'E'),
('2026-08-18 14:15:00', 0, 8, 'EK26-0329', ' ', 'B'),
('2026-08-19 04:11:00', 0, 8, '', ' ', 'E'),
('2026-08-31 20:51:00', 0, 6, 'EK26-0335', ' ', 'B'),
('2026-09-01 07:53:00', 0, 6, '', ' ', 'E'),
('2026-08-31 20:51:00', 0, 7, 'EK26-0335', ' ', 'B'),
('2026-09-01 07:53:00', 0, 7, '', ' ', 'E'),
('2026-09-01 08:27:00', 0, 8, 'EK26-0335', ' ', 'B'),
('2026-09-01 19:29:00', 0, 8, '', ' ', 'E'),
('2026-09-01 20:03:00', 0, 11, 'EK26-0335', ' ', 'B'),
('2026-09-02 07:05:00', 0, 11, '', ' ', 'E'),
('2026-09-14 20:39:00', 0, 6, 'EK26-0341', ' ', 'B'),
('2026-09-15 07:29:00', 0, 6, '', ' ', 'E'),
('2026-09-14 20:39:00', 0, 7, 'EK26-0341', ' ', 'B'),
('2026-09-15 07:29:00', 0, 7, '', ' ', 'E'),
('2026-09-15 08:03:00', 0, 8, 'EK26-0341', ' ', 'B'),
('2026-09-15 18:53:00', 0, 8, '', ' ', 'E'),
('2026-09-15 19:27:00', 0, 10, 'EK26-0341', ' ', 'B'),
('2026-09-16 06:17:00', 0, 10, '', ' ', 'E'),
('2026-09-29 04:35:00', 0, 9, 'EK26-0347', ' ', 'B'),
('2026-09-29 23:21:00', 0, 9, '', ' ', 'E')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS factorytalk.line_serial_event (
  event_id      bigint NOT NULL,
  line_id       varchar(40) NOT NULL,
  event_type    varchar(20) NOT NULL,
  gtin          varchar(14) NOT NULL,
  serial_no     varchar(20) NOT NULL,
  lot           varchar(40) NOT NULL,
  expiry_yymmdd char(6) NOT NULL,
  parent_sscc   varchar(20),
  event_time    timestamptz NOT NULL,
  CONSTRAINT line_serial_event_pk PRIMARY KEY (event_id)
);
COMMENT ON TABLE factorytalk.line_serial_event IS 'Packaging line serialisation events (EU FMD): COMMISSION, VERIFY (camera grade check) and AGGREGATE (pack to case SSCC); sample of each batch.';

INSERT INTO factorytalk.line_serial_event (event_id, line_id, event_type, gtin, serial_no, lot, expiry_yymmdd, parent_sscc, event_time) VALUES
(710001, 'RO10-PKG-01', 'COMMISSION', '05944821011010', 'LMHQRBN7SDJE', 'EK26-0311', '280630', NULL, '2026-07-08 03:45:00+00'),
(710002, 'RO10-PKG-01', 'VERIFY', '05944821011010', 'LMHQRBN7SDJE', 'EK26-0311', '280630', NULL, '2026-07-08 03:45:02+00'),
(710003, 'RO10-PKG-01', 'AGGREGATE', '05944821011010', 'LMHQRBN7SDJE', 'EK26-0311', '280630', '059448210110065217', '2026-07-08 03:49:00+00'),
(710004, 'RO10-PKG-01', 'COMMISSION', '05944821011010', 'G4YG7ZNZQPYQ', 'EK26-0311', '280630', NULL, '2026-07-08 03:45:17+00'),
(710005, 'RO10-PKG-01', 'VERIFY', '05944821011010', 'G4YG7ZNZQPYQ', 'EK26-0311', '280630', NULL, '2026-07-08 03:45:19+00'),
(710006, 'RO10-PKG-01', 'AGGREGATE', '05944821011010', 'G4YG7ZNZQPYQ', 'EK26-0311', '280630', '059448210110065217', '2026-07-08 03:49:17+00'),
(710007, 'RO10-PKG-01', 'COMMISSION', '05944821011010', 'XTBUDNSA7TTT', 'EK26-0311', '280630', NULL, '2026-07-08 03:45:34+00'),
(710008, 'RO10-PKG-01', 'VERIFY', '05944821011010', 'XTBUDNSA7TTT', 'EK26-0311', '280630', NULL, '2026-07-08 03:45:36+00'),
(710009, 'RO10-PKG-01', 'AGGREGATE', '05944821011010', 'XTBUDNSA7TTT', 'EK26-0311', '280630', '059448210110065217', '2026-07-08 03:49:34+00'),
(710010, 'RO10-PKG-01', 'COMMISSION', '05944821011027', 'VR6CKX5QQN42', 'EK26-0318', '290630', NULL, '2026-07-21 21:35:00+00'),
(710011, 'RO10-PKG-01', 'VERIFY', '05944821011027', 'VR6CKX5QQN42', 'EK26-0318', '290630', NULL, '2026-07-21 21:35:02+00'),
(710012, 'RO10-PKG-01', 'AGGREGATE', '05944821011027', 'VR6CKX5QQN42', 'EK26-0318', '290630', '059448210110085192', '2026-07-21 21:39:00+00'),
(710013, 'RO10-PKG-01', 'COMMISSION', '05944821011027', '2V2ZU46QPMUR', 'EK26-0318', '290630', NULL, '2026-07-21 21:35:17+00'),
(710014, 'RO10-PKG-01', 'VERIFY', '05944821011027', '2V2ZU46QPMUR', 'EK26-0318', '290630', NULL, '2026-07-21 21:35:19+00'),
(710015, 'RO10-PKG-01', 'AGGREGATE', '05944821011027', '2V2ZU46QPMUR', 'EK26-0318', '290630', '059448210110085192', '2026-07-21 21:39:17+00'),
(710016, 'RO10-PKG-01', 'COMMISSION', '05944821011027', '622N6KHA5PRT', 'EK26-0318', '290630', NULL, '2026-07-21 21:35:34+00'),
(710017, 'RO10-PKG-01', 'VERIFY', '05944821011027', '622N6KHA5PRT', 'EK26-0318', '290630', NULL, '2026-07-21 21:35:36+00'),
(710018, 'RO10-PKG-01', 'AGGREGATE', '05944821011027', '622N6KHA5PRT', 'EK26-0318', '290630', '059448210110085192', '2026-07-21 21:39:34+00'),
(710019, 'RO10-PKG-01', 'COMMISSION', '05944821011058', 'MU35XZK3SRNW', 'EK26-0324', '280731', NULL, '2026-08-05 03:00:00+00'),
(710020, 'RO10-PKG-01', 'VERIFY', '05944821011058', 'MU35XZK3SRNW', 'EK26-0324', '280731', NULL, '2026-08-05 03:00:02+00'),
(710021, 'RO10-PKG-01', 'AGGREGATE', '05944821011058', 'MU35XZK3SRNW', 'EK26-0324', '280731', '059448210110078798', '2026-08-05 03:04:00+00'),
(710022, 'RO10-PKG-01', 'COMMISSION', '05944821011058', 'ZGLH4MYT7CP3', 'EK26-0324', '280731', NULL, '2026-08-05 03:00:17+00'),
(710023, 'RO10-PKG-01', 'VERIFY', '05944821011058', 'ZGLH4MYT7CP3', 'EK26-0324', '280731', NULL, '2026-08-05 03:00:19+00'),
(710024, 'RO10-PKG-01', 'AGGREGATE', '05944821011058', 'ZGLH4MYT7CP3', 'EK26-0324', '280731', '059448210110078798', '2026-08-05 03:04:17+00'),
(710025, 'RO10-PKG-01', 'COMMISSION', '05944821011058', 'UBDRP7GMPMVA', 'EK26-0324', '280731', NULL, '2026-08-05 03:00:34+00'),
(710026, 'RO10-PKG-01', 'VERIFY', '05944821011058', 'UBDRP7GMPMVA', 'EK26-0324', '280731', NULL, '2026-08-05 03:00:36+00'),
(710027, 'RO10-PKG-01', 'AGGREGATE', '05944821011058', 'UBDRP7GMPMVA', 'EK26-0324', '280731', '059448210110078798', '2026-08-05 03:04:34+00'),
(710028, 'RO10-PKG-01', 'COMMISSION', '05944821011010', '5EGQP2PK6T4E', 'EK26-0329', '280731', NULL, '2026-08-19 03:45:00+00'),
(710029, 'RO10-PKG-01', 'VERIFY', '05944821011010', '5EGQP2PK6T4E', 'EK26-0329', '280731', NULL, '2026-08-19 03:45:02+00'),
(710030, 'RO10-PKG-01', 'AGGREGATE', '05944821011010', '5EGQP2PK6T4E', 'EK26-0329', '280731', '059448210110005626', '2026-08-19 03:49:00+00'),
(710031, 'RO10-PKG-01', 'COMMISSION', '05944821011010', 'RJPVLN3V3WFF', 'EK26-0329', '280731', NULL, '2026-08-19 03:45:17+00'),
(710032, 'RO10-PKG-01', 'VERIFY', '05944821011010', 'RJPVLN3V3WFF', 'EK26-0329', '280731', NULL, '2026-08-19 03:45:19+00'),
(710033, 'RO10-PKG-01', 'AGGREGATE', '05944821011010', 'RJPVLN3V3WFF', 'EK26-0329', '280731', '059448210110005626', '2026-08-19 03:49:17+00'),
(710034, 'RO10-PKG-01', 'COMMISSION', '05944821011010', 'KFPPWF7XK3X3', 'EK26-0329', '280731', NULL, '2026-08-19 03:45:34+00'),
(710035, 'RO10-PKG-01', 'VERIFY', '05944821011010', 'KFPPWF7XK3X3', 'EK26-0329', '280731', NULL, '2026-08-19 03:45:36+00'),
(710036, 'RO10-PKG-01', 'AGGREGATE', '05944821011010', 'KFPPWF7XK3X3', 'EK26-0329', '280731', '059448210110005626', '2026-08-19 03:49:34+00'),
(710037, 'RO10-PKG-01', 'COMMISSION', '05944821011034', '22QM3T3ME5HB', 'EK26-0335', '280831', NULL, '2026-09-02 06:39:00+00'),
(710038, 'RO10-PKG-01', 'VERIFY', '05944821011034', '22QM3T3ME5HB', 'EK26-0335', '280831', NULL, '2026-09-02 06:39:02+00'),
(710039, 'RO10-PKG-01', 'AGGREGATE', '05944821011034', '22QM3T3ME5HB', 'EK26-0335', '280831', '059448210110002052', '2026-09-02 06:43:00+00'),
(710040, 'RO10-PKG-01', 'COMMISSION', '05944821011034', 'CZDX58WQA5WE', 'EK26-0335', '280831', NULL, '2026-09-02 06:39:17+00'),
(710041, 'RO10-PKG-01', 'VERIFY', '05944821011034', 'CZDX58WQA5WE', 'EK26-0335', '280831', NULL, '2026-09-02 06:39:19+00'),
(710042, 'RO10-PKG-01', 'AGGREGATE', '05944821011034', 'CZDX58WQA5WE', 'EK26-0335', '280831', '059448210110002052', '2026-09-02 06:43:17+00'),
(710043, 'RO10-PKG-01', 'COMMISSION', '05944821011034', 'JRW69JY9XPRG', 'EK26-0335', '280831', NULL, '2026-09-02 06:39:34+00'),
(710044, 'RO10-PKG-01', 'VERIFY', '05944821011034', 'JRW69JY9XPRG', 'EK26-0335', '280831', NULL, '2026-09-02 06:39:36+00'),
(710045, 'RO10-PKG-01', 'AGGREGATE', '05944821011034', 'JRW69JY9XPRG', 'EK26-0335', '280831', '059448210110002052', '2026-09-02 06:43:34+00'),
(710046, 'RO10-PKG-01', 'COMMISSION', '05944821011041', 'RQ358VX4XG34', 'EK26-0341', '280831', NULL, '2026-09-16 05:51:00+00'),
(710047, 'RO10-PKG-01', 'VERIFY', '05944821011041', 'RQ358VX4XG34', 'EK26-0341', '280831', NULL, '2026-09-16 05:51:02+00'),
(710048, 'RO10-PKG-01', 'AGGREGATE', '05944821011041', 'RQ358VX4XG34', 'EK26-0341', '280831', '059448210110089022', '2026-09-16 05:55:00+00'),
(710049, 'RO10-PKG-01', 'COMMISSION', '05944821011041', '8XCYY3RPNZ9W', 'EK26-0341', '280831', NULL, '2026-09-16 05:51:17+00'),
(710050, 'RO10-PKG-01', 'VERIFY', '05944821011041', '8XCYY3RPNZ9W', 'EK26-0341', '280831', NULL, '2026-09-16 05:51:19+00'),
(710051, 'RO10-PKG-01', 'AGGREGATE', '05944821011041', '8XCYY3RPNZ9W', 'EK26-0341', '280831', '059448210110089022', '2026-09-16 05:55:17+00'),
(710052, 'RO10-PKG-01', 'COMMISSION', '05944821011041', '947ZM4785LEM', 'EK26-0341', '280831', NULL, '2026-09-16 05:51:34+00'),
(710053, 'RO10-PKG-01', 'AGGREGATE', '05944821011041', '947ZM4785LEM', 'EK26-0341', '280831', '059448210110089022', '2026-09-16 05:55:34+00')
ON CONFLICT DO NOTHING;

-- Serial number blocks received for the packaging lines (subscription apply script buc_factorytalk__serial_number_allocations).
CREATE TABLE IF NOT EXISTS factorytalk.sn_allocation (
  allocation_id varchar(40) NOT NULL,
  gtin          varchar(14) NOT NULL,
  material      varchar(20),
  target_market varchar(8),
  lot           varchar(40),
  serial_start  varchar(40) NOT NULL,
  serial_end    varchar(40) NOT NULL,
  serial_count  integer NOT NULL,
  received_time timestamptz NOT NULL,
  pool_status   varchar(20) NOT NULL,
  CONSTRAINT sn_allocation_pk PRIMARY KEY (allocation_id)
);
COMMENT ON TABLE factorytalk.sn_allocation IS 'Serialisation serial number pool: blocks of serial numbers allocated per GTIN, market and lot, loaded before the line commissions packs.';

GRANT USAGE ON SCHEMA factorytalk TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA factorytalk TO egeria_user, airflow_user;
