-- Subscription: coco_hrim__worker_lifecycle_events - Human Resources Information Manager (HRIM) (Coco core) receives Worker Lifecycle Events
-- Destination: coco_pharma.coco_hrim (System::coco-hrim)
-- Why it subscribes: Worker Master Data depends on it (worker event)
-- Keeps nothing: Coco's joiner, mover and leaver events are raised in HRIM itself (hr_event, hr_event_dist), so
-- they come back as rows it already holds; Austin and EKG events (their own Workday) concern workers HRIM
-- does not manage.

UPDATE incoming_worker_event e SET discard_reason = 'Coco HR event - raised in HRIM'
 WHERE EXISTS (SELECT 1 FROM coco_hrim.hr_event h WHERE h.event_id = e.worker_event_identifier)
    OR e.worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker_event SET discard_reason = 'Austin or EKG worker event - HR is the acquired estate''s own'
 WHERE discard_reason IS NULL;

UPDATE incoming_event_distribution_status d SET discard_reason = 'Coco HR event distribution - tracked in HRIM'
 WHERE EXISTS (SELECT 1 FROM coco_hrim.hr_event h WHERE h.event_id = d.worker_event_identifier);
UPDATE incoming_event_distribution_status SET discard_reason = 'Austin or EKG event distribution - not a Coco HR event'
 WHERE discard_reason IS NULL;
