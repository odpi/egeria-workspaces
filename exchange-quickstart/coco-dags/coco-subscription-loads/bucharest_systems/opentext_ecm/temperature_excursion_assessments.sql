-- Subscription: buc_opentext_ecm__temperature_excursion_assessments - OpenText ECM (Bucharest) receives Temperature Excursion Assessments
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (disposition recorded)
-- Indexes the archived batch dossier of an EKG batch with the temperature excursion assessments made on it (category
-- 3005 Index dosar de lot, attribute 7, valdate = assessment date).  EKG excursions without an archived batch dossier
-- are discarded, as are other companies' (Coco group data - EKG is not yet integrated).  The product has no source yet.
WITH dosar AS (
  SELECT a.valstr AS batch FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2
)
UPDATE incoming_excursion_assessment i
   SET discard_reason = (CASE WHEN i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$' OR i.shipment_identifier LIKE 'EXP-%'
                              THEN 'no archived EKG batch dossier for this excursion'
                              ELSE 'Coco group data - EKG not yet integrated' END)
 WHERE i.batch_identifier IS NULL OR NOT EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier);

WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
), v AS (
  SELECT DISTINCT ON (d.dataid, i.excursion_identifier) d.dataid, i.excursion_identifier AS val,
         (i.excursion_assessment_timestamp AT TIME ZONE 'Europe/Bucharest')::date AS assessed
    FROM incoming_excursion_assessment i JOIN dosar d ON d.batch = i.batch_identifier
   WHERE i.discard_reason IS NULL
     AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata x
                      WHERE x.id = d.dataid AND x.defid = 3005 AND x.attrid = 7 AND x.valstr = i.excursion_identifier)
   ORDER BY d.dataid, i.excursion_identifier
)
INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT v.dataid, 3005, 7,
       coalesce((SELECT max(x.entrynum) FROM opentext_ecm.llattrdata x WHERE x.id = v.dataid AND x.defid = 3005 AND x.attrid = 7), 0)
         + row_number() OVER (PARTITION BY v.dataid ORDER BY v.val),
       v.val, v.assessed
  FROM v;
