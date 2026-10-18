-- Subscription: buc_opcenter_mes__patient_sample_consignments - Siemens Opcenter MES (Bucharest) receives Patient Sample Consignments
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Cold Chain Transit Records depends on it (inbound material record)
-- Keeps inbound patient material consignments for EKG's named-patient orders (pseudonym known on a container or
-- downloaded order of this MES) in the new table inboundshipment - collection, arrival, remaining viable hours - checked
-- before the batch is started.  Other pseudonyms are discarded (Coco group data - EKG is not yet integrated).  The
-- product has no source yet.
UPDATE incoming_sample_consignment i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.patientpseudonym = i.patient_pseudonym_identifier)
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.mfgorder o WHERE o.patientpseudonym = i.patient_pseudonym_identifier);

INSERT INTO opcenter_mes.inboundshipment (shipmentname, mfgordername, patientpseudonym, carriervendor, collectiondate,
                                          dispatchdate, arrivedate, viablehours, arrivalcondition, lastchangedate)
SELECT i.shipment_identifier, left(i.order_identifier, 20), i.patient_pseudonym_identifier, left(i.carrier_identifier, 10),
       i.sample_collection_timestamp, i.shipment_dispatch_timestamp, i.shipment_delivery_timestamp, i.sample_viable_duration,
       i.shipment_arrival_description, now()
  FROM incoming_sample_consignment i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipmentname) DO UPDATE
   SET mfgordername = coalesce(EXCLUDED.mfgordername, opcenter_mes.inboundshipment.mfgordername),
       patientpseudonym = EXCLUDED.patientpseudonym, carriervendor = EXCLUDED.carriervendor,
       collectiondate = EXCLUDED.collectiondate, dispatchdate = EXCLUDED.dispatchdate,
       arrivedate = coalesce(EXCLUDED.arrivedate, opcenter_mes.inboundshipment.arrivedate),
       viablehours = coalesce(EXCLUDED.viablehours, opcenter_mes.inboundshipment.viablehours),
       arrivalcondition = coalesce(EXCLUDED.arrivalcondition, opcenter_mes.inboundshipment.arrivalcondition), lastchangedate = now()
 WHERE (opcenter_mes.inboundshipment.patientpseudonym, opcenter_mes.inboundshipment.carriervendor,
        opcenter_mes.inboundshipment.collectiondate, opcenter_mes.inboundshipment.dispatchdate)
       IS DISTINCT FROM (EXCLUDED.patientpseudonym, EXCLUDED.carriervendor, EXCLUDED.collectiondate, EXCLUDED.dispatchdate)
    OR (EXCLUDED.mfgordername IS NOT NULL AND EXCLUDED.mfgordername IS DISTINCT FROM opcenter_mes.inboundshipment.mfgordername)
    OR (EXCLUDED.arrivedate IS NOT NULL AND EXCLUDED.arrivedate IS DISTINCT FROM opcenter_mes.inboundshipment.arrivedate)
    OR (EXCLUDED.viablehours IS NOT NULL AND EXCLUDED.viablehours IS DISTINCT FROM opcenter_mes.inboundshipment.viablehours)
    OR (EXCLUDED.arrivalcondition IS NOT NULL AND EXCLUDED.arrivalcondition IS DISTINCT FROM opcenter_mes.inboundshipment.arrivalcondition);
