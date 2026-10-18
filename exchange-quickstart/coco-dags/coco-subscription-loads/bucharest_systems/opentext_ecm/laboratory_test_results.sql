-- Subscription: buc_opentext_ecm__laboratory_test_results - OpenText ECM (Bucharest) receives Laboratory Test Results
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (finished product results)
-- Indexes the archived batch dossier of an EKG batch with its certificate of analysis (category 3005 Index dosar de
-- lot, attribute 5, valdate = certificate date).  Samples and individual results are summarised by the certificate,
-- and raw-material release bulletins are not part of a batch dossier, so they are discarded; EKG batches whose dossier
-- is not archived yet are discarded, as are other companies' results (Coco group data - EKG is not yet integrated).
UPDATE incoming_sample SET discard_reason = 'results are summarised in the certificate of analysis'
 WHERE batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$' OR lot_identifier ~ '^MP[0-9]{2}-[0-9]{4}$';
UPDATE incoming_sample SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_test_result r SET discard_reason = 'results are summarised in the certificate of analysis'
 WHERE EXISTS (SELECT 1 FROM incoming_sample s WHERE s.sample_identifier = r.sample_identifier
                AND s.discard_reason = 'results are summarised in the certificate of analysis');
UPDATE incoming_test_result SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_certificate_of_analysis SET discard_reason = 'raw material release bulletin - not part of a batch dossier'
 WHERE batch_identifier IS NULL AND lot_identifier ~ '^MP[0-9]{2}-[0-9]{4}$';
WITH dosar AS (
  SELECT a.valstr AS batch FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2
)
UPDATE incoming_certificate_of_analysis i
   SET discard_reason = (CASE WHEN i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'EKG batch dossier not yet archived - indexed when the signed EBR arrives'
                              ELSE 'Coco group data - EKG not yet integrated' END)
 WHERE i.discard_reason IS NULL
   AND (i.batch_identifier IS NULL OR NOT EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier));

WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
), v AS (
  SELECT DISTINCT ON (d.dataid, i.certificate_identifier) d.dataid, i.certificate_identifier AS val, i.certificate_date
    FROM incoming_certificate_of_analysis i JOIN dosar d ON d.batch = i.batch_identifier
   WHERE i.discard_reason IS NULL
     AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata x
                      WHERE x.id = d.dataid AND x.defid = 3005 AND x.attrid = 5 AND x.valstr = i.certificate_identifier)
   ORDER BY d.dataid, i.certificate_identifier
)
INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT v.dataid, 3005, 5,
       coalesce((SELECT max(x.entrynum) FROM opentext_ecm.llattrdata x WHERE x.id = v.dataid AND x.defid = 3005 AND x.attrid = 5), 0)
         + row_number() OVER (PARTITION BY v.dataid ORDER BY v.val),
       v.val, v.certificate_date
  FROM v;
