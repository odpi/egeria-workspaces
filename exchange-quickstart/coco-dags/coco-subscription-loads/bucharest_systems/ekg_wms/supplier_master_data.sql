-- Subscription: buc_ekg_wms__supplier_master_data - Warehouse Management System (WMS) (Bucharest) receives Supplier Master Data
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Goods Receipts depends on it (approved supplier)
-- Keeps EKG's SAP vendors (vendor numbers 7xxxxx of client 300) in the new table furnizori - name, country, approved
-- D/N and status - so the storekeeper can refuse a delivery from a supplier that is not approved.  Screening results
-- and bank details are not WMS business.  Coco and Austin suppliers are discarded (EKG is not yet integrated).
UPDATE incoming_supplier SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_risk_status SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_risk_status SET discard_reason = 'supplier screening is not kept in the WMS' WHERE discard_reason IS NULL;
UPDATE incoming_supplier_payment_details SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not kept in the WMS' WHERE discard_reason IS NULL;

INSERT INTO ekg_wms.furnizori (cod_furnizor, denumire, tara, aprobat, data_aprob, stare, actualizat)
SELECT i.supplier_identifier, coalesce(i.supplier_name, i.supplier_identifier), i.supplier_country,
       (CASE WHEN i.supplier_approved_flag THEN 'D' ELSE 'N' END), i.supplier_approved_date,
       coalesce(i.supplier_current_status, 'active'), (now() AT TIME ZONE 'Europe/Bucharest')::timestamp(0)
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (cod_furnizor) DO UPDATE
   SET denumire = EXCLUDED.denumire, tara = EXCLUDED.tara, aprobat = EXCLUDED.aprobat, data_aprob = EXCLUDED.data_aprob,
       stare = EXCLUDED.stare, actualizat = EXCLUDED.actualizat
 WHERE (ekg_wms.furnizori.denumire, ekg_wms.furnizori.tara, ekg_wms.furnizori.aprobat, ekg_wms.furnizori.data_aprob,
        ekg_wms.furnizori.stare)
       IS DISTINCT FROM (EXCLUDED.denumire, EXCLUDED.tara, EXCLUDED.aprobat, EXCLUDED.data_aprob, EXCLUDED.stare);
