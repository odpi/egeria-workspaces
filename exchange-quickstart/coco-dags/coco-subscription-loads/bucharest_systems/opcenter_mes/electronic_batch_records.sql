-- Subscription: buc_opcenter_mes__electronic_batch_records - Siemens Opcenter MES (Bucharest) receives Electronic Batch Records
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Batch Certification Decisions depends on it (batch record for review)
-- Opcenter is the source of EKG's electronic batch records (ebrheader, ebrsectionref, batchreleasehistory), so those are
-- discarded as already held (no feedback loop).  The one thing it keeps is the ECM's archive reference: the OpenText
-- node of the signed batch record is set as ebrheader.archivedocref of the batch, which no extract reads.  Other
-- batches are discarded as Coco group data (EKG is not yet integrated).
UPDATE incoming_batch_record i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_release_authorisation i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_batch_record_section i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE i.system_identifier IS DISTINCT FROM 'SoftwareServer::SYS-024::OpenText ECM'
   AND EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_batch_record_section i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.container c JOIN opcenter_mes.ebrheader h ON h.containerid = c.containerid
                    WHERE c.containername = i.batch_identifier);
UPDATE incoming_batch_record SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_release_authorisation SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

WITH a AS (
  SELECT DISTINCT ON (i.batch_identifier) i.batch_identifier, i.batch_record_section_reference_identifier
    FROM incoming_batch_record_section i WHERE i.discard_reason IS NULL
   ORDER BY i.batch_identifier, i.batch_record_section_received_timestamp DESC NULLS LAST, i.batch_record_section_reference_identifier DESC
)
UPDATE opcenter_mes.ebrheader h
   SET archivedocref = a.batch_record_section_reference_identifier
  FROM a
  JOIN opcenter_mes.container c ON c.containername = a.batch_identifier
 WHERE h.containerid = c.containerid
   AND h.archivedocref IS DISTINCT FROM a.batch_record_section_reference_identifier;
