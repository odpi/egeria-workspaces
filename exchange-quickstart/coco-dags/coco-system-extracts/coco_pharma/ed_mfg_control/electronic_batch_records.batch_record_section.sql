-- Extract: Edmonton Manufacturing Control System (Coco core) -> Electronic Batch Records / batch_record_section
-- Source: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Target: coco_data_hub.electronic_batch_records.batch_record_section
-- ebr_section; section kind lower-cased, local text receipt time to timestamptz.
SELECT
  s.lot_id::varchar(40)                  AS batch_identifier,
  s.section_ref::varchar(40)             AS batch_record_section_reference_identifier,
  lower(s.section_kind)::varchar(40)     AS batch_record_section_type,
  s.source_system::varchar(60)           AS system_identifier,
  (s.received::timestamp AT TIME ZONE 'America/Edmonton') AS batch_record_section_received_timestamp
FROM ed_mfg_control.ebr_section s
