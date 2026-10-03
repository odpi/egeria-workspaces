-- Subscription: buc_workday_hcm__worker_lifecycle_events - Workday HCM (Bucharest) receives Worker Lifecycle Events
-- Destination: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Why it subscribes: Worker Master Data depends on it (worker event)
-- Workday raises EKG's joiner/mover/leaver events and distributes them, so every EKG event and distribution status is
-- already held here and is discarded (no feedback loop); Coco and Austin events are discarded too (EKG is not yet
-- integrated).  Nothing is written.
UPDATE incoming_worker_event i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.business_process_event e WHERE e.event_id = i.worker_event_identifier);
UPDATE incoming_event_distribution_status i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.business_process_event e WHERE e.event_id = i.worker_event_identifier);
UPDATE incoming_worker_event SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_event_distribution_status SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
