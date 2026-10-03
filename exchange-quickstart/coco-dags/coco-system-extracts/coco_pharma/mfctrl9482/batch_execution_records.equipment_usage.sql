-- Extract: Austin Manufacturing Control System (Coco core) -> Batch Execution Records / equipment_usage
-- Source: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Target: coco_data_hub.batch_execution_records.equipment_usage
-- mfc_equipment_use for finished operations; status lower-cased.
SELECT
  e.batch_id::varchar(40)               AS batch_identifier,
  (e.op_seq / 10)::integer              AS execution_step_number,
  e.equip_id::varchar(40)               AS equipment_identifier,
  lower(e.qual_status)::varchar(20)     AS equipment_qualified_status,
  e.cal_expiry                          AS equipment_calibration_end_date
FROM mfctrl9482.mfc_equipment_use e
JOIN mfctrl9482.mfc_operation o ON o.batch_id = e.batch_id AND o.op_seq = e.op_seq
WHERE o.end_utc IS NOT NULL
