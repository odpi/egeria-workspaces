-- Extract: Edmonton Manufacturing Control System (Coco core) -> Batch Execution Records / material_usage
-- Source: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Target: coco_data_hub.batch_execution_records.material_usage
-- consumption for finished operations; seq/10 as step number.
SELECT
  c.lot_id::varchar(40)                  AS batch_identifier,
  (c.seq / 10)::integer                  AS execution_step_number,
  c.component_lot::varchar(40)           AS lot_identifier,
  upper(c.item_no)::varchar(20)          AS raw_material_code,
  c.qty_used::double precision           AS raw_material_used_quantity,
  c.uom::varchar(20)                     AS raw_material_used_unit
FROM ed_mfg_control.consumption c
JOIN ed_mfg_control.op_log l ON l.lot_id = c.lot_id AND l.seq = c.seq
WHERE l.finished IS NOT NULL
