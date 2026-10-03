-- Subscription: aus_sap_s4hana__therapy_delivery_events - SAP S/4HANA (Austin) receives Therapy Delivery Events
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Treatment Invoices depends on it (fulfilment confirmed)
-- Keeps the proof of delivery and of administration for Austin patient therapy batches in the NEW Z table
-- ZSD_THERAPY_POD (one row per batch), which releases the billing due list. In-transit tracking events and other
-- estates' batches are discarded; the billing documents themselves (VBRK/VBRP, read by the extracts) are created by
-- billing, not here.

UPDATE incoming_delivery_event i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_delivery_event i SET discard_reason = 'tracking event: not a proof of delivery'
 WHERE i.discard_reason IS NULL AND i.shipment_event_type <> 'delivered';
INSERT INTO sap_s4hana.zsd_therapy_pod
       (mandt, charg, zz_treatment_order, zz_patient_pseudonym, pod_date, pod_time, pod_location)
SELECT DISTINCT ON (i.batch_identifier) '100', i.batch_identifier, i.order_identifier,
       i.patient_pseudonym_identifier, to_char(i.shipment_event_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.shipment_event_timestamp AT TIME ZONE 'UTC', 'HH24MISS'), left(i.shipment_event_location, 60)
  FROM incoming_delivery_event i
 WHERE i.discard_reason IS NULL
 ORDER BY i.batch_identifier, i.shipment_event_timestamp DESC
ON CONFLICT (mandt, charg) DO UPDATE SET
       zz_treatment_order = EXCLUDED.zz_treatment_order, zz_patient_pseudonym = EXCLUDED.zz_patient_pseudonym,
       pod_date = EXCLUDED.pod_date, pod_time = EXCLUDED.pod_time, pod_location = EXCLUDED.pod_location;

UPDATE incoming_administration_confirmation i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
INSERT INTO sap_s4hana.zsd_therapy_pod
       (mandt, charg, zz_treatment_order, zz_patient_pseudonym, admin_date, admin_time, admin_npi)
SELECT '100', i.batch_identifier, i.order_identifier, i.patient_pseudonym_identifier,
       to_char(i.treatment_administration_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'),
       to_char(i.treatment_administration_timestamp AT TIME ZONE 'UTC', 'HH24MISS'), i.clinician_identifier
  FROM incoming_administration_confirmation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, charg) DO UPDATE SET
       admin_date = EXCLUDED.admin_date, admin_time = EXCLUDED.admin_time, admin_npi = EXCLUDED.admin_npi;
