-- Subscription: buc_opentext_ecm__deviations_and_capas - OpenText ECM (Bucharest) receives Deviations And CAPAs
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (deviation disposition)
-- Indexes the archived batch dossier of an EKG batch with the deviations raised against it (category 3005 Index dosar
-- de lot, attribute 4 Abatere, multi-valued), so the dossier is found from the deviation number.  Investigations and
-- CAPAs stay in the QMS.  EKG deviations without an archived batch dossier are discarded, as are other companies'
-- deviations (Coco group data - EKG is not yet integrated).
WITH dosar AS (
  SELECT a.valstr AS batch FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2
)
UPDATE incoming_deviation i
   SET discard_reason = (CASE WHEN i.deviation_identifier LIKE 'DEV-RO-%' OR i.deviation_identifier LIKE 'TWD-%'
                                   OR i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'no archived EKG batch dossier for this deviation'
                              ELSE 'Coco group data - EKG not yet integrated' END)
 WHERE i.batch_identifier IS NULL OR NOT EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier);
UPDATE incoming_investigation SET discard_reason = 'investigation records stay in the QMS'
 WHERE deviation_identifier LIKE 'DEV-RO-%' OR deviation_identifier LIKE 'TWD-%';
UPDATE incoming_investigation SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_corrective_action SET discard_reason = 'CAPA records stay in the QMS'
 WHERE deviation_identifier LIKE 'DEV-RO-%' OR deviation_identifier LIKE 'TWD-%'
    OR corrective_action_identifier LIKE 'CAPA-RO-%' OR corrective_action_identifier LIKE 'TWC-%';
UPDATE incoming_corrective_action SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
), v AS (
  SELECT DISTINCT d.dataid, i.deviation_identifier AS val
    FROM incoming_deviation i JOIN dosar d ON d.batch = i.batch_identifier
   WHERE i.discard_reason IS NULL
     AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata x
                      WHERE x.id = d.dataid AND x.defid = 3005 AND x.attrid = 4 AND x.valstr = i.deviation_identifier)
)
INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT v.dataid, 3005, 4,
       coalesce((SELECT max(x.entrynum) FROM opentext_ecm.llattrdata x WHERE x.id = v.dataid AND x.defid = 3005 AND x.attrid = 4), 0)
         + row_number() OVER (PARTITION BY v.dataid ORDER BY v.val),
       v.val, NULL
  FROM v;
