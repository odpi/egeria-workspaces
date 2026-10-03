-- Subscription: buc_opentext_ecm__personalised_manufacturing_schedule - OpenText ECM (Bucharest) receives Personalised Manufacturing Schedule
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (open batch)
-- Indexes the archived batch dossier of an EKG named-patient batch with its treatment order (category 3005 Index dosar
-- de lot, attribute 6 Comandă tratament), so the dossier can be retrieved from the hospital's order.  The patient
-- material receipt is held in SAP and is not archived here.  EKG batches whose dossier is not archived yet are discarded
-- (indexed when the signed EBR arrives), as are other companies' slots (Coco group data - EKG is not yet integrated).
WITH dosar AS (
  SELECT a.valstr AS batch FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2
)
UPDATE incoming_manufacturing_slot i
   SET discard_reason = (CASE WHEN i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'EKG batch dossier not yet archived - indexed when the signed EBR arrives'
                              ELSE 'Coco group data - EKG not yet integrated' END)
 WHERE NOT EXISTS (SELECT 1 FROM dosar WHERE dosar.batch = i.batch_identifier);
UPDATE incoming_manufacturing_slot SET discard_reason = 'slot has no treatment order'
 WHERE discard_reason IS NULL AND order_identifier IS NULL;
UPDATE incoming_patient_material_receipt r SET discard_reason = 'patient material receipts are held in SAP, not archived'
 WHERE EXISTS (SELECT 1 FROM incoming_manufacturing_slot s WHERE s.patient_pseudonym_identifier = r.patient_pseudonym_identifier
                AND s.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$');
UPDATE incoming_patient_material_receipt SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

WITH dosar AS (
  SELECT a.valstr AS batch, max(a.id) AS dataid
    FROM opentext_ecm.llattrdata a JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
   WHERE a.defid = 3001 AND a.attrid = 2 GROUP BY a.valstr
), v AS (
  SELECT DISTINCT d.dataid, i.order_identifier AS val
    FROM incoming_manufacturing_slot i JOIN dosar d ON d.batch = i.batch_identifier
   WHERE i.discard_reason IS NULL
     AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata x
                      WHERE x.id = d.dataid AND x.defid = 3005 AND x.attrid = 6 AND x.valstr = i.order_identifier)
)
INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT v.dataid, 3005, 6,
       coalesce((SELECT max(x.entrynum) FROM opentext_ecm.llattrdata x WHERE x.id = v.dataid AND x.defid = 3005 AND x.attrid = 6), 0)
         + row_number() OVER (PARTITION BY v.dataid ORDER BY v.val),
       v.val, NULL
  FROM v;
