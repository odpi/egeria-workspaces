-- Extract: Workday Human Capital Management (Austin) -> Worker Lifecycle Events / event_distribution_status
-- Source: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Target: coco_data_hub.worker_lifecycle_events.event_distribution_status
-- integration_event grouped per event and target (retries collapsed: first send, last successful completion);
-- integration system mapped to the target system's qualified name.
SELECT
  i.business_process_event_id::varchar(40) AS worker_event_identifier,
  (CASE i.integration_system_id
     WHEN 'INT001_Entra_ID_User_Provisioning' THEN 'SoftwareServer::AUS-SYS-032::SN-AAD-AU-20200601'
     WHEN 'INT004_Cornerstone_User_Feed' THEN 'SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110'
     WHEN 'INT006_UKG_Dimensions_Employee_Export' THEN 'SoftwareServer::AUS-SYS-021::SN-TNA-AU-20190305'
     ELSE i.integration_system_id END)::varchar(60) AS system_identifier,
  min(i.initiated_moment) AS worker_event_sent_timestamp,
  bool_or(i.status = 'Completed') AS worker_event_applied_flag,
  max(i.completed_moment) FILTER (WHERE i.status = 'Completed') AS worker_event_applied_timestamp
FROM workday_hcm.integration_event i
GROUP BY i.business_process_event_id, i.integration_system_id
