-- Subscription: buc_sap_s4hana__therapy_delivery_events - SAP ERP S/4HANA (Bucharest) receives Therapy Delivery Events
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Treatment Invoices depends on it (fulfilment confirmed)
-- Keeps delivery and administration confirmations of EKG's named-patient therapies (batch of a ZPAT process order) in
-- the new Z table zekg_ther_evt, which releases the treatment order for billing; the billing documents themselves are
-- not created here (they feed Treatment Invoices).  Other therapies are discarded (Coco group data - EKG not yet
-- integrated); today only Austin's therapies are in the product.
UPDATE incoming_delivery_event i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.afpo p JOIN sap_s4hana.aufk a ON a.mandt = p.mandt AND a.aufnr = p.aufnr AND a.auart = 'ZPAT'
                    WHERE p.mandt = '300' AND p.charg = i.batch_identifier);
UPDATE incoming_administration_confirmation i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.afpo p JOIN sap_s4hana.aufk a ON a.mandt = p.mandt AND a.aufnr = p.aufnr AND a.auart = 'ZPAT'
                    WHERE p.mandt = '300' AND p.charg = i.batch_identifier);
UPDATE incoming_administration_confirmation SET discard_reason = 'administration time not yet reported'
 WHERE discard_reason IS NULL AND treatment_administration_timestamp IS NULL;

INSERT INTO sap_s4hana.zekg_ther_evt (mandt, charg, evt_type, evt_date, evt_time, pseudo_id, treat_order, location)
SELECT '300', i.batch_identifier, i.shipment_event_type, to_char(i.shipment_event_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.shipment_event_timestamp AT TIME ZONE 'UTC', 'HH24MISS'), i.patient_pseudonym_identifier, i.order_identifier,
       i.shipment_event_location
  FROM incoming_delivery_event i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, charg, evt_type, evt_date, evt_time) DO UPDATE
   SET pseudo_id = EXCLUDED.pseudo_id, treat_order = EXCLUDED.treat_order, location = EXCLUDED.location;

INSERT INTO sap_s4hana.zekg_ther_evt (mandt, charg, evt_type, evt_date, evt_time, pseudo_id, treat_order, location)
SELECT '300', i.batch_identifier, 'administered', to_char(i.treatment_administration_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.treatment_administration_timestamp AT TIME ZONE 'UTC', 'HH24MISS'), i.patient_pseudonym_identifier,
       i.order_identifier, NULL
  FROM incoming_administration_confirmation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, charg, evt_type, evt_date, evt_time) DO UPDATE
   SET pseudo_id = EXCLUDED.pseudo_id, treat_order = EXCLUDED.treat_order;
