-- Subscription: buc_factorytalk__serial_number_allocations - Rockwell FactoryTalk (Bucharest) receives Serial Number Allocations
-- Destination: bucharest_systems.factorytalk (SoftwareServer::SYS-015::Rockwell FactoryTalk)
-- Why it subscribes: Commissioned Packs depends on it (issue identifiers)
-- Keeps the serial number blocks for EKG packs (GTINs of EKG's GS1 company prefix 0594482, as commissioned on its
-- lines) in the new serialisation pool table sn_allocation, loaded before the packaging line starts a lot; the line's
-- serial events are unchanged.  Blocks for other companies' GTINs are discarded (Coco group data - EKG is not yet
-- integrated).  The product has no source yet.
UPDATE incoming_serial_number_allocation SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE pack_code IS NULL OR pack_code NOT LIKE '0594482%';

INSERT INTO factorytalk.sn_allocation (allocation_id, gtin, material, target_market, lot, serial_start, serial_end,
                                       serial_count, received_time, pool_status)
SELECT i.allocation_identifier, i.pack_code, i.product_code, i.market_code, i.batch_identifier,
       i.allocation_start_number, i.allocation_end_number, coalesce(i.allocation_count, 0),
       coalesce(i.allocation_timestamp, now()), 'LOADED'
  FROM incoming_serial_number_allocation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (allocation_id) DO NOTHING;
