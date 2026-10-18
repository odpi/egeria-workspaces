-- Subscription: aus_sap_s4hana__patient_pseudonym_register - SAP S/4HANA (Austin) receives Patient Pseudonym Register
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Personalised Manufacturing Schedule depends on it (identified manufacturing instruction)
-- Keeps the pseudonym links for Austin treatment orders (product AU-) in the NEW Z table ZPP_PSEUDONYM_LINK, from
-- which planning creates the ZPAT process order carrying the pseudonym; AUFK, read by the schedule extract, is only
-- written when the order is created. Administration records (TMS/EBR business) and other estates' links are
-- discarded.

UPDATE incoming_patient_pseudonym_link i SET discard_reason = 'other estate: not an Austin product'
 WHERE i.product_code NOT LIKE 'AU-%';
INSERT INTO sap_s4hana.zpp_pseudonym_link
       (mandt, zz_patient_pseudonym, zz_treatment_order, matnr, issued_date, issued_time, zz_patient_params)
SELECT '100', i.patient_pseudonym_identifier, i.order_identifier, i.product_code,
       to_char(i.patient_pseudonym_issued_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.patient_pseudonym_issued_timestamp AT TIME ZONE 'UTC', 'HH24MISS'),
       left(i.patient_parameter_description, 255)
  FROM incoming_patient_pseudonym_link i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, zz_patient_pseudonym) DO UPDATE SET
       zz_treatment_order = EXCLUDED.zz_treatment_order, matnr = EXCLUDED.matnr, issued_date = EXCLUDED.issued_date,
       issued_time = EXCLUDED.issued_time, zz_patient_params = EXCLUDED.zz_patient_params;

UPDATE incoming_administration_record SET discard_reason = 'administration is recorded by TMS and the EBR, not ERP';
