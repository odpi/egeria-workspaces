-- Extract: Manhattan WMS (Austin) -> Goods Inventory Stock / material_issue
-- Source: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Target: coco_data_hub.goods_inventory_stock.material_issue
-- Production issue PIX transactions (300/01, reason PI): ref_field_1 is the batch, ref_field_2 the lot status at
-- issue.
SELECT
  p.pix_tran_id::varchar(40) AS stock_movement_identifier,
  p.ref_field_1::varchar(40) AS batch_identifier,
  p.item_name::varchar(20) AS raw_material_code,
  p.batch_nbr::varchar(40) AS lot_identifier,
  p.invn_adjmt_qty AS raw_material_issued_quantity,
  (CASE p.ref_field_2 WHEN 'R' THEN 'released' WHEN 'Q' THEN 'held' ELSE 'rejected' END)::varchar(20) AS lot_quarantine_status
FROM manhattan_wms.pix_tran p
WHERE p.tran_type = '300' AND p.tran_code = '01' AND p.reason_code = 'PI'
