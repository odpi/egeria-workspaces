-- Subscription: buc_sap_s4hana__patient_sample_consignments - SAP ERP S/4HANA (Bucharest) receives Patient Sample Consignments
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Personalised Manufacturing Schedule depends on it (patient material received)
-- Announces inbound patient material for EKG's named-patient orders (pseudonym known on a ZPAT process order or ZPMI
-- delivery) as an inbound delivery likp (lfart ZPMI, courier AWB in lifex, wbstk A = not yet received); goods receipt
-- at the dock completes it (wbstk C), and only completed deliveries are read by the schedule extract.  A consignment
-- that already has its inbound delivery is discarded; other pseudonyms are discarded (Coco group data - EKG not yet
-- integrated).  The product has no source yet.
UPDATE incoming_sample_consignment i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.aufk a WHERE a.mandt = '300' AND a.auart = 'ZPAT'
                    AND a.zz_patient_pseudonym = i.patient_pseudonym_identifier)
   AND NOT EXISTS (SELECT 1 FROM sap_s4hana.likp l WHERE l.mandt = '300' AND l.lfart = 'ZPMI'
                    AND l.zz_patient_pseudonym = i.patient_pseudonym_identifier);
UPDATE incoming_sample_consignment i SET discard_reason = 'inbound delivery already exists for this consignment'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.likp l WHERE l.mandt = '300' AND l.lifex = i.shipment_identifier);

INSERT INTO sap_s4hana.likp (mandt, vbeln, lfart, lifex, lfdat, lfuhr, lifnr, zz_patient_pseudonym, zz_arrival_cond,
                             zz_viable_hours, wbstk)
SELECT '300', '0181' || lpad(mod(abs(hashtext(i.shipment_identifier)), 1000000)::text, 6, '0'), 'ZPMI', left(i.shipment_identifier, 35),
       to_char(coalesce(i.shipment_delivery_timestamp, i.shipment_dispatch_timestamp, i.sample_collection_timestamp) AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(coalesce(i.shipment_delivery_timestamp, i.shipment_dispatch_timestamp, i.sample_collection_timestamp) AT TIME ZONE 'UTC', 'HH24MISS'),
       (CASE WHEN i.carrier_identifier ~ '^[0-9]+$' THEN lpad(i.carrier_identifier, 10, '0') END), i.patient_pseudonym_identifier,
       left(i.shipment_arrival_description, 255), i.sample_viable_duration, 'A'
  FROM incoming_sample_consignment i
 WHERE i.discard_reason IS NULL
   AND coalesce(i.shipment_delivery_timestamp, i.shipment_dispatch_timestamp, i.sample_collection_timestamp) IS NOT NULL
ON CONFLICT (mandt, vbeln) DO NOTHING;
UPDATE incoming_sample_consignment SET discard_reason = 'no dispatch or delivery time - not yet announced'
 WHERE discard_reason IS NULL
   AND coalesce(shipment_delivery_timestamp, shipment_dispatch_timestamp, sample_collection_timestamp) IS NULL;
