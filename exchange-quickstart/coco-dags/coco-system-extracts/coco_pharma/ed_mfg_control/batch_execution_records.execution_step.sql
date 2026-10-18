-- Extract: Edmonton Manufacturing Control System (Coco core) -> Batch Execution Records / execution_step
-- Source: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Target: coco_data_hub.batch_execution_records.execution_step
-- op_log for finished operations; local text times to timestamptz, seq/10 as step number, DEV result as complete with deviation, operator emp_no to pseudonym via operator.
SELECT
  l.lot_id::varchar(40)                  AS batch_identifier,
  (l.seq / 10)::integer                  AS execution_step_number,
  upper(l.op_code)::varchar(40)          AS execution_step_code,
  (l.started::timestamp AT TIME ZONE 'America/Edmonton')  AS execution_step_start_timestamp,
  (l.finished::timestamp AT TIME ZONE 'America/Edmonton') AS execution_step_end_timestamp,
  o.worker_ref::varchar(40)              AS worker_pseudonym_identifier,
  l.esig_hash::varchar(200)              AS execution_step_signature,
  (CASE l.result WHEN 'DEV' THEN 'complete with deviation' WHEN 'ABT' THEN 'aborted' ELSE 'complete' END)::varchar(100) AS execution_step_status
FROM ed_mfg_control.op_log l
JOIN ed_mfg_control.operator o ON o.emp_no = l.operator
WHERE l.finished IS NOT NULL
