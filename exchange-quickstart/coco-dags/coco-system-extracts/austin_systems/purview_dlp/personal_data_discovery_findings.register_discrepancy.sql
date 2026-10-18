-- Extract: Microsoft Purview DLP (Austin) -> Personal Data Discovery Findings / register_discrepancy
-- Source: austin_systems.purview_dlp (SoftwareServer::AUS-SYS-039::SN-DLP-AU-20220601)
-- Target: coco_data_hub.personal_data_discovery_findings.register_discrepancy
-- health_action rows from the privacy rules; finding types and states translated.
SELECT
  h.action_id::varchar(40) AS discrepancy_identifier,
  h.target_asset_guid::varchar(40) AS holding_identifier,
  h.target_processing_activity::varchar(40) AS processing_activity_identifier,
  (CASE h.finding_type WHEN 'PersonalDataNotRegistered' THEN 'unregistered holding'
        WHEN 'RegisteredActivityNoAsset' THEN 'missing holding' ELSE 'category mismatch' END)::varchar(40) AS discrepancy_type,
  h.description AS discrepancy_description,
  (CASE h.state WHEN 'Active' THEN 'open' WHEN 'Resolved.RegisterCorrected' THEN 'register corrected'
        WHEN 'Resolved.HoldingRemoved' THEN 'holding removed' ELSE 'accepted' END)::varchar(40) AS discrepancy_current_status
FROM purview_dlp.health_action h
