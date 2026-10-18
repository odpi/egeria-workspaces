-- Extract: Edmonton Manufacturing Control System (Coco core) -> Electronic Batch Records / release_authorisation
-- Source: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Target: coco_data_hub.electronic_batch_records.release_authorisation
-- market_release; country upper-cased, QP employee number to pseudonym via operator.
SELECT
  r.lot_id::varchar(40)                  AS batch_identifier,
  upper(r.country)::varchar(8)           AS market_code,
  r.qty_rel::integer                     AS batch_released_quantity,
  r.certified_on                         AS batch_certification_date,
  o.worker_ref::varchar(40)              AS batch_certifier_identifier
FROM ed_mfg_control.market_release r
JOIN ed_mfg_control.operator o ON o.emp_no = r.qp
