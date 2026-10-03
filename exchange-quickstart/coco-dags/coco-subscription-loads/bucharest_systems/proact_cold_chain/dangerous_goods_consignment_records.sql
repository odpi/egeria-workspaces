-- Subscription: buc_proact_cold_chain__dangerous_goods_consignment_records - Proact Cold Chain Monitor (Bucharest) receives Dangerous Goods Consignment Records
-- Destination: bucharest_systems.proact_cold_chain (SoftwareServer::SYS-022::Proact Cold Chain Monitor)
-- Why it subscribes: Carrier Transit Events depends on it (consigned to carrier)
-- Keeps the WMS's dangerous goods declaration of each EKG despatch (EXP- numbers) as the outbound shipment manifest in
-- the new table shipment_manifest (carrier, dispatch date, dry-ice UN number and quantity), used to set up the trip and
-- its alarm profile; the accompanying documents are not kept.  Other companies' consignments are discarded (Coco group
-- data - EKG is not yet integrated).
UPDATE incoming_consignment_declaration SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE shipment_identifier NOT LIKE 'EXP-%';
UPDATE incoming_consignment_document SET discard_reason = 'consignment documents are not kept by the cold chain monitor'
 WHERE shipment_identifier LIKE 'EXP-%';
UPDATE incoming_consignment_document SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO proact_cold_chain.shipment_manifest (shipment_ref, direction, carrier_ref, dispatch_date, ship_to, un_number,
                                                 dg_quantity, dg_unit, updated_at)
SELECT i.shipment_identifier, 'OUT', left(i.carrier_identifier, 10), i.shipment_dispatch_date, i.shipment_ship_to_address,
       i.transport_classification_code, i.shipment_quantity, i.shipment_unit, now()
  FROM incoming_consignment_declaration i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipment_ref) DO UPDATE
   SET carrier_ref = EXCLUDED.carrier_ref, dispatch_date = EXCLUDED.dispatch_date, ship_to = EXCLUDED.ship_to,
       un_number = EXCLUDED.un_number, dg_quantity = EXCLUDED.dg_quantity, dg_unit = EXCLUDED.dg_unit, updated_at = now()
 WHERE (proact_cold_chain.shipment_manifest.carrier_ref, proact_cold_chain.shipment_manifest.dispatch_date,
        proact_cold_chain.shipment_manifest.ship_to, proact_cold_chain.shipment_manifest.un_number,
        proact_cold_chain.shipment_manifest.dg_quantity, proact_cold_chain.shipment_manifest.dg_unit)
       IS DISTINCT FROM (EXCLUDED.carrier_ref, EXCLUDED.dispatch_date, EXCLUDED.ship_to, EXCLUDED.un_number,
                         EXCLUDED.dg_quantity, EXCLUDED.dg_unit);
