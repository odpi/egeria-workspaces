-- Extract: Coco Inventory (Coco core) -> Material Quarantine Dispositions / release_disposition
-- Source: coco_pharma.coco_inventory (System::coco-inventory)
-- Target: coco_data_hub.material_quarantine_dispositions.release_disposition
-- inv_qdisp decisions only (interim HLD rows excluded).
SELECT
  d.lot_no::varchar(40)               AS lot_identifier,
  d.disp_ts                           AS lot_disposition_timestamp,
  (CASE d.disp WHEN 'REL' THEN 'released for use' ELSE 'rejected' END)::varchar(20) AS lot_disposition_status,
  d.lab_ref::varchar(40)              AS test_result_identifier,
  d.exp_dt                            AS lot_expiry_date,
  d.rel_qty::integer                  AS lot_released_quantity
FROM coco_inventory.inv_qdisp d
WHERE d.disp IN ('REL', 'REJ')
