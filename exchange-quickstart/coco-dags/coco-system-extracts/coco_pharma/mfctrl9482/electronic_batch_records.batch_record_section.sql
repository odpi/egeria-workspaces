-- Extract: Austin Manufacturing Control System (Coco core) -> Electronic Batch Records / batch_record_section
-- Source: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Target: coco_data_hub.electronic_batch_records.batch_record_section
-- mfc_record_section; section type codes to the product's section names.
SELECT
  r.batch_id::varchar(40)               AS batch_identifier,
  r.section_ref::varchar(40)            AS batch_record_section_reference_identifier,
  lower(replace(r.section_type, '_', ' '))::varchar(40) AS batch_record_section_type,
  r.source_system::varchar(60)          AS system_identifier,
  r.received_utc                        AS batch_record_section_received_timestamp
FROM mfctrl9482.mfc_record_section r
