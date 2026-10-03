-- Extract: Microsoft Entra ID (Austin) -> Access Entitlements / account
-- Source: austin_systems.entra_id (SoftwareServer::AUS-SYS-032::SN-AAD-AU-20200601)
-- Target: coco_data_hub.access_entitlements.account
-- users: account key is the UPN; deleted -> removed, sign-in blocked -> suspended; end date from deletion or leave
-- date.
SELECT
  u.userprincipalname::varchar(60) AS user_account_identifier,
  ('WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  'SoftwareServer::AUS-SYS-032::SN-AAD-AU-20200601'::varchar(60) AS system_identifier,
  u.createddatetime::date AS user_account_start_date,
  coalesce(u.deleteddatetime, u.signin_blocked_datetime)::date AS user_account_end_date,
  (CASE WHEN u.deleteddatetime IS NOT NULL THEN 'removed'
        WHEN NOT u.accountenabled THEN 'suspended' ELSE 'active' END)::varchar(20) AS user_account_current_status,
  u.extension_workday_event_id::varchar(40) AS worker_event_identifier
FROM entra_id.users u
WHERE u.employeeid IS NOT NULL
