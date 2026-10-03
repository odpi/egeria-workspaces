-- Extract: Active Directory (Bucharest) -> Access Entitlements / entitlement
-- Source: bucharest_systems.active_directory (SoftwareServer::SYS-008::Active Directory)
-- Target: coco_data_hub.access_entitlements.entitlement
-- ad_group_member joined to ad_group and ad_user; linked-value create/delete times give the grant and revoke dates.
SELECT
  ('EKG\' || u.samaccountname)::varchar(60) AS user_account_identifier,
  g.samaccountname::varchar(60) AS entitlement_code,
  g.description AS entitlement_description,
  m.originating_create_time::date AS entitlement_start_date,
  m.originating_delete_time::date AS entitlement_end_date,
  coalesce(g.extensionattribute1 = 'DATA-OWNER', false) AS entitlement_data_owner_flag
FROM active_directory.ad_group_member m
JOIN active_directory.ad_group g ON g.objectguid = m.group_objectguid
JOIN active_directory.ad_user u ON u.objectguid = m.member_objectguid
