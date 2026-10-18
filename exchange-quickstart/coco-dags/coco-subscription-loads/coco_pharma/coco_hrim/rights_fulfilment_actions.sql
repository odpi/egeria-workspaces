-- Subscription: coco_hrim__rights_fulfilment_actions - Human Resources Information Manager (HRIM) (Coco core) receives Rights Fulfilment Actions
-- Destination: coco_pharma.coco_hrim (System::coco-hrim)
-- Why it subscribes: Worker Master Data depends on it (locate employee data)
-- Keeps the system actions addressed to HRIM (system identifier naming coco-hrim) in dsr_action (NEW), with the
-- request type and data subject of their request.  Discards actions for other systems, and requests with no
-- action for HRIM (customers, patients, or workers of the acquired estates, whose data HRIM does not hold).

UPDATE incoming_system_action SET discard_reason = 'action for another system'
 WHERE coalesce(system_identifier, '') NOT ILIKE '%coco-hrim%';

UPDATE incoming_fulfilment_request r SET discard_reason = 'no action for HRIM in this request'
 WHERE NOT EXISTS (SELECT 1 FROM incoming_system_action a
                    WHERE a.discard_reason IS NULL AND a.rights_request_identifier = r.rights_request_identifier)
   AND NOT EXISTS (SELECT 1 FROM coco_hrim.dsr_action d WHERE d.request_ref = r.rights_request_identifier);

INSERT INTO coco_hrim.dsr_action (action_ref, request_ref, subject_ref, request_typ, action_typ, requested_at, completed_at,
       action_sts, retention_ref)
SELECT a.system_action_identifier, a.rights_request_identifier, r.data_subject_identifier, r.rights_request_type,
       a.system_action_type, a.system_action_requested_timestamp, a.system_action_completed_timestamp,
       a.system_action_status, a.retention_obligation_identifier
  FROM incoming_system_action a
  LEFT JOIN incoming_fulfilment_request r ON r.rights_request_identifier = a.rights_request_identifier
 WHERE a.discard_reason IS NULL
ON CONFLICT (action_ref) DO UPDATE SET request_ref = EXCLUDED.request_ref,
       subject_ref = coalesce(EXCLUDED.subject_ref, coco_hrim.dsr_action.subject_ref),
       request_typ = coalesce(EXCLUDED.request_typ, coco_hrim.dsr_action.request_typ), action_typ = EXCLUDED.action_typ,
       requested_at = EXCLUDED.requested_at, completed_at = EXCLUDED.completed_at, action_sts = EXCLUDED.action_sts,
       retention_ref = EXCLUDED.retention_ref;

UPDATE coco_hrim.dsr_action d SET subject_ref = r.data_subject_identifier, request_typ = r.rights_request_type
  FROM incoming_fulfilment_request r
 WHERE r.discard_reason IS NULL AND r.rights_request_identifier = d.request_ref
   AND (d.subject_ref, d.request_typ) IS DISTINCT FROM (r.data_subject_identifier, r.rights_request_type);
