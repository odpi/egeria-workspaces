-- Subscription: buc_proact_cold_chain__in_transit_temperature_readings - Proact Cold Chain Monitor (Bucharest) receives In-Transit Temperature Readings
-- Destination: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Why it subscribes: Cold Chain Transit Records depends on it (transit temperature record)
-- The cold chain monitor is the only source of EKG's in-transit readings, so every reading from one of its devices is
-- already held here and is discarded (no feedback loop); readings from other devices are discarded as Coco group data
-- (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_temperature_reading i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM proact_cold_chain.device d WHERE d.device_id = i.device_identifier);
UPDATE incoming_temperature_reading SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
