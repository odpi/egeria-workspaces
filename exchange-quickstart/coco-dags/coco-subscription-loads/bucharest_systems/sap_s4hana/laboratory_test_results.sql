-- Subscription: buc_sap_s4hana__laboratory_test_results - SAP ERP S/4HANA (Bucharest) receives Laboratory Test Results
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Material Quarantine Dispositions depends on it (test results)
-- Records LabWare's results on EKG raw-material lots against the lot's goods-receipt inspection lot, in the new Z table
-- zekg_qm_lims (bewertg A/R), which the usage decision refers to (qave.zz_lims_result).  Samples are not SAP records,
-- release bulletins and batch certificates stay in LIMS, and results on finished batches are not used for goods-receipt
-- decisions; all are discarded, as are Coco and Austin results (EKG is not yet integrated).
UPDATE incoming_sample i SET discard_reason = 'SAP QM records results against the inspection lot, not samples'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.qals q WHERE q.mandt = '300' AND q.charg = i.lot_identifier)
    OR EXISTS (SELECT 1 FROM sap_s4hana.afpo p WHERE p.mandt = '300' AND p.charg = i.batch_identifier);
UPDATE incoming_sample SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_certificate_of_analysis i SET discard_reason = 'certificates are kept in LIMS'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.qals q WHERE q.mandt = '300' AND q.charg = i.lot_identifier)
    OR EXISTS (SELECT 1 FROM sap_s4hana.afpo p WHERE p.mandt = '300' AND p.charg = i.batch_identifier);
UPDATE incoming_certificate_of_analysis SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_test_result r SET discard_reason = 'result on a finished batch - not a goods-receipt inspection'
 WHERE EXISTS (SELECT 1 FROM incoming_sample s JOIN sap_s4hana.afpo p ON p.mandt = '300' AND p.charg = s.batch_identifier
                WHERE s.sample_identifier = r.sample_identifier);
UPDATE incoming_test_result r SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE r.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM incoming_sample s JOIN sap_s4hana.qals q ON q.mandt = '300' AND q.art = '01' AND q.charg = s.lot_identifier
                    WHERE s.sample_identifier = r.sample_identifier);

WITH lot AS (
  SELECT DISTINCT ON (s.sample_identifier) s.sample_identifier, q.prueflos
    FROM incoming_sample s
    JOIN sap_s4hana.qals q ON q.mandt = '300' AND q.art = '01' AND q.charg = s.lot_identifier
   ORDER BY s.sample_identifier, q.prueflos DESC
)
INSERT INTO sap_s4hana.zekg_qm_lims (mandt, prueflos, lims_result, verwmerkm, messwert, meinh, toleranzun, toleranzob,
                                     bewertg, pruefdatuv, pruefzeit, pruefer)
SELECT '300', l.prueflos, r.test_result_identifier, coalesce(r.test_code, '?'), r.test_value, r.test_unit,
       r.specification_minimum_value, r.specification_maximum_value, (CASE WHEN r.test_conformity_flag THEN 'A' ELSE 'R' END),
       to_char(r.test_completed_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'), to_char(r.test_completed_timestamp AT TIME ZONE 'UTC', 'HH24MISS'),
       upper(left(r.test_analyst_identifier, 12))
  FROM incoming_test_result r
  JOIN lot l ON l.sample_identifier = r.sample_identifier
 WHERE r.discard_reason IS NULL
ON CONFLICT (mandt, prueflos, lims_result) DO UPDATE
   SET verwmerkm = EXCLUDED.verwmerkm, messwert = EXCLUDED.messwert, meinh = EXCLUDED.meinh, toleranzun = EXCLUDED.toleranzun,
       toleranzob = EXCLUDED.toleranzob, bewertg = EXCLUDED.bewertg, pruefdatuv = EXCLUDED.pruefdatuv,
       pruefzeit = EXCLUDED.pruefzeit, pruefer = EXCLUDED.pruefer;
