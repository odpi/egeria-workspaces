-- Extract: SAP ERP S/4HANA (Bucharest) -> Material Quarantine Dispositions / release_disposition
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.material_quarantine_dispositions.release_disposition
-- GR inspection lots (qals.art = 01) with their usage decision (qave) and batch expiry (mch1); A* codes released, R*
-- rejected; quantities converted to the WMS base unit (mg for G, g for KG, ml for L, each).
SELECT
  q.charg::varchar(40) AS lot_identifier,
  ((to_date(v.vdatum, 'YYYYMMDD') + v.vezeiterf::time) AT TIME ZONE 'UTC') AS lot_disposition_timestamp,
  (CASE WHEN v.vcode LIKE 'A%' THEN 'released for use' ELSE 'rejected' END)::varchar(20) AS lot_disposition_status,
  v.zz_lims_result::varchar(40) AS test_result_identifier,
  to_date(b.vfdat, 'YYYYMMDD') AS lot_expiry_date,
  (NULLIF(q.lmenge01, 0) * CASE q.mengeneinh WHEN 'KG' THEN 1000 WHEN 'L' THEN 1000 WHEN 'G' THEN 1000 ELSE 1 END)::integer AS lot_released_quantity
FROM sap_s4hana.qals q
JOIN sap_s4hana.qave v ON v.mandt = q.mandt AND v.prueflos = q.prueflos AND v.kzart = 'L'
LEFT JOIN sap_s4hana.mch1 b ON b.mandt = q.mandt AND b.matnr = q.matnr AND b.charg = q.charg
WHERE q.mandt = '300' AND q.art = '01'
