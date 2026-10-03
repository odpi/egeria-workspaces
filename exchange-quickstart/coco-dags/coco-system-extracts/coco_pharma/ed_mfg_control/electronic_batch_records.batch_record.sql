-- Extract: Edmonton Manufacturing Control System (Coco core) -> Electronic Batch Records / batch_record
-- Source: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Target: coco_data_hub.electronic_batch_records.batch_record
-- prod_lot; item_no to product code text, local text times to timestamptz, ebr_complete 1/0 to boolean, qa_disposition to certification status.
SELECT
  p.lot_id::varchar(40)                  AS batch_identifier,
  p.item_no::varchar(20)                 AS product_code,
  NULL::varchar(40)                      AS patient_pseudonym_identifier,
  (p.start_dt::timestamp AT TIME ZONE 'America/Edmonton')  AS batch_start_timestamp,
  (p.finish_dt::timestamp AT TIME ZONE 'America/Edmonton') AS batch_end_timestamp,
  p.yield_qty::integer                   AS batch_quantity,
  (p.ebr_complete = 1)                   AS batch_record_complete_flag,
  (CASE lower(p.qa_disposition) WHEN 'approved' THEN 'certified' WHEN 'rejected' THEN 'rejected' ELSE 'awaiting review' END)::varchar(20) AS batch_certification_status
FROM ed_mfg_control.prod_lot p
