-- Extract: Austin Manufacturing Control System (Coco core) -> Batch Execution Records / execution_step
-- Source: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Target: coco_data_hub.batch_execution_records.execution_step
-- mfc_operation for finished operations; op_seq/10 as step number, badge to pseudonym via mfc_operator.
SELECT
  o.batch_id::varchar(40)               AS batch_identifier,
  (o.op_seq / 10)::integer              AS execution_step_number,
  o.op_code::varchar(40)                AS execution_step_code,
  o.start_utc                           AS execution_step_start_timestamp,
  o.end_utc                             AS execution_step_end_timestamp,
  p.worker_psn::varchar(40)             AS worker_pseudonym_identifier,
  o.e_signature::varchar(200)           AS execution_step_signature,
  (CASE o.op_result WHEN 'CD' THEN 'complete with deviation' WHEN 'AB' THEN 'aborted' ELSE 'complete' END)::varchar(100) AS execution_step_status
FROM mfctrl9482.mfc_operation o
JOIN mfctrl9482.mfc_operator p ON p.badge_no = o.badge_no
WHERE o.end_utc IS NOT NULL
