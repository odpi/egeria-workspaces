-- Subscription: coco_inventory__serialised_product_identifiers - Coco Inventory (Coco core) receives Serialised Product Identifiers
-- Destination: coco_pharma.coco_inventory (System::coco-inventory)
-- Why it subscribes: Goods Inventory Stock depends on it (serialised stock)
-- Keeps serialised packs located at Coco's own locations (Winchester, Edmonton, Kansas City) and their events in
-- inv_serial and inv_serial_evt (both NEW), so serialised stock can be reconciled with inv_bal.  Discards packs
-- elsewhere (Austin site, Austin's and EKG's warehouses, or no location).  No system supplies this product yet.

UPDATE incoming_serialised_identifier s SET discard_reason = 'pack not at a Coco location'
 WHERE s.warehouse_code IS NULL OR NOT (s.warehouse_code IN (SELECT loc_cd FROM coco_inventory.inv_loc) OR s.warehouse_code ~ '^(WIN|EDM|KC)-');

INSERT INTO coco_inventory.inv_serial (serial_no, item_cd, pack_cd, lot_no, exp_dt, mkt, serial_sts, parent_serial, loc_cd)
SELECT s.pack_serial_number, s.product_code, s.pack_code, s.batch_identifier, s.pack_expiry_date, s.market_code,
       s.pack_current_status, s.aggregation_parent_serial_number, s.warehouse_code
  FROM incoming_serialised_identifier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (serial_no) DO UPDATE SET item_cd = EXCLUDED.item_cd, pack_cd = EXCLUDED.pack_cd, lot_no = EXCLUDED.lot_no,
       exp_dt = EXCLUDED.exp_dt, mkt = EXCLUDED.mkt, serial_sts = EXCLUDED.serial_sts, parent_serial = EXCLUDED.parent_serial,
       loc_cd = EXCLUDED.loc_cd;

UPDATE incoming_identifier_event e SET discard_reason = 'event of a pack not at a Coco location'
 WHERE NOT EXISTS (SELECT 1 FROM coco_inventory.inv_serial s WHERE s.serial_no = e.pack_serial_number);

INSERT INTO coco_inventory.inv_serial_evt (serial_no, evt_ts, evt_typ, src_sys, alert_ref)
SELECT e.pack_serial_number, e.pack_event_timestamp, e.pack_event_type, e.system_identifier, e.alert_identifier
  FROM incoming_identifier_event e
 WHERE e.discard_reason IS NULL
ON CONFLICT (serial_no, evt_ts) DO UPDATE SET evt_typ = EXCLUDED.evt_typ, src_sys = EXCLUDED.src_sys, alert_ref = EXCLUDED.alert_ref;
