-- Subscription: aus_manhattan_wms__serialised_product_identifiers - Manhattan WMS (Austin) receives Serialised Product Identifiers
-- Destination: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Why it subscribes: Goods Inventory Stock depends on it (serialised stock)
-- Keeps the serial numbers of packs of Austin-made products from Austin batches (AU- products and the Coco products
-- made at Austin) in the NEW srl_nbr_track table, with their pack events in NEW srl_nbr_track_event, so pick and
-- ship can verify serialised stock. Serials of other products or estates' batches, and events for serials it does
-- not track, are discarded.

UPDATE incoming_serialised_identifier i SET discard_reason = 'other estate: not an Austin-made pack'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000')) OR i.batch_identifier !~ '^A[0-9]{2}-';
INSERT INTO manhattan_wms.srl_nbr_track
       (srl_nbr, item_name, gtin, batch_nbr, expire_date, market, srl_status, parent_srl_nbr, whse)
SELECT i.pack_serial_number, i.product_code, i.pack_code, i.batch_identifier, i.pack_expiry_date, i.market_code,
       i.pack_current_status, i.aggregation_parent_serial_number, i.warehouse_code
  FROM incoming_serialised_identifier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (srl_nbr) DO UPDATE SET
       item_name = EXCLUDED.item_name, gtin = EXCLUDED.gtin, batch_nbr = EXCLUDED.batch_nbr,
       expire_date = EXCLUDED.expire_date, market = EXCLUDED.market, srl_status = EXCLUDED.srl_status,
       parent_srl_nbr = EXCLUDED.parent_srl_nbr, whse = EXCLUDED.whse;

UPDATE incoming_identifier_event i SET discard_reason = 'serial number not tracked by the WMS'
 WHERE NOT EXISTS (SELECT 1 FROM manhattan_wms.srl_nbr_track t WHERE t.srl_nbr = i.pack_serial_number);
INSERT INTO manhattan_wms.srl_nbr_track_event (srl_nbr, event_dttm, event_type, source_system, alert_id)
SELECT i.pack_serial_number, i.pack_event_timestamp, i.pack_event_type, i.system_identifier, i.alert_identifier
  FROM incoming_identifier_event i
 WHERE i.discard_reason IS NULL
ON CONFLICT (srl_nbr, event_dttm) DO UPDATE SET
       event_type = EXCLUDED.event_type, source_system = EXCLUDED.source_system, alert_id = EXCLUDED.alert_id;
