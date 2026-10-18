-- Subscription: aus_factorytalk_scada__serial_number_allocations - Rockwell FactoryTalk SCADA (Austin) receives Serial Number Allocations
-- Destination: austin_systems.factorytalk_scada (SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610)
-- Why it subscribes: Commissioned Packs depends on it (issue identifiers)
-- Keeps the serial number ranges allocated for packs made on the Austin packaging lines (Austin AU- products and the
-- Coco products made at Austin, for the US market) in the NEW serial_pool table the line serialisation controller
-- draws from; line_serial_event, which feeds Commissioned Packs, only changes when packs are commissioned.
-- Allocations for other products, markets or estates' batches are discarded.

UPDATE incoming_serial_number_allocation i SET discard_reason = 'other estate: product not packed at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
UPDATE incoming_serial_number_allocation i SET discard_reason = 'other estate: batch not made at Austin'
 WHERE i.discard_reason IS NULL AND i.batch_identifier IS NOT NULL AND i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_serial_number_allocation i SET discard_reason = 'market not packed on the Austin lines'
 WHERE i.discard_reason IS NULL AND i.market_code <> 'US';
INSERT INTO factorytalk_scada.serial_pool
       (allocation_id, gtin, product_code, market, range_start, range_end, serial_count, allocated_time, lot)
SELECT i.allocation_identifier, i.pack_code, i.product_code, i.market_code, i.allocation_start_number,
       i.allocation_end_number, i.allocation_count, i.allocation_timestamp, i.batch_identifier
  FROM incoming_serial_number_allocation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (allocation_id) DO UPDATE SET
       gtin = EXCLUDED.gtin, product_code = EXCLUDED.product_code, market = EXCLUDED.market,
       range_start = EXCLUDED.range_start, range_end = EXCLUDED.range_end, serial_count = EXCLUDED.serial_count,
       allocated_time = EXCLUDED.allocated_time, lot = EXCLUDED.lot;
