-- Subscription: coco_hrim__worker_master_data - Human Resources Information Manager (HRIM) (Coco core) receives Worker Master Data
-- Destination: coco_pharma.coco_hrim (System::coco-hrim)
-- Why it subscribes: Worker Qualifications depends on it (new worker record)
-- Keeps nothing: HRIM is the source of every Coco worker record (it issues the CW- pseudonyms), so Coco rows
-- come back as records it already holds in person and job_assignment; the rest are Austin and EKG workers,
-- whose HR is their own (Workday) and outside Coco's HRIM.

UPDATE incoming_worker SET discard_reason = 'Coco worker - HRIM is the source of this record'
 WHERE worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - HR is the acquired estate''s own'
 WHERE discard_reason IS NULL;

UPDATE incoming_worker_assignment SET discard_reason = 'Coco worker assignment - HRIM is the source of this record'
 WHERE worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker_assignment SET discard_reason = 'Austin or EKG worker - HR is the acquired estate''s own'
 WHERE discard_reason IS NULL;
