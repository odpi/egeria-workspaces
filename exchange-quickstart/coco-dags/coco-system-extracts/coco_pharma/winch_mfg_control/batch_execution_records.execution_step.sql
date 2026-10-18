-- Extract: Winchester Manufacturing Control System (Coco core) -> Batch Execution Records / execution_step
-- Source: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Target: coco_data_hub.batch_execution_records.execution_step
-- wstep, completed steps only (en_ts set); dev_flg/abrt_flg translated to the step status.
SELECT
  st.batch_no::varchar(40)            AS batch_identifier,
  st.step_no::integer                 AS execution_step_number,
  st.op_cd::varchar(40)               AS execution_step_code,
  st.st_ts                            AS execution_step_start_timestamp,
  st.en_ts                            AS execution_step_end_timestamp,
  st.opr_psn::varchar(40)             AS worker_pseudonym_identifier,
  st.esig::varchar(200)               AS execution_step_signature,
  (CASE WHEN st.abrt_flg = 'Y' THEN 'aborted' WHEN st.dev_flg = 'Y' THEN 'complete with deviation'
        ELSE 'complete' END)::varchar(100) AS execution_step_status
FROM winch_mfg_control.wstep st
WHERE st.en_ts IS NOT NULL
