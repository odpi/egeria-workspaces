-- Extract: Microsoft Active Directory (Austin) -> Access Entitlements / entitlement
-- Source: austin_systems.active_directory (SoftwareServer::AUS-SYS-031::SN-AD-AU-20170901)
-- Target: coco_data_hub.access_entitlements.entitlement
-- ad_group_member joined to ad_group and ad_user; LVR create/delete times give the grant and revoke dates.
SELECT
  ('AUSTINPHARMA\' || u.samaccountname)::varchar(60) AS user_account_identifier,
  g.samaccountname::varchar(60) AS entitlement_code,
  g.description AS entitlement_description,
  m.originating_create_time::date AS entitlement_start_date,
  m.originating_delete_time::date AS entitlement_end_date,
  coalesce(g.extensionattribute1 = 'DATA-OWNER', false) AS entitlement_data_owner_flag
FROM active_directory.ad_group_member m
JOIN active_directory.ad_group g ON g.objectguid = m.group_objectguid
JOIN active_directory.ad_user u ON u.objectguid = m.member_objectguid
