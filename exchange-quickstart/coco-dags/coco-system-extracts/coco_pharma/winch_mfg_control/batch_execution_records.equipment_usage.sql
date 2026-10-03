-- Extract: Winchester Manufacturing Control System (Coco core) -> Batch Execution Records / equipment_usage
-- Source: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Target: coco_data_hub.batch_execution_records.equipment_usage
-- wstep_eq for completed steps; Q/X/N qualification codes expanded.
SELECT
  e.batch_no::varchar(40)             AS batch_identifier,
  e.step_no::integer                  AS execution_step_number,
  e.eq_id::varchar(40)                AS equipment_identifier,
  (CASE e.qual_at_use WHEN 'Q' THEN 'qualified' WHEN 'X' THEN 'expired' ELSE 'not qualified' END)::varchar(20) AS equipment_qualified_status,
  e.cal_due                           AS equipment_calibration_end_date
FROM winch_mfg_control.wstep_eq e
JOIN winch_mfg_control.wstep st ON st.batch_no = e.batch_no AND st.step_no = e.step_no
WHERE st.en_ts IS NOT NULL
