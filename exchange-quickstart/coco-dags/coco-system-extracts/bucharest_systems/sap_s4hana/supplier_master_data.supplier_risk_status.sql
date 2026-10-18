-- Extract: SAP ERP S/4HANA (Bucharest) -> Supplier Master Data / supplier_risk_status
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.supplier_master_data.supplier_risk_status
-- Latest zekg_vend_scrn screening per vendor; result codes translated; risk rating lower-cased.
SELECT DISTINCT ON (s.lifnr)
  ltrim(s.lifnr, '0')::varchar(40) AS supplier_identifier,
  (CASE s.result WHEN 'C' THEN 'clear' WHEN 'R' THEN 'match under review' ELSE 'blocked' END)::varchar(20) AS supplier_screened_status,
  to_date(s.screen_date, 'YYYYMMDD') AS supplier_screened_date,
  lower(s.risk_rating)::varchar(20) AS supplier_rating,
  s.screen_id::varchar(40) AS screening_identifier,
  s.anomaly_ref::varchar(40) AS anomaly_identifier
FROM sap_s4hana.zekg_vend_scrn s
WHERE s.mandt = '300'
ORDER BY s.lifnr, s.screen_date DESC, s.screen_id DESC
