-- Subscription: aus_veeva_ebr__personalised_manufacturing_schedule - Veeva Vault EBR (Austin) receives Personalised Manufacturing Schedule
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (open batch)
-- Keeps the Austin patient-specific manufacturing slots (SAP ZPAT orders) as NEW planned_batch__c records, from
-- which the batch record is opened when the slot starts, and the patient material receipts for those patients as NEW
-- patient_material_receipt__c records. batch__v, which the extracts read, is not written. Coco (Winchester cell
-- therapy) and EKG slots and receipts are discarded.

UPDATE incoming_manufacturing_slot i SET discard_reason = CASE WHEN i.batch_identifier ~ '^[WE][0-9]{2}-'
       THEN 'other estate: Coco factory batch' ELSE 'other estate: not an Austin batch' END
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
INSERT INTO veeva_ebr.planned_batch__c
       (id, name__v, order_reference__c, patient_pseudonym__c, product_code__c, slot_start__c, slot_end__c,
        patient_parameters__c, slot_status__c)
SELECT ('0PB' || upper(substr(md5(i.batch_identifier), 1, 11))), i.batch_identifier, i.order_identifier, i.patient_pseudonym_identifier,
       i.product_code, i.slot_start_timestamp, i.slot_end_timestamp, i.patient_parameter_description, i.slot_status
  FROM incoming_manufacturing_slot i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, order_reference__c = EXCLUDED.order_reference__c,
       patient_pseudonym__c = EXCLUDED.patient_pseudonym__c, product_code__c = EXCLUDED.product_code__c,
       slot_start__c = EXCLUDED.slot_start__c, slot_end__c = EXCLUDED.slot_end__c,
       patient_parameters__c = EXCLUDED.patient_parameters__c, slot_status__c = EXCLUDED.slot_status__c;

UPDATE incoming_patient_material_receipt i SET discard_reason = 'other estate: patient not scheduled at Austin'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_ebr.planned_batch__c p
                    WHERE p.patient_pseudonym__c = i.patient_pseudonym_identifier);
INSERT INTO veeva_ebr.patient_material_receipt__c
       (id, name__v, patient_pseudonym__c, received_datetime__c, arrival_condition__c, viable_hours__c)
SELECT ('0PM' || upper(substr(md5(i.shipment_identifier), 1, 11))), i.shipment_identifier, i.patient_pseudonym_identifier,
       i.shipment_delivery_timestamp, i.shipment_arrival_description, i.sample_viable_duration
  FROM incoming_patient_material_receipt i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, patient_pseudonym__c = EXCLUDED.patient_pseudonym__c,
       received_datetime__c = EXCLUDED.received_datetime__c, arrival_condition__c = EXCLUDED.arrival_condition__c,
       viable_hours__c = EXCLUDED.viable_hours__c;
