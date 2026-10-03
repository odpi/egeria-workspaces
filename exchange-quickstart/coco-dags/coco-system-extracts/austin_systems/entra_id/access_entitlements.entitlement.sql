-- Extract: Microsoft Entra ID (Austin) -> Access Entitlements / entitlement
-- Source: austin_systems.entra_id (SoftwareServer::AUS-SYS-032::SN-AAD-AU-20200601)
-- Target: coco_data_hub.access_entitlements.entitlement
-- app_role_assignment joined to service_principal_app_role and users; entitlement code is '<application>:<role
-- value>'.
SELECT
  u.userprincipalname::varchar(60) AS user_account_identifier,
  (r.resource_display_name || ':' || r.value)::varchar(60) AS entitlement_code,
  r.description AS entitlement_description,
  a.createddatetime::date AS entitlement_start_date,
  a.deleteddatetime::date AS entitlement_end_date,
  r.is_data_owner_role AS entitlement_data_owner_flag
FROM entra_id.app_role_assignment a
JOIN entra_id.service_principal_app_role r ON r.resource_id = a.resource_id AND r.app_role_id = a.app_role_id
JOIN entra_id.users u ON u.id = a.principal_id
