-- Extract: Austin Manufacturing Control System (Coco core) -> Electronic Batch Records / release_authorisation
-- Source: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Target: coco_data_hub.electronic_batch_records.release_authorisation
-- mfc_release; ISO alpha-3 market to alpha-2, badge to pseudonym via mfc_operator.
SELECT
  r.batch_id::varchar(40)               AS batch_identifier,
  (CASE r.market WHEN 'USA' THEN 'US' WHEN 'CAN' THEN 'CA' WHEN 'GBR' THEN 'GB' ELSE r.market END)::varchar(8) AS market_code,
  r.qty_released::integer               AS batch_released_quantity,
  r.cert_date                           AS batch_certification_date,
  p.worker_psn::varchar(40)             AS batch_certifier_identifier
FROM mfctrl9482.mfc_release r
JOIN mfctrl9482.mfc_operator p ON p.badge_no = r.released_by
