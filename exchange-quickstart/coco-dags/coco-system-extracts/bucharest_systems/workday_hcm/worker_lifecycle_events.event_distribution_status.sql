-- Extract: Workday HCM (Bucharest) -> Worker Lifecycle Events / event_distribution_status
-- Source: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Target: coco_data_hub.worker_lifecycle_events.event_distribution_status
-- integration_event grouped per event and target (retries collapsed: first send, last successful completion);
-- integration system mapped to the target system's qualified name.
SELECT
  i.business_process_event_id::varchar(40) AS worker_event_identifier,
  (CASE i.integration_system_id
     WHEN 'INT_RO01_M365_Graph_Provisioning' THEN 'SoftwareServer::SYS-007::Microsoft 365'
     WHEN 'INT_RO02_Kronos_Employee_Export' THEN 'SoftwareServer::SYS-023::Kronos Workforce'
     ELSE i.integration_system_id END)::varchar(60) AS system_identifier,
  min(i.initiated_moment) AS worker_event_sent_timestamp,
  bool_or(i.status = 'Completed') AS worker_event_applied_flag,
  max(i.completed_moment) FILTER (WHERE i.status = 'Completed') AS worker_event_applied_timestamp
FROM workday_hcm.integration_event i
GROUP BY i.business_process_event_id, i.integration_system_id
