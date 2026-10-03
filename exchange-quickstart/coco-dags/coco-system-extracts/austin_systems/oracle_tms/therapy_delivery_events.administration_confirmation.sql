-- Extract: Oracle TMS (Austin) -> Therapy Delivery Events / administration_confirmation
-- Source: austin_systems.oracle_tms (SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004)
-- Target: coco_data_hub.therapy_delivery_events.administration_confirmation
-- ADMINISTERED status events posted by the treating site through the courier portal, with the clinician NPI reference.
SELECT
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.BATCH_NO' LIMIT 1)::varchar(40) AS batch_identifier,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.PATIENT_REF' LIMIT 1)::varchar(40) AS patient_pseudonym_identifier,
  e.event_date AS treatment_administration_timestamp,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.CLINICIAN_NPI' LIMIT 1)::varchar(40) AS clinician_identifier,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.ORDER_NO' LIMIT 1)::varchar(40) AS order_identifier
FROM oracle_tms.ie_shipmentstatus e
JOIN oracle_tms.shipment s ON s.shipment_gid = e.shipment_gid
WHERE e.status_code_gid = 'AUS.ADMINISTERED'
