-- Extract: Edmonton Manufacturing Control System (Coco core) -> Batch Execution Records / equipment_usage
-- Source: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Target: coco_data_hub.batch_execution_records.equipment_usage
-- equip_log for finished operations; DD/MM/YYYY text to date, overdue calibration reported as expired.
SELECT
  e.lot_id::varchar(40)                  AS batch_identifier,
  (e.seq / 10)::integer                  AS execution_step_number,
  e.asset_tag::varchar(40)               AS equipment_identifier,
  (CASE lower(e.qual_state) WHEN 'qualified' THEN 'qualified' WHEN 'overdue' THEN 'expired' ELSE 'not qualified' END)::varchar(20) AS equipment_qualified_status,
  to_date(e.cal_exp, 'DD/MM/YYYY')       AS equipment_calibration_end_date
FROM ed_mfg_control.equip_log e
JOIN ed_mfg_control.op_log l ON l.lot_id = e.lot_id AND l.seq = e.seq
WHERE l.finished IS NOT NULL
