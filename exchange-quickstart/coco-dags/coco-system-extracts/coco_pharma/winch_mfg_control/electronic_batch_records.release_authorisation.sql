-- Extract: Winchester Manufacturing Control System (Coco core) -> Electronic Batch Records / release_authorisation
-- Source: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Target: coco_data_hub.electronic_batch_records.release_authorisation
-- wrel; market UK translated to ISO GB.
SELECT
  r.batch_no::varchar(40)             AS batch_identifier,
  (CASE upper(r.mkt) WHEN 'UK' THEN 'GB' ELSE upper(r.mkt) END)::varchar(8) AS market_code,
  r.rel_qty::integer                  AS batch_released_quantity,
  r.cert_dt                           AS batch_certification_date,
  r.qp_psn::varchar(40)               AS batch_certifier_identifier
FROM winch_mfg_control.wrel r
