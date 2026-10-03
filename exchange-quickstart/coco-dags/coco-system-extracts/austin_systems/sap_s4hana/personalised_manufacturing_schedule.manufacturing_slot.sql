-- Extract: SAP S/4HANA (Austin) -> Personalised Manufacturing Schedule / manufacturing_slot
-- Source: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Target: coco_data_hub.personalised_manufacturing_schedule.manufacturing_slot
-- Patient-specific process orders (aufk.auart = ZPAT) with afko scheduling and afpo batch; slot status from jest (DLFL
-- cancelled, TECO/CNF complete, REL with actual start in progress, otherwise scheduled).
WITH st AS (
  SELECT objnr, array_agg(stat) FILTER (WHERE coalesce(inact, '') <> 'X') AS stats FROM sap_s4hana.jest GROUP BY objnr
)
SELECT
  p.charg::varchar(40) AS batch_identifier,
  a.zz_treatment_order::varchar(40) AS order_identifier,
  a.zz_patient_pseudonym::varchar(40) AS patient_pseudonym_identifier,
  p.matnr::varchar(20) AS product_code,
  ((to_date(k.gstrp, 'YYYYMMDD') + k.gsuzp::time) AT TIME ZONE 'UTC') AS slot_start_timestamp,
  ((to_date(k.gltrp, 'YYYYMMDD') + k.gluzp::time) AT TIME ZONE 'UTC') AS slot_end_timestamp,
  a.zz_patient_params AS patient_parameter_description,
  (CASE WHEN 'I0076' = ANY(st.stats) THEN 'cancelled'
        WHEN 'I0045' = ANY(st.stats) OR 'I0009' = ANY(st.stats) THEN 'complete'
        WHEN 'I0002' = ANY(st.stats) AND k.gstri IS NOT NULL THEN 'in progress'
        ELSE 'scheduled' END)::varchar(20) AS slot_status
FROM sap_s4hana.aufk a
JOIN sap_s4hana.afko k ON k.mandt = a.mandt AND k.aufnr = a.aufnr
JOIN sap_s4hana.afpo p ON p.mandt = a.mandt AND p.aufnr = a.aufnr AND p.posnr = '0001'
LEFT JOIN st ON st.objnr = a.objnr
WHERE a.mandt = '100' AND a.auart = 'ZPAT'
