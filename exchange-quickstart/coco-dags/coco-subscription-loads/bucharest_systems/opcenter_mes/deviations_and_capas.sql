-- Subscription: buc_opcenter_mes__deviations_and_capas - Siemens Opcenter MES (Bucharest) receives Deviations And CAPAs
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Electronic Batch Records depends on it (deviation disposition)
-- Keeps the deviations raised in Veeva QMS or Trackwise against an EKG batch of this MES in the new table
-- extqualityevent, with the investigation's disposition, so a batch with an open event cannot be closed and the EBR
-- shows the disposition (the EBR's own DEVIATION section, an extract source, is not touched).  CAPAs stay in the QMS.
-- EKG events with no MES batch are discarded, as are other companies' events (Coco group data - EKG not yet integrated).
UPDATE incoming_deviation i SET discard_reason = 'no MES batch - not relevant to execution'
 WHERE (i.deviation_identifier LIKE 'DEV-RO-%' OR i.deviation_identifier LIKE 'TWD-%')
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_deviation i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);

INSERT INTO opcenter_mes.extqualityevent (eventname, eventtype, containerid, sourcesystem, raiseddate, severity, eventstatus,
                                          description, lastchangedate)
SELECT i.deviation_identifier, 'Deviation', c.containerid,
       (CASE WHEN i.deviation_identifier LIKE 'TWD-%' THEN 'TRACKWISE' ELSE 'VEEVA_QMS' END),
       i.deviation_raised_timestamp, i.deviation_severity, i.deviation_current_status, i.deviation_description, now()
  FROM incoming_deviation i
  JOIN opcenter_mes.container c ON c.containername = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (eventname) DO UPDATE
   SET containerid = EXCLUDED.containerid, sourcesystem = EXCLUDED.sourcesystem, raiseddate = EXCLUDED.raiseddate,
       severity = EXCLUDED.severity, eventstatus = EXCLUDED.eventstatus, description = EXCLUDED.description, lastchangedate = now()
 WHERE (opcenter_mes.extqualityevent.containerid, opcenter_mes.extqualityevent.sourcesystem, opcenter_mes.extqualityevent.raiseddate,
        opcenter_mes.extqualityevent.severity, opcenter_mes.extqualityevent.eventstatus, opcenter_mes.extqualityevent.description)
       IS DISTINCT FROM (EXCLUDED.containerid, EXCLUDED.sourcesystem, EXCLUDED.raiseddate, EXCLUDED.severity,
                         EXCLUDED.eventstatus, EXCLUDED.description);

UPDATE incoming_investigation i SET discard_reason = 'no MES batch - not relevant to execution'
 WHERE (i.deviation_identifier LIKE 'DEV-RO-%' OR i.deviation_identifier LIKE 'TWD-%')
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.extqualityevent q WHERE q.eventname = i.deviation_identifier);
UPDATE incoming_investigation i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.extqualityevent q WHERE q.eventname = i.deviation_identifier);
UPDATE opcenter_mes.extqualityevent q
   SET dispositionstatus = i.deviation_disposition_status,
       dispositiondate = (i.deviation_investigation_completed_date::timestamp AT TIME ZONE 'UTC'), lastchangedate = now()
  FROM incoming_investigation i
 WHERE i.discard_reason IS NULL AND q.eventname = i.deviation_identifier
   AND (q.dispositionstatus, q.dispositiondate) IS DISTINCT FROM
       (i.deviation_disposition_status, (i.deviation_investigation_completed_date::timestamp AT TIME ZONE 'UTC'));

UPDATE incoming_corrective_action SET discard_reason = 'CAPAs are managed in the QMS'
 WHERE deviation_identifier LIKE 'DEV-RO-%' OR deviation_identifier LIKE 'TWD-%'
    OR corrective_action_identifier LIKE 'CAPA-RO-%' OR corrective_action_identifier LIKE 'TWC-%';
UPDATE incoming_corrective_action SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
