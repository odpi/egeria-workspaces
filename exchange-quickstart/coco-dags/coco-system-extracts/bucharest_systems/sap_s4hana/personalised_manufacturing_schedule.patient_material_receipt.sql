-- Extract: SAP ERP S/4HANA (Bucharest) -> Personalised Manufacturing Schedule / patient_material_receipt
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.personalised_manufacturing_schedule.patient_material_receipt
-- Received (wbstk = C) patient blood donation deliveries (likp.lfart = ZPMI); courier AWB from lifex; arrival
-- date/time from lfdat/lfuhr.
SELECT
  l.lifex::varchar(40) AS shipment_identifier,
  l.zz_patient_pseudonym::varchar(40) AS patient_pseudonym_identifier,
  ((to_date(l.lfdat, 'YYYYMMDD') + l.lfuhr::time) AT TIME ZONE 'UTC') AS shipment_delivery_timestamp,
  l.zz_arrival_cond AS shipment_arrival_description,
  l.zz_viable_hours AS sample_viable_duration
FROM sap_s4hana.likp l
WHERE l.mandt = '300' AND l.lfart = 'ZPMI' AND l.wbstk = 'C'
