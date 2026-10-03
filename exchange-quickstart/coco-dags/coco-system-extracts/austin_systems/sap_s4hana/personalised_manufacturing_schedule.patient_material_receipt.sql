-- Extract: SAP S/4HANA (Austin) -> Personalised Manufacturing Schedule / patient_material_receipt
-- Source: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Target: coco_data_hub.personalised_manufacturing_schedule.patient_material_receipt
-- Received (wbstk = C) patient material inbound deliveries (likp.lfart = ZPMI); courier shipment ID from lifex;
-- arrival date/time from lfdat/lfuhr.
SELECT
  l.lifex::varchar(40) AS shipment_identifier,
  l.zz_patient_pseudonym::varchar(40) AS patient_pseudonym_identifier,
  ((to_date(l.lfdat, 'YYYYMMDD') + l.lfuhr::time) AT TIME ZONE 'UTC') AS shipment_delivery_timestamp,
  l.zz_arrival_cond AS shipment_arrival_description,
  l.zz_viable_hours AS sample_viable_duration
FROM sap_s4hana.likp l
WHERE l.mandt = '100' AND l.lfart = 'ZPMI' AND l.wbstk = 'C'
