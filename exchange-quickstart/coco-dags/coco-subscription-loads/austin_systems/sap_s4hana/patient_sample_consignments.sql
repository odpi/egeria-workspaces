-- Subscription: aus_sap_s4hana__patient_sample_consignments - SAP S/4HANA (Austin) receives Patient Sample Consignments
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Personalised Manufacturing Schedule depends on it (patient material received)
-- Keeps courier notices of patient material for Austin treatment orders (TO-) as inbound deliveries of type ZPMI in
-- LIKP with goods receipt status A (expected): the cell suite posts the receipt (status C), which is the only state
-- the schedule extract reads. Consignments already known (courier shipment ID in LIFEX) and other estates'
-- consignments are discarded.

UPDATE incoming_sample_consignment i SET discard_reason = 'other estate: not an Austin treatment order'
 WHERE i.order_identifier NOT LIKE 'TO-%';
UPDATE incoming_sample_consignment i SET discard_reason = 'already held: inbound delivery exists'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.likp l WHERE l.mandt = '100' AND l.lifex = i.shipment_identifier
                  AND l.vbeln NOT LIKE '19%');
INSERT INTO sap_s4hana.likp AS l
       (mandt, vbeln, lfart, lifex, lfdat, lfuhr, lifnr, zz_patient_pseudonym, zz_arrival_cond, zz_viable_hours, wbstk)
SELECT '100', '19' || right(lpad(regexp_replace(i.shipment_identifier, '[^0-9]', '', 'g'), 8, '0'), 8), 'ZPMI',
       left(i.shipment_identifier, 35),
       to_char(coalesce(i.shipment_delivery_timestamp, i.shipment_dispatch_timestamp) AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(coalesce(i.shipment_delivery_timestamp, i.shipment_dispatch_timestamp) AT TIME ZONE 'UTC', 'HH24MISS'),
       NULL, i.patient_pseudonym_identifier, left(i.shipment_arrival_description, 255), i.sample_viable_duration, 'A'
  FROM incoming_sample_consignment i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, vbeln) DO UPDATE SET
       lifex = EXCLUDED.lifex, lfdat = EXCLUDED.lfdat, lfuhr = EXCLUDED.lfuhr,
       zz_patient_pseudonym = EXCLUDED.zz_patient_pseudonym, zz_arrival_cond = EXCLUDED.zz_arrival_cond,
       zz_viable_hours = EXCLUDED.zz_viable_hours
 WHERE l.wbstk = 'A';
