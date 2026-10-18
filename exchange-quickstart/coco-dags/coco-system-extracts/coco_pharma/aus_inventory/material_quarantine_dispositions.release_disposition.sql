-- Extract: Austin Inventory (Coco core) -> Material Quarantine Dispositions / release_disposition
-- Source: coco_pharma.aus_inventory (System::aus-inventory)
-- Target: coco_data_hub.material_quarantine_dispositions.release_disposition
-- lot_disposition; decision words normalised, MM/DD/YYYY expiry parsed.
SELECT
  d.lot_no::varchar(40)               AS lot_identifier,
  d.disp_utc                          AS lot_disposition_timestamp,
  (CASE d.decision WHEN 'RELEASE' THEN 'released for use' ELSE 'rejected' END)::varchar(20) AS lot_disposition_status,
  d.lab_result_ref::varchar(40)       AS test_result_identifier,
  to_date(d.expiry, 'MM/DD/YYYY')     AS lot_expiry_date,
  round(d.qty_released)::integer      AS lot_released_quantity
FROM aus_inventory.lot_disposition d
