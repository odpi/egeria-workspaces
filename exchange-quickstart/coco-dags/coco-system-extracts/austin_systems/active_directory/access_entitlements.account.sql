-- Extract: Microsoft Active Directory (Austin) -> Access Entitlements / account
-- Source: austin_systems.active_directory (SoftwareServer::AUS-SYS-031::SN-AD-AU-20170901)
-- Target: coco_data_hub.access_entitlements.account
-- ad_user: account key is DOMAIN\sAMAccountName; disabled accounts are removed once accountexpires has passed,
-- otherwise suspended; FILETIME converted to a date.
SELECT
  ('AUSTINPHARMA\' || u.samaccountname)::varchar(60) AS user_account_identifier,
  ('WP-' || upper(substr(md5('AUS:' || u.employeeid), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  'SoftwareServer::AUS-SYS-031::SN-AD-AU-20170901'::varchar(60) AS system_identifier,
  u.whencreated::date AS user_account_start_date,
  (CASE WHEN u.accountexpires NOT IN (0, 9223372036854775807)
        THEN to_timestamp(u.accountexpires / 10000000 - 11644473600)::date END) AS user_account_end_date,
  (CASE WHEN (u.useraccountcontrol & 2) = 0 THEN 'active'
        WHEN u.accountexpires NOT IN (0, 9223372036854775807) THEN 'removed'
        ELSE 'suspended' END)::varchar(20) AS user_account_current_status,
  u.extensionattribute10::varchar(40) AS worker_event_identifier
FROM active_directory.ad_user u
WHERE u.employeeid IS NOT NULL
