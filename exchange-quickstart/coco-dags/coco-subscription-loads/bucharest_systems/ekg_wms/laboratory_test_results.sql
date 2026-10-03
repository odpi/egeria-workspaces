-- Subscription: buc_ekg_wms__laboratory_test_results - Warehouse Management System (WMS) (Bucharest) receives Laboratory Test Results
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Material Quarantine Dispositions depends on it (test results)
-- Keeps the LIMS release bulletin (BA-) of each lot the WMS holds in quarantine, in the new table buletine_analiza
-- (conform D/N), which the storekeeper checks before releasing the lot.  Samples are already referenced by the
-- quarantine record (nr_proba) and individual results are not kept; finished-batch samples and certificates are not WMS
-- business.  Coco and Austin results are discarded (EKG is not yet integrated).
UPDATE incoming_sample i SET discard_reason = 'sample already referenced by the quarantine record'
 WHERE EXISTS (SELECT 1 FROM ekg_wms.carantina c WHERE c.nr_proba = i.sample_identifier OR c.lot_intern = i.lot_identifier);
UPDATE incoming_sample SET discard_reason = 'batch sample - the WMS keeps only release bulletins of received lots'
 WHERE discard_reason IS NULL AND batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_sample SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

UPDATE incoming_test_result r SET discard_reason = 'WMS keeps the release bulletin, not individual results'
 WHERE EXISTS (SELECT 1 FROM ekg_wms.carantina c WHERE c.nr_proba = r.sample_identifier)
    OR EXISTS (SELECT 1 FROM incoming_sample s WHERE s.sample_identifier = r.sample_identifier
                AND s.discard_reason <> 'Coco group data - EKG not yet integrated');
UPDATE incoming_test_result SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

UPDATE incoming_certificate_of_analysis SET discard_reason = 'batch certificate - the WMS releases received lots only'
 WHERE lot_identifier IS NULL AND batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$';
UPDATE incoming_certificate_of_analysis i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM ekg_wms.carantina c WHERE c.lot_intern = i.lot_identifier);

INSERT INTO ekg_wms.buletine_analiza (nr_buletin, lot_intern, data_bul, conform, aprobat_de, actualizat)
SELECT i.certificate_identifier, i.lot_identifier, i.certificate_date,
       (CASE WHEN i.certificate_conformity_flag THEN 'D' ELSE 'N' END), i.certificate_approver_identifier,
       (now() AT TIME ZONE 'Europe/Bucharest')::timestamp(0)
  FROM incoming_certificate_of_analysis i
 WHERE i.discard_reason IS NULL
ON CONFLICT (nr_buletin) DO UPDATE
   SET lot_intern = EXCLUDED.lot_intern, data_bul = EXCLUDED.data_bul, conform = EXCLUDED.conform,
       aprobat_de = EXCLUDED.aprobat_de, actualizat = EXCLUDED.actualizat
 WHERE (ekg_wms.buletine_analiza.lot_intern, ekg_wms.buletine_analiza.data_bul, ekg_wms.buletine_analiza.conform,
        ekg_wms.buletine_analiza.aprobat_de)
       IS DISTINCT FROM (EXCLUDED.lot_intern, EXCLUDED.data_bul, EXCLUDED.conform, EXCLUDED.aprobat_de);
