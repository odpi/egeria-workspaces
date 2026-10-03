-- Extract: Manhattan WMS (Austin) -> Goods Inventory Stock / stock_movement
-- Source: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Target: coco_data_hub.goods_inventory_stock.stock_movement
-- pix_tran; transaction type/code translated to receipt, issue, transfer, adjustment or shipment; quantity signed by
-- adjustment type.
SELECT
  p.pix_tran_id::varchar(40) AS stock_movement_identifier,
  p.item_name::varchar(20) AS product_code,
  p.batch_nbr::varchar(40) AS lot_identifier,
  (CASE WHEN p.tran_type = '100' THEN 'receipt'
        WHEN p.tran_type = '200' THEN 'transfer'
        WHEN p.tran_type = '300' AND p.tran_code = '01' THEN 'issue'
        WHEN p.tran_type = '300' THEN 'adjustment'
        ELSE 'shipment' END)::varchar(20) AS stock_movement_type,
  (CASE p.invn_adjmt_type WHEN 'S' THEN -p.invn_adjmt_qty ELSE p.invn_adjmt_qty END) AS stock_movement_quantity,
  p.create_date_time AS stock_movement_timestamp,
  p.whse::varchar(20) AS warehouse_code
FROM manhattan_wms.pix_tran p
