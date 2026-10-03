-- Subscription: buc_ekg_wms__supplier_material_certificates - Warehouse Management System (WMS) (Bucharest) receives Supplier Material Certificates
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps the certificates (COA/COC, conform D/N) that EKG's suppliers (SAP vendor numbers 7xxxxx) sent with their
-- material, from LIMS and the ECM, in the new table certificate_furnizor, which the receipt check matches against
-- receptii.nr_certificat.  The certificate test values are not kept.  Coco and Austin certificates are discarded (EKG is
-- not yet integrated).
UPDATE incoming_certificate_of_analysis SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier IS NULL OR supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_certificate_test_result t SET discard_reason = 'WMS keeps the certificate verdict, not its test values'
 WHERE EXISTS (SELECT 1 FROM incoming_certificate_of_analysis c
                WHERE c.certificate_identifier = t.certificate_identifier AND c.discard_reason IS NULL)
    OR EXISTS (SELECT 1 FROM ekg_wms.certificate_furnizor f WHERE f.nr_certificat = t.certificate_identifier);
UPDATE incoming_certificate_test_result SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO ekg_wms.certificate_furnizor (nr_certificat, cod_furnizor, cod_art, lot, tip_cert, data_cert, conform, actualizat)
SELECT i.certificate_identifier, i.supplier_identifier, i.raw_material_code, i.lot_identifier,
       (CASE WHEN i.certificate_type = 'certificate of conformity' THEN 'COC' ELSE 'COA' END), i.certificate_date,
       (CASE WHEN i.certificate_conformity_flag THEN 'D' ELSE 'N' END), (now() AT TIME ZONE 'Europe/Bucharest')::timestamp(0)
  FROM incoming_certificate_of_analysis i
 WHERE i.discard_reason IS NULL
ON CONFLICT (nr_certificat) DO UPDATE
   SET cod_furnizor = EXCLUDED.cod_furnizor, cod_art = EXCLUDED.cod_art, lot = EXCLUDED.lot, tip_cert = EXCLUDED.tip_cert,
       data_cert = EXCLUDED.data_cert, conform = EXCLUDED.conform, actualizat = EXCLUDED.actualizat
 WHERE (ekg_wms.certificate_furnizor.cod_furnizor, ekg_wms.certificate_furnizor.cod_art, ekg_wms.certificate_furnizor.lot,
        ekg_wms.certificate_furnizor.tip_cert, ekg_wms.certificate_furnizor.data_cert, ekg_wms.certificate_furnizor.conform)
       IS DISTINCT FROM (EXCLUDED.cod_furnizor, EXCLUDED.cod_art, EXCLUDED.lot, EXCLUDED.tip_cert, EXCLUDED.data_cert,
                         EXCLUDED.conform);
