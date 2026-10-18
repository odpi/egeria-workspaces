-- Extract: Winchester Manufacturing Control System (Coco core) -> Electronic Batch Records / batch_record_section
-- Source: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Target: coco_data_hub.electronic_batch_records.batch_record_section
-- wdoc; section type codes expanded to the product's section names.
SELECT
  d.batch_no::varchar(40)             AS batch_identifier,
  d.sect_ref::varchar(40)             AS batch_record_section_reference_identifier,
  (CASE d.sect_typ WHEN 'EXEC' THEN 'execution' WHEN 'PARAM' THEN 'process parameters' WHEN 'LAB' THEN 'laboratory results'
                   WHEN 'DEV' THEN 'deviation disposition' WHEN 'EXC' THEN 'excursion disposition'
                   WHEN 'SIGN' THEN 'signature authority' END)::varchar(40) AS batch_record_section_type,
  d.src_sys::varchar(60)              AS system_identifier,
  d.rcvd_ts                           AS batch_record_section_received_timestamp
FROM winch_mfg_control.wdoc d
