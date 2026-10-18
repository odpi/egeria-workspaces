-- Subscription: buc_opcenter_mes__personalised_manufacturing_schedule - Siemens Opcenter MES (Bucharest) receives Personalised Manufacturing Schedule
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Electronic Batch Records depends on it (open batch)
-- Keeps SAP's named-patient manufacturing slots for EKG products (product known in this MES) that have not started yet
-- as downloaded manufacturing orders (new table mfgorder, ordertype NamedPatient, keyed by the treatment order, with the
-- planned batch and patient parameters), and the receipt of the patient's material in inboundshipment.  Slots whose
-- batch is already a container are discarded (already held); other products' slots and receipts are discarded (Coco
-- group data - EKG is not yet integrated).
UPDATE incoming_manufacturing_slot i SET discard_reason = 'batch already started in the MES'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_manufacturing_slot i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.product p WHERE p.productname = i.product_code);

INSERT INTO opcenter_mes.mfgorder (mfgordername, ordertype, productid, plannedcontainer, qty, uom, plannedstartdate,
                                   plannedcompletiondate, patientpseudonym, patientparameters, orderstatus, lastchangedate)
SELECT left(coalesce(i.order_identifier, i.batch_identifier), 20), 'NamedPatient', p.productid, i.batch_identifier, 1, 'BUC',
       i.slot_start_timestamp, i.slot_end_timestamp, i.patient_pseudonym_identifier, i.patient_parameter_description,
       coalesce(i.slot_status, 'scheduled'), now()
  FROM incoming_manufacturing_slot i JOIN opcenter_mes.product p ON p.productname = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (mfgordername) DO UPDATE
   SET productid = EXCLUDED.productid, plannedcontainer = EXCLUDED.plannedcontainer,
       plannedstartdate = EXCLUDED.plannedstartdate, plannedcompletiondate = EXCLUDED.plannedcompletiondate,
       patientpseudonym = EXCLUDED.patientpseudonym, patientparameters = EXCLUDED.patientparameters,
       orderstatus = EXCLUDED.orderstatus, lastchangedate = now()
 WHERE (opcenter_mes.mfgorder.productid, opcenter_mes.mfgorder.plannedcontainer, opcenter_mes.mfgorder.plannedstartdate,
        opcenter_mes.mfgorder.plannedcompletiondate, opcenter_mes.mfgorder.patientpseudonym,
        opcenter_mes.mfgorder.patientparameters, opcenter_mes.mfgorder.orderstatus)
       IS DISTINCT FROM (EXCLUDED.productid, EXCLUDED.plannedcontainer, EXCLUDED.plannedstartdate,
                         EXCLUDED.plannedcompletiondate, EXCLUDED.patientpseudonym, EXCLUDED.patientparameters,
                         EXCLUDED.orderstatus);

UPDATE incoming_patient_material_receipt i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.patientpseudonym = i.patient_pseudonym_identifier)
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.mfgorder o WHERE o.patientpseudonym = i.patient_pseudonym_identifier);

INSERT INTO opcenter_mes.inboundshipment (shipmentname, mfgordername, patientpseudonym, arrivedate, viablehours,
                                          arrivalcondition, lastchangedate)
SELECT i.shipment_identifier,
       coalesce((SELECT min(c.mfgordername) FROM opcenter_mes.container c WHERE c.patientpseudonym = i.patient_pseudonym_identifier),
                (SELECT min(o.mfgordername) FROM opcenter_mes.mfgorder o WHERE o.patientpseudonym = i.patient_pseudonym_identifier)),
       i.patient_pseudonym_identifier, i.shipment_delivery_timestamp, i.sample_viable_duration, i.shipment_arrival_description, now()
  FROM incoming_patient_material_receipt i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipmentname) DO UPDATE
   SET mfgordername = EXCLUDED.mfgordername, patientpseudonym = EXCLUDED.patientpseudonym, arrivedate = EXCLUDED.arrivedate,
       viablehours = EXCLUDED.viablehours, arrivalcondition = EXCLUDED.arrivalcondition, lastchangedate = now()
 WHERE (opcenter_mes.inboundshipment.mfgordername, opcenter_mes.inboundshipment.patientpseudonym,
        opcenter_mes.inboundshipment.arrivedate, opcenter_mes.inboundshipment.viablehours,
        opcenter_mes.inboundshipment.arrivalcondition)
       IS DISTINCT FROM (EXCLUDED.mfgordername, EXCLUDED.patientpseudonym, EXCLUDED.arrivedate, EXCLUDED.viablehours,
                         EXCLUDED.arrivalcondition);
