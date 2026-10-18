-- Subscription: buc_ekg_wms__material_quarantine_dispositions - Warehouse Management System (WMS) (Bucharest) receives Material Quarantine Dispositions
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Goods Inventory Stock depends on it (release for use)
-- Keeps SAP's usage decision on each lot the WMS holds in quarantine, in the new import table imp_decizii_sap (E
-- eliberat / R respins, Bucharest local time), from which the storekeeper releases or rejects the lot; carantina itself
-- is not touched, so the quarantine extract is unchanged.  The quarantine records are the WMS's own and are discarded
-- (no feedback loop), as are Coco and Austin lots (EKG is not yet integrated).
UPDATE incoming_quarantine_record i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM ekg_wms.carantina c WHERE c.lot_intern = i.lot_identifier);
UPDATE incoming_quarantine_record SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_release_disposition i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM ekg_wms.carantina c WHERE c.lot_intern = i.lot_identifier);

INSERT INTO ekg_wms.imp_decizii_sap (lot_intern, data_decizie, decizie, nr_rezultat, data_exp, cant_elib, importat)
SELECT i.lot_identifier, (i.lot_disposition_timestamp AT TIME ZONE 'Europe/Bucharest'),
       (CASE WHEN i.lot_disposition_status LIKE 'released%' THEN 'E' ELSE 'R' END),
       i.test_result_identifier, i.lot_expiry_date, i.lot_released_quantity,
       (now() AT TIME ZONE 'Europe/Bucharest')::timestamp(0)
  FROM incoming_release_disposition i
 WHERE i.discard_reason IS NULL
ON CONFLICT (lot_intern, data_decizie) DO UPDATE
   SET decizie = EXCLUDED.decizie, nr_rezultat = EXCLUDED.nr_rezultat, data_exp = EXCLUDED.data_exp,
       cant_elib = EXCLUDED.cant_elib, importat = EXCLUDED.importat
 WHERE (ekg_wms.imp_decizii_sap.decizie, ekg_wms.imp_decizii_sap.nr_rezultat, ekg_wms.imp_decizii_sap.data_exp,
        ekg_wms.imp_decizii_sap.cant_elib)
       IS DISTINCT FROM (EXCLUDED.decizie, EXCLUDED.nr_rezultat, EXCLUDED.data_exp, EXCLUDED.cant_elib);
