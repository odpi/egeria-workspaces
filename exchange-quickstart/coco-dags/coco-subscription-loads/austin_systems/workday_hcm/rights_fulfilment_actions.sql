-- Subscription: aus_workday_hcm__rights_fulfilment_actions - Workday Human Capital Management (Austin) receives Rights Fulfilment Actions
-- Destination: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Why it subscribes: Worker Master Data depends on it (locate employee data)
-- Keeps data subject requests about Austin workers (pseudonym resolved to the Workday employee ID) in the NEW
-- personal_data_request table, and the actions assigned to Workday itself in the NEW personal_data_request_task
-- table. Requests about customers, patients or other estates' workers, and actions for other systems, are discarded.

UPDATE incoming_fulfilment_request i SET discard_reason = 'data subject is not an Austin worker in Workday'
 WHERE NOT EXISTS (SELECT 1 FROM workday_hcm.worker w
                    WHERE 'WP-' || upper(substr(md5('AUS:' || w.employee_id), 1, 12)) = i.data_subject_identifier);

INSERT INTO workday_hcm.personal_data_request
       (request_id, employee_id, request_type, fulfilment_start_moment, systems_in_scope, request_status)
SELECT i.rights_request_identifier, w.employee_id, i.rights_request_type,
       i.rights_request_fulfilment_start_timestamp, i.rights_request_fulfilment_count, i.rights_request_fulfilment_status
  FROM incoming_fulfilment_request i
  JOIN workday_hcm.worker w ON 'WP-' || upper(substr(md5('AUS:' || w.employee_id), 1, 12)) = i.data_subject_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (request_id) DO UPDATE SET
       employee_id = EXCLUDED.employee_id, request_type = EXCLUDED.request_type,
       fulfilment_start_moment = EXCLUDED.fulfilment_start_moment, systems_in_scope = EXCLUDED.systems_in_scope,
       request_status = EXCLUDED.request_status;

UPDATE incoming_system_action i SET discard_reason = 'action for another system'
 WHERE i.system_identifier IS DISTINCT FROM 'SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301';
UPDATE incoming_system_action i SET discard_reason = 'request is not about an Austin worker'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM workday_hcm.personal_data_request r WHERE r.request_id = i.rights_request_identifier);

INSERT INTO workday_hcm.personal_data_request_task
       (task_id, request_id, action_type, requested_moment, completed_moment, task_status, retention_obligation)
SELECT i.system_action_identifier, i.rights_request_identifier, i.system_action_type,
       i.system_action_requested_timestamp, i.system_action_completed_timestamp, i.system_action_status,
       i.retention_obligation_identifier
  FROM incoming_system_action i
 WHERE i.discard_reason IS NULL
ON CONFLICT (task_id) DO UPDATE SET
       request_id = EXCLUDED.request_id, action_type = EXCLUDED.action_type,
       requested_moment = EXCLUDED.requested_moment, completed_moment = EXCLUDED.completed_moment,
       task_status = EXCLUDED.task_status, retention_obligation = EXCLUDED.retention_obligation;
