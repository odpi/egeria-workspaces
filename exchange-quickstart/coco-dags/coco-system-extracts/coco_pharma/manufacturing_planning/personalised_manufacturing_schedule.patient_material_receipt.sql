-- Extract: Global Manufacturing Planning (Coco core) -> Personalised Manufacturing Schedule / patient_material_receipt
-- Source: coco_pharma.manufacturing_planning (System::manufacturing-planning)
-- Target: coco_data_hub.personalised_manufacturing_schedule.patient_material_receipt
-- inbd_matl; arrival condition code expanded into the description with the receiving note.
SELECT
  m.consignment_no::varchar(40)                 AS shipment_identifier,
  m.patient_ref::varchar(40)                    AS patient_pseudonym_identifier,
  m.arr_ts                                      AS shipment_delivery_timestamp,
  (CASE m.arr_cond_cd WHEN 'OK' THEN 'Received in condition' WHEN 'TEMP' THEN 'Temperature excursion'
                      WHEN 'LATE' THEN 'Late arrival' WHEN 'DMG' THEN 'Damaged' ELSE m.arr_cond_cd END
     || coalesce(': ' || m.arr_note, ''))::text AS shipment_arrival_description,
  m.viab_hrs_rem::integer                       AS sample_viable_duration
FROM manufacturing_planning.inbd_matl m
