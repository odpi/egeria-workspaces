-- Subscription: coco_aus_inventory__serialised_product_identifiers - Austin Inventory (Coco core) receives Serialised Product Identifiers
-- Destination: coco_pharma.aus_inventory (System::aus-inventory)
-- Why it subscribes: Goods Inventory Stock depends on it (serialised stock)
-- Keeps serialised packs located at Austin Inventory's locations (AUS- location ids) and their events in serial_no
-- and serial_event (both NEW, expiry as text MM/DD/YYYY), so serialised stock can be reconciled with on_hand.
-- Discards packs elsewhere, including Austin's own SAP warehouses.  No system supplies this product yet.

UPDATE incoming_serialised_identifier SET discard_reason = 'pack not at an Austin Inventory location'
 WHERE coalesce(warehouse_code, '') NOT LIKE 'AUS-%';

INSERT INTO aus_inventory.serial_no (serial_no, item_no, pack_code, lot_no, expiry, market, serial_status, parent_serial, loc_id)
SELECT s.pack_serial_number, lower(s.product_code), s.pack_code, s.batch_identifier, to_char(s.pack_expiry_date, 'MM/DD/YYYY'),
       s.market_code, upper(s.pack_current_status), s.aggregation_parent_serial_number, s.warehouse_code
  FROM incoming_serialised_identifier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (serial_no) DO UPDATE SET item_no = EXCLUDED.item_no, pack_code = EXCLUDED.pack_code, lot_no = EXCLUDED.lot_no,
       expiry = EXCLUDED.expiry, market = EXCLUDED.market, serial_status = EXCLUDED.serial_status,
       parent_serial = EXCLUDED.parent_serial, loc_id = EXCLUDED.loc_id;

UPDATE incoming_identifier_event e SET discard_reason = 'event of a pack not at an Austin Inventory location'
 WHERE NOT EXISTS (SELECT 1 FROM aus_inventory.serial_no s WHERE s.serial_no = e.pack_serial_number);

INSERT INTO aus_inventory.serial_event (serial_no, event_utc, event_type, source_system, alert_no)
SELECT e.pack_serial_number, e.pack_event_timestamp, upper(e.pack_event_type), e.system_identifier, e.alert_identifier
  FROM incoming_identifier_event e
 WHERE e.discard_reason IS NULL
ON CONFLICT (serial_no, event_utc) DO UPDATE SET event_type = EXCLUDED.event_type, source_system = EXCLUDED.source_system,
       alert_no = EXCLUDED.alert_no;
