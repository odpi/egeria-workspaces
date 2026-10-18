-- Extract: Winchester Manufacturing Control System (Coco core) -> Batch Execution Records / material_usage
-- Source: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Target: coco_data_hub.batch_execution_records.material_usage
-- wmatl for steps that have completed.
SELECT
  m.batch_no::varchar(40)             AS batch_identifier,
  m.step_no::integer                  AS execution_step_number,
  m.lot_no::varchar(40)               AS lot_identifier,
  m.mat_cd::varchar(20)               AS raw_material_code,
  m.qty::double precision             AS raw_material_used_quantity,
  m.uom::varchar(20)                  AS raw_material_used_unit
FROM winch_mfg_control.wmatl m
JOIN winch_mfg_control.wstep st ON st.batch_no = m.batch_no AND st.step_no = m.step_no
WHERE st.en_ts IS NOT NULL
