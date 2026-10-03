-- Subscription: buc_ekg_wms__serialised_product_identifiers - Warehouse Management System (WMS) (Bucharest) receives Serialised Product Identifiers
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Goods Inventory Stock depends on it (serialised stock)
-- Keeps the current state of each serialised pack of an EKG article (product code known in articole) in the new table
-- serii_ambalaj (zone = the RO10 warehouse code without the plant prefix); the pack event history is not kept.  Packs
-- of other products are discarded (Coco group data - EKG is not yet integrated).  The product has no source yet.
UPDATE incoming_serialised_identifier i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM ekg_wms.articole a WHERE a.cod_art = i.product_code);
UPDATE incoming_identifier_event e SET discard_reason = 'WMS keeps the pack''s current state, not its event history'
 WHERE EXISTS (SELECT 1 FROM incoming_serialised_identifier i
                WHERE i.pack_serial_number = e.pack_serial_number AND i.discard_reason IS NULL)
    OR EXISTS (SELECT 1 FROM ekg_wms.serii_ambalaj s WHERE s.nr_serie = e.pack_serial_number);
UPDATE incoming_identifier_event SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO ekg_wms.serii_ambalaj (nr_serie, cod_art, gtin, lot, data_exp, piata, stare, sscc_parinte, depozit, actualizat)
SELECT i.pack_serial_number, i.product_code, i.pack_code, i.batch_identifier, i.pack_expiry_date, i.market_code,
       coalesce(i.pack_current_status, 'necunoscut'), i.aggregation_parent_serial_number,
       (CASE WHEN i.warehouse_code LIKE 'RO10-%' THEN substr(i.warehouse_code, 6) END),
       (now() AT TIME ZONE 'Europe/Bucharest')::timestamp(0)
  FROM incoming_serialised_identifier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (nr_serie) DO UPDATE
   SET cod_art = EXCLUDED.cod_art, gtin = EXCLUDED.gtin, lot = EXCLUDED.lot, data_exp = EXCLUDED.data_exp,
       piata = EXCLUDED.piata, stare = EXCLUDED.stare, sscc_parinte = EXCLUDED.sscc_parinte, depozit = EXCLUDED.depozit,
       actualizat = EXCLUDED.actualizat
 WHERE (ekg_wms.serii_ambalaj.cod_art, ekg_wms.serii_ambalaj.gtin, ekg_wms.serii_ambalaj.lot, ekg_wms.serii_ambalaj.data_exp,
        ekg_wms.serii_ambalaj.piata, ekg_wms.serii_ambalaj.stare, ekg_wms.serii_ambalaj.sscc_parinte, ekg_wms.serii_ambalaj.depozit)
       IS DISTINCT FROM (EXCLUDED.cod_art, EXCLUDED.gtin, EXCLUDED.lot, EXCLUDED.data_exp, EXCLUDED.piata, EXCLUDED.stare,
                         EXCLUDED.sscc_parinte, EXCLUDED.depozit);
