-- Extract: Informatica MDM (Austin) -> Supplier Master Data / supplier_risk_status
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.supplier_master_data.supplier_risk_status
-- c_b_party_screening joined to the SAP cross-reference; screening codes to clear / match under review / blocked.
SELECT
  x.pkey_src_object::varchar(40) AS supplier_identifier,
  (CASE s.screen_status_cd WHEN 'CLR' THEN 'clear' WHEN 'REV' THEN 'match under review' ELSE 'blocked' END)::varchar(20) AS supplier_screened_status,
  s.screened_dt AS supplier_screened_date,
  lower(s.risk_rating_cd)::varchar(20) AS supplier_rating,
  s.screening_ref::varchar(40) AS screening_identifier,
  s.anomaly_ref::varchar(40) AS anomaly_identifier
FROM informatica_mdm.c_b_party_screening s
JOIN informatica_mdm.c_b_party_xref x ON x.rowid_object = s.rowid_party AND x.rowid_system = 'SAP_S4'
