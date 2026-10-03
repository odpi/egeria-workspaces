-- Subscription: buc_proact_cold_chain__patient_sample_consignments - Proact Cold Chain Monitor (Bucharest) receives Patient Sample Consignments
-- Destination: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Why it subscribes: Cold Chain Transit Records depends on it (inbound material record)
-- Keeps inbound patient material consignments carried by EKG's couriers (carrier = an EKG SAP vendor number 7xxxxx) as
-- inbound shipment manifests in shipment_manifest (order, patient pseudonym, viable hours), so a trip can be started with
-- the right alarm profile and viability clock.  Other consignments are discarded (Coco group data - EKG is not yet
-- integrated).  The product has no source yet.
UPDATE incoming_sample_consignment SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE carrier_identifier IS NULL OR carrier_identifier !~ '^0*7[0-9]{5}$';

INSERT INTO proact_cold_chain.shipment_manifest (shipment_ref, direction, carrier_ref, dispatch_date, order_ref, patient_ref,
                                                 viable_hours, updated_at)
SELECT i.shipment_identifier, 'IN', ltrim(i.carrier_identifier, '0'),
       (coalesce(i.shipment_dispatch_timestamp, i.sample_collection_timestamp) AT TIME ZONE 'Europe/Bucharest')::date,
       i.order_identifier, i.patient_pseudonym_identifier, i.sample_viable_duration, now()
  FROM incoming_sample_consignment i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipment_ref) DO UPDATE
   SET carrier_ref = EXCLUDED.carrier_ref, dispatch_date = EXCLUDED.dispatch_date, order_ref = EXCLUDED.order_ref,
       patient_ref = EXCLUDED.patient_ref, viable_hours = EXCLUDED.viable_hours, updated_at = now()
 WHERE (proact_cold_chain.shipment_manifest.carrier_ref, proact_cold_chain.shipment_manifest.dispatch_date,
        proact_cold_chain.shipment_manifest.order_ref, proact_cold_chain.shipment_manifest.patient_ref,
        proact_cold_chain.shipment_manifest.viable_hours)
       IS DISTINCT FROM (EXCLUDED.carrier_ref, EXCLUDED.dispatch_date, EXCLUDED.order_ref, EXCLUDED.patient_ref,
                         EXCLUDED.viable_hours);
