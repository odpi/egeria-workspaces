-- Subscription: aus_purview_dlp__open_metadata_catalogue_holdings - Microsoft Purview DLP (Austin) receives Open Metadata Catalogue Holdings
-- Destination: austin_systems.purview_dlp (SoftwareServer::AUS-SYS-039::SN-DLP-AU-20220601)
-- Why it subscribes: Personal Data Discovery Findings depends on it (catalogued holdings)
-- Keeps the catalogued assets of Austin systems (system identifiers AUS-SYS-) in the NEW external_catalog_asset
-- table, against which the discrepancy rules compare what the scans find; data_map_asset and health_action, which
-- the extracts read, only change when a scan or rule runs. Assets of Coco and EKG systems are discarded.

UPDATE incoming_catalogued_asset i SET discard_reason = 'other estate: not an Austin system'
 WHERE coalesce(i.system_identifier, '') NOT LIKE '%::AUS-SYS-%';
INSERT INTO purview_dlp.external_catalog_asset
       (asset_id, asset_name, asset_type, system_qualified_name, owner_ref, personal_data, confidentiality)
SELECT i.asset_identifier, i.asset_name, i.asset_type, i.system_identifier, i.asset_owner_identifier,
       i.asset_personal_data_flag, i.asset_confidentiality_level
  FROM incoming_catalogued_asset i
 WHERE i.discard_reason IS NULL
ON CONFLICT (asset_id) DO UPDATE SET
       asset_name = EXCLUDED.asset_name, asset_type = EXCLUDED.asset_type,
       system_qualified_name = EXCLUDED.system_qualified_name, owner_ref = EXCLUDED.owner_ref,
       personal_data = EXCLUDED.personal_data, confidentiality = EXCLUDED.confidentiality;
