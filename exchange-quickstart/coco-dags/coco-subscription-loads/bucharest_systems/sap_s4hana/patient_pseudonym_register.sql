-- Subscription: buc_sap_s4hana__patient_pseudonym_register - SAP ERP S/4HANA (Bucharest) receives Patient Pseudonym Register
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Personalised Manufacturing Schedule depends on it (identified manufacturing instruction)
-- Keeps the pseudonyms issued for EKG's named-patient treatment orders (pseudonym or treatment order known on a ZPAT
-- process order or a ZPMI inbound delivery) in the new Z table zekg_pat_link, with the patient parameters and the
-- process order; aufk itself is not changed (the schedule extract reads it).  A confirmed administration is recorded as a
-- therapy event (zekg_ther_evt) for billing.  Other pseudonyms are discarded (Coco group data - EKG not yet integrated).
-- The product has no source yet.
UPDATE incoming_patient_pseudonym_link i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.aufk a WHERE a.mandt = '300' AND a.auart = 'ZPAT'
                    AND (a.zz_patient_pseudonym = i.patient_pseudonym_identifier OR a.zz_treatment_order = i.order_identifier))
   AND NOT EXISTS (SELECT 1 FROM sap_s4hana.likp l WHERE l.mandt = '300' AND l.lfart = 'ZPMI'
                    AND l.zz_patient_pseudonym = i.patient_pseudonym_identifier);
UPDATE incoming_administration_record i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.afpo p JOIN sap_s4hana.aufk a ON a.mandt = p.mandt AND a.aufnr = p.aufnr AND a.auart = 'ZPAT'
                    WHERE p.mandt = '300' AND p.charg = i.batch_identifier);
UPDATE incoming_administration_record SET discard_reason = 'administration not yet confirmed by the treating site'
 WHERE discard_reason IS NULL AND (treatment_administration_confirmed_flag IS NOT TRUE OR treatment_administration_timestamp IS NULL);

INSERT INTO sap_s4hana.zekg_pat_link (mandt, pseudo_id, treat_order, matnr, issued_date, issued_time, pat_params, aufnr)
SELECT '300', i.patient_pseudonym_identifier, i.order_identifier, i.product_code,
       to_char(i.patient_pseudonym_issued_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.patient_pseudonym_issued_timestamp AT TIME ZONE 'UTC', 'HH24MISS'), left(i.patient_parameter_description, 255),
       (SELECT min(a.aufnr) FROM sap_s4hana.aufk a WHERE a.mandt = '300' AND a.auart = 'ZPAT'
         AND (a.zz_patient_pseudonym = i.patient_pseudonym_identifier OR a.zz_treatment_order = i.order_identifier))
  FROM incoming_patient_pseudonym_link i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, pseudo_id) DO UPDATE
   SET treat_order = EXCLUDED.treat_order, matnr = EXCLUDED.matnr, issued_date = EXCLUDED.issued_date,
       issued_time = EXCLUDED.issued_time, pat_params = EXCLUDED.pat_params, aufnr = EXCLUDED.aufnr;

INSERT INTO sap_s4hana.zekg_ther_evt (mandt, charg, evt_type, evt_date, evt_time, pseudo_id, treat_order, location)
SELECT '300', i.batch_identifier, 'administered', to_char(i.treatment_administration_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.treatment_administration_timestamp AT TIME ZONE 'UTC', 'HH24MISS'), i.patient_pseudonym_identifier,
       (SELECT min(a.zz_treatment_order) FROM sap_s4hana.afpo p JOIN sap_s4hana.aufk a ON a.mandt = p.mandt AND a.aufnr = p.aufnr
         WHERE p.mandt = '300' AND p.charg = i.batch_identifier), NULL
  FROM incoming_administration_record i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, charg, evt_type, evt_date, evt_time) DO NOTHING;
