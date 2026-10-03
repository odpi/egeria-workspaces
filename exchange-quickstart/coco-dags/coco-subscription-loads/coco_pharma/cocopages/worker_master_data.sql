-- Subscription: cocopages__worker_master_data - CocoPages (Coco core) receives Worker Master Data
-- Destination: coco_pharma.cocopages (System::cocopages)
-- Why it subscribes: Corporate Directory Entries depends on it (directory entry)
-- Keeps every Coco worker (CW- pseudonyms) in hr_sync (NEW), the queue the nightly directory refresh works
-- from: entry type EMP/CTR, location, title, manager and leaving date.  dir_person itself is not touched -
-- it is what CocoPages publishes, and the refresh (which also needs names and phone numbers) maintains it.
-- Discards Austin/EKG workers, who are in their own estates' directories.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - listed in its own estate''s directory'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';

INSERT INTO cocopages.hr_sync (worker_ref, entry_typ, loc_cd, hire_dt, leave_dt, hr_sts)
SELECT w.worker_pseudonym_identifier, (CASE w.worker_type WHEN 'contractor' THEN 'CTR' ELSE 'EMP' END), w.site_code,
       w.worker_hire_date, w.worker_leave_date, w.worker_current_status
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL
ON CONFLICT (worker_ref) DO UPDATE SET entry_typ = EXCLUDED.entry_typ, loc_cd = EXCLUDED.loc_cd, hire_dt = EXCLUDED.hire_dt,
       leave_dt = EXCLUDED.leave_dt, hr_sts = EXCLUDED.hr_sts;

UPDATE incoming_worker_assignment a SET discard_reason = 'not a Coco worker'
 WHERE NOT EXISTS (SELECT 1 FROM cocopages.hr_sync s WHERE s.worker_ref = a.worker_pseudonym_identifier);

UPDATE cocopages.hr_sync s SET title = a.role_name, mgr_ref = a.manager_pseudonym_identifier
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = s.worker_ref;
