-- Extract: Austin Manufacturing Control System (Coco core) -> Batch Execution Records / material_usage
-- Source: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Target: coco_data_hub.batch_execution_records.material_usage
-- mfc_consumption for finished operations; unit lower-cased.
SELECT
  c.batch_id::varchar(40)               AS batch_identifier,
  (c.op_seq / 10)::integer              AS execution_step_number,
  c.lot_no::varchar(40)                 AS lot_identifier,
  c.item_cd::varchar(20)                AS raw_material_code,
  c.qty_consumed::double precision      AS raw_material_used_quantity,
  (CASE c.uom WHEN 'L' THEN 'L' ELSE lower(c.uom) END)::varchar(20) AS raw_material_used_unit
FROM mfctrl9482.mfc_consumption c
JOIN mfctrl9482.mfc_operation o ON o.batch_id = c.batch_id AND o.op_seq = c.op_seq
WHERE o.end_utc IS NOT NULL
