-- Subscription: coco_global_crm__therapy_delivery_events - Global customer ordering system (Coco core) receives Therapy Delivery Events
-- Destination: coco_pharma.global_crm (System::globalCRM)
-- Why it subscribes: Treatment Invoices depends on it (fulfilment confirmed)
-- Keeps the shipment events and administration confirmations of its own personalised therapy orders (SO- order
-- numbers) in the custom objects therapy_shipment_event__c and therapy_administration__c (both NEW), shown on
-- the order and used to raise the invoice; sales_order.status is left to the order desk.  Discards Austin's own
-- cell therapy orders (TO- orders, AU-7710), which are not in Coco's ordering system.

UPDATE incoming_delivery_event SET discard_reason = 'Austin therapy order - not in Coco''s ordering system'
 WHERE order_identifier NOT LIKE 'SO-%';

INSERT INTO global_crm.therapy_shipment_event__c (batch_number__c, event_type__c, event_time__c, order__c, patient_reference__c,
       location__c, storage_conditions__c)
SELECT e.batch_identifier, initcap(e.shipment_event_type), e.shipment_event_timestamp, e.order_identifier,
       e.patient_pseudonym_identifier, e.shipment_event_location, e.shipment_storage_description
  FROM incoming_delivery_event e
 WHERE e.discard_reason IS NULL
ON CONFLICT (batch_number__c, event_type__c, event_time__c) DO UPDATE SET order__c = EXCLUDED.order__c,
       patient_reference__c = EXCLUDED.patient_reference__c, location__c = EXCLUDED.location__c,
       storage_conditions__c = EXCLUDED.storage_conditions__c;

UPDATE incoming_administration_confirmation SET discard_reason = 'Austin therapy order - not in Coco''s ordering system'
 WHERE order_identifier NOT LIKE 'SO-%';

INSERT INTO global_crm.therapy_administration__c (batch_number__c, order__c, patient_reference__c, administered_at__c, clinician__c)
SELECT a.batch_identifier, a.order_identifier, a.patient_pseudonym_identifier, a.treatment_administration_timestamp,
       a.clinician_identifier
  FROM incoming_administration_confirmation a
 WHERE a.discard_reason IS NULL
ON CONFLICT (batch_number__c) DO UPDATE SET order__c = EXCLUDED.order__c, patient_reference__c = EXCLUDED.patient_reference__c,
       administered_at__c = EXCLUDED.administered_at__c, clinician__c = EXCLUDED.clinician__c;
