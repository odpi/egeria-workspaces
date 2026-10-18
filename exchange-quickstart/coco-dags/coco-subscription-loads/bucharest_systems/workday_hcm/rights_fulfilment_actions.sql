-- Subscription: buc_workday_hcm__rights_fulfilment_actions - Workday HCM (Bucharest) receives Rights Fulfilment Actions
-- Destination: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Why it subscribes: Worker Master Data depends on it (locate employee data)
-- Keeps data subject requests about EKG workers (subject pseudonym matched to a Workday employee through the EKG
-- pseudonym rule) in data_privacy_request, with the task asked of Workday itself (the latest system action naming
-- Workday HCM).  Actions for other systems or processors are discarded, as are requests about anyone who is not an EKG
-- worker (Coco group data subjects - EKG is not yet integrated).
UPDATE incoming_fulfilment_request i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM workday_hcm.worker w
                    WHERE 'WP-' || upper(substr(md5('EKG:' || w.employee_id), 1, 12)) = i.data_subject_identifier);
UPDATE incoming_system_action a SET discard_reason = 'action for another system or processor'
 WHERE a.system_identifier IS DISTINCT FROM 'SoftwareServer::SYS-013::Workday HCM';
UPDATE incoming_system_action a SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE a.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM incoming_fulfilment_request r
                    WHERE r.rights_request_identifier = a.rights_request_identifier AND r.discard_reason IS NULL)
   AND NOT EXISTS (SELECT 1 FROM workday_hcm.data_privacy_request d WHERE d.request_id = a.rights_request_identifier);

INSERT INTO workday_hcm.data_privacy_request (request_id, employee_id, request_type, received_moment, request_status, last_updated)
SELECT i.rights_request_identifier, w.employee_id, i.rights_request_type, i.rights_request_fulfilment_start_timestamp,
       i.rights_request_fulfilment_status, now()
  FROM incoming_fulfilment_request i
  JOIN workday_hcm.worker w ON 'WP-' || upper(substr(md5('EKG:' || w.employee_id), 1, 12)) = i.data_subject_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (request_id) DO UPDATE
   SET employee_id = EXCLUDED.employee_id, request_type = EXCLUDED.request_type,
       received_moment = EXCLUDED.received_moment, request_status = EXCLUDED.request_status, last_updated = now()
 WHERE (workday_hcm.data_privacy_request.employee_id, workday_hcm.data_privacy_request.request_type,
        workday_hcm.data_privacy_request.received_moment, workday_hcm.data_privacy_request.request_status)
       IS DISTINCT FROM (EXCLUDED.employee_id, EXCLUDED.request_type, EXCLUDED.received_moment, EXCLUDED.request_status);

WITH t AS (
  SELECT DISTINCT ON (a.rights_request_identifier) a.*
    FROM incoming_system_action a WHERE a.discard_reason IS NULL
   ORDER BY a.rights_request_identifier, a.system_action_requested_timestamp DESC NULLS LAST, a.system_action_identifier DESC
)
UPDATE workday_hcm.data_privacy_request d
   SET task_id = t.system_action_identifier, task_type = t.system_action_type, task_status = t.system_action_status,
       task_completed_moment = t.system_action_completed_timestamp, last_updated = now()
  FROM t
 WHERE d.request_id = t.rights_request_identifier
   AND (d.task_id, d.task_type, d.task_status, d.task_completed_moment)
       IS DISTINCT FROM (t.system_action_identifier, t.system_action_type, t.system_action_status, t.system_action_completed_timestamp);
