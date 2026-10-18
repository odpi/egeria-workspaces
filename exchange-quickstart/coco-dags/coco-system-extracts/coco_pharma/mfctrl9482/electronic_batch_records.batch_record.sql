-- Extract: Austin Manufacturing Control System (Coco core) -> Electronic Batch Records / batch_record
-- Source: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Target: coco_data_hub.electronic_batch_records.batch_record
-- mfc_batch; quantity only once the batch has ended, qa_status to certification status.
SELECT
  b.batch_id::varchar(40)               AS batch_identifier,
  b.product_cd::varchar(20)             AS product_code,
  NULL::varchar(40)                     AS patient_pseudonym_identifier,
  b.start_utc                           AS batch_start_timestamp,
  b.end_utc                             AS batch_end_timestamp,
  (CASE WHEN b.end_utc IS NOT NULL THEN b.qty END)::integer AS batch_quantity,
  b.record_complete                     AS batch_record_complete_flag,
  (CASE b.qa_status WHEN 'CERTIFIED' THEN 'certified' WHEN 'REJECTED' THEN 'rejected' ELSE 'awaiting review' END)::varchar(20) AS batch_certification_status
FROM mfctrl9482.mfc_batch b
