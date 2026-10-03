-- Extract: Microsoft Purview DLP (Austin) -> Personal Data Discovery Findings / discovered_holding
-- Source: austin_systems.purview_dlp (SoftwareServer::AUS-SYS-039::SN-DLP-AU-20220601)
-- Target: coco_data_hub.personal_data_discovery_findings.discovered_holding
-- One holding per classified data map asset: classifications aggregated into the description; data source mapped to
-- the system qualified name; processing activity from the Privacy managed attribute.
SELECT
  a.guid::varchar(40) AS holding_identifier,
  a.name::varchar(40) AS asset_identifier,
  (CASE a.data_source_name WHEN 'SAP-S4-AUS' THEN 'SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923' WHEN 'Workday-AUS' THEN 'SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301' WHEN 'Salesforce-AUS' THEN 'SoftwareServer::AUS-SYS-016::SN-CRM-AU-20200901' WHEN 'ServiceNow-AUS' THEN 'SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601' WHEN 'OracleFusion-OM-AUS' THEN 'SoftwareServer::AUS-SYS-011::SN-OMS-AU-20200310' WHEN 'VeevaVault-QMS-AUS' THEN 'SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901' WHEN 'SharePoint-AUS' THEN 'SoftwareServer::AUS-SYS-033::SN-M365-AU-20200601' WHEN 'OneDrive-AUS' THEN 'SoftwareServer::AUS-SYS-033::SN-M365-AU-20200601' WHEN 'Hive-CDP-AUS' THEN 'SoftwareServer::AUS-SYS-001::CDH-AUS-7X-00142' END)::varchar(60) AS system_identifier,
  (CASE a.data_subject_hint WHEN 'hcp' THEN 'healthcare professional' ELSE a.data_subject_hint END)::varchar(100) AS data_subject_type,
  string_agg(c.classification_name || ' (' || c.match_count || ')', '; ' ORDER BY c.classification_name) AS holding_data_description,
  min(c.first_detected_at) AS holding_discovered_timestamp,
  max(m.attribute_value)::varchar(40) AS processing_activity_identifier
FROM purview_dlp.data_map_asset a
JOIN purview_dlp.asset_classification c ON c.asset_guid = a.guid
LEFT JOIN purview_dlp.asset_managed_attribute m ON m.asset_guid = a.guid AND m.attribute_group = 'Privacy' AND m.attribute_name = 'ProcessingActivityId'
GROUP BY a.guid, a.name, a.data_source_name, a.data_subject_hint
