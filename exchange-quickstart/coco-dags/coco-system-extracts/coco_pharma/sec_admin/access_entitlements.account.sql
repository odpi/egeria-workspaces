-- Extract: SecAdmin (Coco core) -> Access Entitlements / account
-- Source: coco_pharma.sec_admin (System::sec-admin)
-- Target: coco_data_hub.access_entitlements.account
-- sa_user; status codes expanded.
SELECT
  u.acct_id::varchar(60)            AS user_account_identifier,
  u.worker_ref::varchar(40)         AS worker_pseudonym_identifier,
  u.sys_cd::varchar(60)             AS system_identifier,
  u.created_dt                      AS user_account_start_date,
  u.removed_dt                      AS user_account_end_date,
  (CASE u.acct_sts WHEN 'A' THEN 'active' WHEN 'S' THEN 'suspended' ELSE 'removed' END)::varchar(20) AS user_account_current_status,
  u.last_hr_evt::varchar(40)        AS worker_event_identifier
FROM sec_admin.sa_user u
