-- system-qualified-name: System::manufacturing-planning
-- Global Manufacturing Planning - Coco core.  Coco's COTS planning system that schedules every factory (Winchester, Edmonton and the Austin site); only its personalised orders and inbound patient material feed the Personalised Manufacturing Schedule.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS manufacturing_planning;
COMMENT ON SCHEMA manufacturing_planning IS 'Global Manufacturing Planning (Coco core): planned orders for all factories, personalised order details and inbound patient material.';

CREATE TABLE IF NOT EXISTS manufacturing_planning.plnord (
  plnord_no varchar(20) NOT NULL,
  matnr varchar(10) NOT NULL,
  plant varchar(4) NOT NULL,
  ord_typ varchar(4) NOT NULL,
  batch_no varchar(20),
  cust_ord_ref varchar(20),
  sched_start timestamptz NOT NULL,
  sched_end timestamptz NOT NULL,
  plan_qty integer NOT NULL,
  uom varchar(4) NOT NULL,
  ord_sts varchar(4) NOT NULL,
  created_on timestamptz NOT NULL,
  CONSTRAINT plnord_pk PRIMARY KEY (plnord_no)
);
COMMENT ON TABLE manufacturing_planning.plnord IS 'Planned production orders for every Coco factory. ord_typ STD = batch production, PERS = personalised order; ord_sts FIRM, REL, ACT, CMPL, CNCL.';

CREATE TABLE IF NOT EXISTS manufacturing_planning.plnord_pers (
  plnord_no varchar(20) NOT NULL,
  patient_ref varchar(20) NOT NULL,
  param_text text,
  cust_ord_ref varchar(20) NOT NULL,
  CONSTRAINT plnord_pers_pk PRIMARY KEY (plnord_no)
);
COMMENT ON TABLE manufacturing_planning.plnord_pers IS 'Personalised planned orders: the patient pseudonym issued at order acceptance and the patient-specific parameters.';

CREATE TABLE IF NOT EXISTS manufacturing_planning.inbd_matl (
  consignment_no varchar(20) NOT NULL,
  patient_ref varchar(20) NOT NULL,
  plnord_no varchar(20) NOT NULL,
  arr_ts timestamptz NOT NULL,
  arr_cond_cd varchar(4) NOT NULL,
  arr_note text,
  viab_hrs_rem integer NOT NULL,
  origin_site varchar(60),
  CONSTRAINT inbd_matl_pk PRIMARY KEY (consignment_no)
);
COMMENT ON TABLE manufacturing_planning.inbd_matl IS 'Inbound patient material consignments booked in at the manufacturing site against a personalised order. arr_cond_cd OK, TEMP (excursion), LATE, DMG.';

INSERT INTO manufacturing_planning.plnord (plnord_no, matnr, plant, ord_typ, batch_no, cust_ord_ref, sched_start, sched_end, plan_qty, uom, ord_sts, created_on) VALUES
('GMP-PO-26-0412', '3000', 'USA1', 'STD', 'A26-3000-0141', NULL, '2026-08-03 06:00+00', '2026-08-05 18:00+00', 120000, 'TAB', 'CMPL', '2026-07-13 06:00+00'),
('GMP-PO-26-0431', '2050', 'USA1', 'STD', 'A26-2050-0087', NULL, '2026-08-17 06:00+00', '2026-08-19 14:00+00', 90000, 'TAB', 'CMPL', '2026-07-27 06:00+00'),
('GMP-PO-26-0448', '9000', 'USA1', 'STD', 'A26-9000-0019', NULL, '2026-09-01 07:00+00', '2026-09-02 19:00+00', 2500, 'VIAL', 'CMPL', '2026-08-11 07:00+00'),
('GMP-PO-26-0457', '3000', 'USA1', 'STD', 'A26-3000-0142', NULL, '2026-09-07 06:00+00', '2026-09-09 18:00+00', 120000, 'TAB', 'CMPL', '2026-08-17 06:00+00'),
('GMP-PO-26-0466', '2050', 'USA1', 'STD', 'A26-2050-0088', NULL, '2026-09-28 06:00+00', '2026-09-30 18:00+00', 90000, 'TAB', 'ACT', '2026-09-07 06:00+00'),
('GMP-PO-26-0402', '1000', 'UKW1', 'STD', 'W26-1000-0031', NULL, '2026-07-27 07:00+00', '2026-07-28 16:00+00', 250000, 'TAB', 'CMPL', '2026-07-06 07:00+00'),
('GMP-PO-26-0418', '1010', 'UKW1', 'STD', 'W26-1010-0012', NULL, '2026-08-10 07:00+00', '2026-08-11 15:30+00', 150000, 'TAB', 'CMPL', '2026-07-20 07:00+00'),
('GMP-PO-26-0437', '5000', 'UKW1', 'STD', 'W26-5000-0024', NULL, '2026-08-24 07:00+00', '2026-08-25 17:00+00', 90000, 'TAB', 'CMPL', '2026-08-03 07:00+00'),
('GMP-PO-26-0455', '1000', 'UKW1', 'STD', 'W26-1000-0032', NULL, '2026-09-14 07:00+00', '2026-09-15 16:00+00', 250000, 'TAB', 'CMPL', '2026-08-24 07:00+00'),
('GMP-PO-26-0469', '5000', 'UKW1', 'STD', 'W26-5000-0025', NULL, '2026-09-29 07:00+00', '2026-10-01 19:00+00', 90000, 'TAB', 'ACT', '2026-09-08 07:00+00'),
('GMP-PO-26-0371', '9100', 'UKW1', 'PERS', 'W26-9100-0003', 'SO-26-01102', '2026-05-26 09:00+00', '2026-06-06 09:00+00', 1, 'BAG', 'CMPL', '2026-05-05 09:00+00'),
('GMP-PO-26-0385', '9100', 'UKW1', 'PERS', 'W26-9100-0004', 'SO-26-01127', '2026-06-16 09:00+00', '2026-06-27 09:00+00', 1, 'BAG', 'CMPL', '2026-05-26 09:00+00'),
('GMP-PO-26-0398', '9100', 'UKW1', 'PERS', 'W26-9100-0005', 'SO-26-01145', '2026-07-07 09:00+00', '2026-07-18 09:00+00', 1, 'BAG', 'CMPL', '2026-06-16 09:00+00'),
('GMP-PO-26-0401', '9100', 'UKW1', 'PERS', 'W26-9100-0006', 'SO-26-01152', '2026-07-15 09:00+00', '2026-07-26 09:00+00', 1, 'BAG', 'CNCL', '2026-06-24 09:00+00'),
('GMP-PO-26-0416', '9100', 'UKW1', 'PERS', 'W26-9100-0007', 'SO-26-01163', '2026-08-04 09:00+00', '2026-08-15 09:00+00', 1, 'BAG', 'CMPL', '2026-07-14 09:00+00'),
('GMP-PO-26-0452', '9100', 'UKW1', 'PERS', 'W26-9100-0008', 'SO-26-01181', '2026-09-22 09:00+00', '2026-10-03 09:00+00', 1, 'BAG', 'ACT', '2026-09-01 09:00+00'),
('GMP-PO-26-0471', '9100', 'UKW1', 'PERS', 'W26-9100-0009', 'SO-26-01194', '2026-10-06 09:00+00', '2026-10-17 09:00+00', 1, 'BAG', 'FIRM', '2026-09-15 09:00+00'),
('GMP-PO-26-0399', '2000', 'CAE1', 'STD', 'E26-2000-0044', NULL, '2026-07-20 13:00+00', '2026-07-22 01:00+00', 180000, 'TAB', 'CMPL', '2026-06-29 13:00+00'),
('GMP-PO-26-0414', '4000', 'CAE1', 'STD', 'E26-4000-0027', NULL, '2026-08-04 13:00+00', '2026-08-06 03:00+00', 120000, 'TAB', 'CMPL', '2026-07-14 13:00+00'),
('GMP-PO-26-0429', '2010', 'CAE1', 'STD', 'E26-2010-0019', NULL, '2026-08-18 13:00+00', '2026-08-19 23:00+00', 180000, 'TAB', 'CMPL', '2026-07-28 13:00+00'),
('GMP-PO-26-0446', '4010', 'CAE1', 'STD', 'E26-4010-0011', NULL, '2026-09-01 13:00+00', '2026-09-03 01:00+00', 120000, 'TAB', 'CMPL', '2026-08-11 13:00+00'),
('GMP-PO-26-0461', '2000', 'CAE1', 'STD', 'E26-2000-0045', NULL, '2026-09-21 13:00+00', '2026-09-23 02:00+00', 180000, 'TAB', 'CMPL', '2026-08-31 13:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO manufacturing_planning.plnord_pers (plnord_no, patient_ref, param_text, cust_ord_ref) VALUES
('GMP-PO-26-0371', 'CPX-7K4Q2M', 'Weight 71kg; target dose 2.0 x 10^8 CAR+ T cells; lymphodepletion day -5', 'SO-26-01102'),
('GMP-PO-26-0385', 'CPX-3M8R1T', 'Weight 64kg; target dose 1.5 x 10^8; lymphodepletion day -5', 'SO-26-01127'),
('GMP-PO-26-0398', 'CPX-9D2H6W', 'Weight 88kg; target dose 2.5 x 10^8; prior bridging therapy', 'SO-26-01145'),
('GMP-PO-26-0401', 'CPX-6W9C3E', 'Weight 59kg; target dose 1.2 x 10^8', 'SO-26-01152'),
('GMP-PO-26-0416', 'CPX-5T1N8B', 'Weight 77kg; target dose 2.0 x 10^8', 'SO-26-01163'),
('GMP-PO-26-0452', 'CPX-2B7J4Y', 'Weight 69kg; target dose 1.8 x 10^8; low lymphocyte count at apheresis', 'SO-26-01181'),
('GMP-PO-26-0471', 'CPX-8F3L5P', 'Weight 82kg; target dose 2.2 x 10^8', 'SO-26-01194')
ON CONFLICT DO NOTHING;

INSERT INTO manufacturing_planning.inbd_matl (consignment_no, patient_ref, plnord_no, arr_ts, arr_cond_cd, arr_note, viab_hrs_rem, origin_site) VALUES
('PMC-26-0118', 'CPX-7K4Q2M', 'GMP-PO-26-0371', '2026-05-25 14:20+00', 'OK', 'Dry shipper intact, logger within -150C', 52, 'Hampton Hospital'),
('PMC-26-0131', 'CPX-3M8R1T', 'GMP-PO-26-0385', '2026-06-15 13:05+00', 'OK', 'Received in specification', 55, 'Bowden Arrow Hospital'),
('PMC-26-0144', 'CPX-9D2H6W', 'GMP-PO-26-0398', '2026-07-06 16:40+00', 'TEMP', 'Logger shows 40 minute excursion to 12C in transit; QA accepted', 41, 'Oak Dene Hospital'),
('PMC-26-0149', 'CPX-6W9C3E', 'GMP-PO-26-0401', '2026-07-14 19:55+00', 'LATE', 'Flight delayed 20 hours; viability below release threshold', 14, 'Oak Dene Hospital'),
('PMC-26-0158', 'CPX-5T1N8B', 'GMP-PO-26-0416', '2026-08-03 12:30+00', 'OK', 'Received in specification', 58, 'Hampton Hospital'),
('PMC-26-0172', 'CPX-2B7J4Y', 'GMP-PO-26-0452', '2026-09-21 15:10+00', 'OK', 'Received in specification; low cell count noted', 49, 'Old Market Hospital')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS manufacturing_planning.pers_psn_reg (
  patient_ref varchar(40) NOT NULL,
  cust_ord_ref varchar(40) NOT NULL,
  matnr varchar(20) NOT NULL,
  issued_ts timestamptz NOT NULL,
  param_text text,
  CONSTRAINT pers_psn_reg_pk PRIMARY KEY (patient_ref)
);
COMMENT ON TABLE manufacturing_planning.pers_psn_reg IS 'Patient pseudonyms issued for personalised orders (Patient Pseudonym Register): the identified manufacturing instruction a PERS planned order is created from.';

CREATE TABLE IF NOT EXISTS manufacturing_planning.inbd_asn (
  consignment_no varchar(40) NOT NULL,
  cust_ord_ref varchar(40) NOT NULL,
  patient_ref varchar(40) NOT NULL,
  origin_site varchar(60) NOT NULL,
  collected_ts timestamptz NOT NULL,
  dispatched_ts timestamptz NOT NULL,
  delivered_ts timestamptz,
  viab_hrs integer,
  arr_note text,
  carrier_ref varchar(40) NOT NULL,
  CONSTRAINT inbd_asn_pk PRIMARY KEY (consignment_no)
);
COMMENT ON TABLE manufacturing_planning.inbd_asn IS 'Advance notice of patient material on its way to the manufacturing site (Patient Sample Consignments); the consignment is booked in to inbd_matl on arrival.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA manufacturing_planning TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA manufacturing_planning TO egeria_user, airflow_user;
