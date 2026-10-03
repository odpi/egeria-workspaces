-- Extract: Winchester Manufacturing Control System (Coco core) -> Electronic Batch Records / batch_record
-- Source: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Target: coco_data_hub.electronic_batch_records.batch_record
-- wbatch; Y/N completeness flag to boolean and qp_sts to the certification status.
SELECT
  b.batch_no::varchar(40)             AS batch_identifier,
  b.prd_cd::varchar(20)               AS product_code,
  b.psn_ref::varchar(40)              AS patient_pseudonym_identifier,
  b.strt_ts                           AS batch_start_timestamp,
  b.end_ts                            AS batch_end_timestamp,
  b.qty_made::integer                 AS batch_quantity,
  (b.rec_cmplt = 'Y')                 AS batch_record_complete_flag,
  (CASE b.qp_sts WHEN 'C' THEN 'certified' WHEN 'R' THEN 'rejected' ELSE 'awaiting review' END)::varchar(20) AS batch_certification_status
FROM winch_mfg_control.wbatch b
