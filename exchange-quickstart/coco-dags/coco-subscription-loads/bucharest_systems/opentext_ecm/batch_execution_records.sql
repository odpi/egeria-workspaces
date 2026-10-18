-- Subscription: buc_opentext_ecm__batch_execution_records - OpenText ECM (Bucharest) receives Batch Execution Records
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (execution record)
-- Indexes the archived batch dossier of each EKG batch (the document node carrying category 3001 Dosar de lot with the
-- batch number) with the raw-material lots and the equipment the batch used, as multi-valued attributes of the new
-- category 3005 Index dosar de lot (llattrdata defid 3005, attributes 2 and 3), so the dossiers can be found by lot or
-- equipment.  The steps themselves are in the signed batch record PDF.  EKG batches whose dossier is not archived yet
-- are discarded (indexed when the signed EBR arrives), as are other companies' batches (Coco group data).
WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
)
UPDATE incoming_execution_step i
   SET discard_reason = (CASE WHEN EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier)
                              THEN 'steps are in the signed batch record PDF'
                              WHEN i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'EKG batch dossier not yet archived - indexed when the signed EBR arrives'
                              ELSE 'Coco group data - EKG not yet integrated' END);
WITH dosar AS (
  SELECT a.valstr AS batch FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2
)
UPDATE incoming_material_usage i
   SET discard_reason = (CASE WHEN i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'EKG batch dossier not yet archived - indexed when the signed EBR arrives'
                              ELSE 'Coco group data - EKG not yet integrated' END)
 WHERE NOT EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier);
WITH dosar AS (
  SELECT a.valstr AS batch FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2
)
UPDATE incoming_equipment_usage i
   SET discard_reason = (CASE WHEN i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'EKG batch dossier not yet archived - indexed when the signed EBR arrives'
                              ELSE 'Coco group data - EKG not yet integrated' END)
 WHERE NOT EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier);

WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
), v AS (
  SELECT DISTINCT d.dataid, i.lot_identifier AS val
    FROM incoming_material_usage i JOIN dosar d ON d.batch = i.batch_identifier
   WHERE i.discard_reason IS NULL AND i.lot_identifier IS NOT NULL
     AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata x
                      WHERE x.id = d.dataid AND x.defid = 3005 AND x.attrid = 2 AND x.valstr = i.lot_identifier)
)
INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT v.dataid, 3005, 2,
       coalesce((SELECT max(x.entrynum) FROM opentext_ecm.llattrdata x WHERE x.id = v.dataid AND x.defid = 3005 AND x.attrid = 2), 0)
         + row_number() OVER (PARTITION BY v.dataid ORDER BY v.val),
       v.val, NULL
  FROM v;

WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
), v AS (
  SELECT DISTINCT d.dataid, i.equipment_identifier AS val
    FROM incoming_equipment_usage i JOIN dosar d ON d.batch = i.batch_identifier
   WHERE i.discard_reason IS NULL AND i.equipment_identifier IS NOT NULL
     AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata x
                      WHERE x.id = d.dataid AND x.defid = 3005 AND x.attrid = 3 AND x.valstr = i.equipment_identifier)
)
INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT v.dataid, 3005, 3,
       coalesce((SELECT max(x.entrynum) FROM opentext_ecm.llattrdata x WHERE x.id = v.dataid AND x.defid = 3005 AND x.attrid = 3), 0)
         + row_number() OVER (PARTITION BY v.dataid ORDER BY v.val),
       v.val, NULL
  FROM v;
