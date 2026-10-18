-- Extract: SecAdmin (Coco core) -> Access Entitlements / entitlement
-- Source: coco_pharma.sec_admin (System::sec-admin)
-- Target: coco_data_hub.access_entitlements.entitlement
-- sa_grant with the entitlement definition of the account's system; Y/N owner flag to boolean.
SELECT
  g.acct_id::varchar(60)            AS user_account_identifier,
  g.ent_cd::varchar(60)             AS entitlement_code,
  e.ent_desc                        AS entitlement_description,
  g.granted_dt                      AS entitlement_start_date,
  g.revoked_dt                      AS entitlement_end_date,
  (e.owner_yn = 'Y')                AS entitlement_data_owner_flag
FROM sec_admin.sa_grant g
JOIN sec_admin.sa_user u ON u.acct_id = g.acct_id
JOIN sec_admin.sa_entitlement e ON e.sys_cd = u.sys_cd AND e.ent_cd = g.ent_cd
