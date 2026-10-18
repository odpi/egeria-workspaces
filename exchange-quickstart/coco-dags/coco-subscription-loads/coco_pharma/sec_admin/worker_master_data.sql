-- Subscription: coco_sec_admin__worker_master_data - SecAdmin (Coco core) receives Worker Master Data
-- Destination: coco_pharma.sec_admin (System::sec-admin)
-- Why it subscribes: Access Entitlements depends on it (provision or revoke)
-- Keeps every Coco worker (CW- pseudonyms) in sa_hr_feed (NEW) with the action it implies: PROVISION for an
-- active worker with no account yet, REVOKE for a leaver who still has an active account in sa_user.  Accounts
-- and grants (sa_user, sa_grant) are changed by the administrators working that queue, never directly from the
-- feed.  Discards Austin/EKG workers, whose access is administered in their own directories.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - access administered in its own estate'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';

INSERT INTO sec_admin.sa_hr_feed (worker_ref, worker_cat, company, site_cd, hire_dt, leave_dt, hr_sts, action_req)
SELECT w.worker_pseudonym_identifier, (CASE w.worker_type WHEN 'contractor' THEN 'CTR' ELSE 'EMP' END), w.legal_entity_code,
       w.site_code, w.worker_hire_date, w.worker_leave_date,
       (CASE w.worker_current_status WHEN 'left' THEN 'T' WHEN 'on leave' THEN 'L' ELSE 'A' END),
       (CASE WHEN w.worker_current_status = 'left'
                  AND EXISTS (SELECT 1 FROM sec_admin.sa_user u WHERE u.worker_ref = w.worker_pseudonym_identifier AND u.acct_sts = 'A')
             THEN 'REVOKE'
             WHEN w.worker_current_status <> 'left'
                  AND NOT EXISTS (SELECT 1 FROM sec_admin.sa_user u WHERE u.worker_ref = w.worker_pseudonym_identifier)
             THEN 'PROVISION' END)
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL
ON CONFLICT (worker_ref) DO UPDATE SET worker_cat = EXCLUDED.worker_cat, company = EXCLUDED.company, site_cd = EXCLUDED.site_cd,
       hire_dt = EXCLUDED.hire_dt, leave_dt = EXCLUDED.leave_dt, hr_sts = EXCLUDED.hr_sts, action_req = EXCLUDED.action_req;

UPDATE incoming_worker_assignment a SET discard_reason = 'not a Coco worker'
 WHERE NOT EXISTS (SELECT 1 FROM sec_admin.sa_hr_feed f WHERE f.worker_ref = a.worker_pseudonym_identifier);

UPDATE sec_admin.sa_hr_feed f SET job_cd = a.role_code, mgr_ref = a.manager_pseudonym_identifier
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = f.worker_ref;
