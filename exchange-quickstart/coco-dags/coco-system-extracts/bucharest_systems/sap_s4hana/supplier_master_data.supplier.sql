-- Extract: SAP ERP S/4HANA (Bucharest) -> Supplier Master Data / supplier
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.supplier_master_data.supplier
-- lfa1; account group to supplier type; posting block / deletion flag to status; EKG qualification Z-fields give the
-- approval.
SELECT
  ltrim(v.lifnr, '0')::varchar(40) AS supplier_identifier,
  (v.name1 || coalesce(v.name2, ''))::varchar(200) AS supplier_name,
  (CASE v.ktokk WHEN 'ZRAW' THEN 'material supplier' WHEN 'ZPKG' THEN 'packaging supplier' WHEN 'ZSRV' THEN 'service provider'
        ELSE lower(v.ktokk) END)::varchar(40) AS supplier_type,
  v.land1::varchar(60) AS supplier_country,
  (coalesce(v.zzqual_status, 'N') = 'A') AS supplier_approved_flag,
  to_date(v.zzqual_date, 'YYYYMMDD') AS supplier_approved_date,
  (CASE WHEN v.loevm = 'X' THEN 'deleted' WHEN v.sperr = 'X' THEN 'suspended' ELSE 'active' END)::varchar(20) AS supplier_current_status
FROM sap_s4hana.lfa1 v
WHERE v.mandt = '300'
