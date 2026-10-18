-- Subscription: aus_workday_hcm__worker_lifecycle_events - Workday Human Capital Management (Austin) receives Worker Lifecycle Events
-- Destination: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Why it subscribes: Worker Master Data depends on it (worker event)
-- Keeps nothing: the Austin events are Workday's own staffing business process events (and the distribution status
-- of its own outbound integrations), while HRE- events are Coco HRIM's and EVT-RO- events are EKG's Workday tenant.
-- Every row is discarded as already held or as another estate's.

UPDATE incoming_worker_event i SET discard_reason = 'already held: Workday business process event'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.business_process_event e WHERE e.event_id = i.worker_event_identifier);
UPDATE incoming_worker_event SET discard_reason = 'other estate: not an Austin Workday event'
 WHERE discard_reason IS NULL;

UPDATE incoming_event_distribution_status i SET discard_reason = 'already held: Workday integration event'
 WHERE EXISTS (SELECT 1 FROM workday_hcm.business_process_event e WHERE e.event_id = i.worker_event_identifier);
UPDATE incoming_event_distribution_status SET discard_reason = 'other estate: not an Austin Workday event'
 WHERE discard_reason IS NULL;
