-- Extract: Manhattan WMS (Austin) -> Goods Inventory Stock / stock_position
-- Source: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Target: coco_data_hub.goods_inventory_stock.stock_position
-- wm_inventory summed per item and warehouse; the lot is given only where a single lot is held; min/max from
-- item_facility_mapping_wms.
SELECT
  i.item_name::varchar(20) AS product_code,
  f.whse::varchar(20) AS warehouse_code,
  (CASE WHEN count(DISTINCT w.batch_nbr) = 1 THEN max(w.batch_nbr) END)::varchar(40) AS lot_identifier,
  sum(w.on_hand_qty)::integer AS stock_level,
  m.min_invn_qty AS stock_minimum_level,
  m.max_invn_qty AS stock_maximum_level,
  max(w.last_updated_dttm) AS stock_current_timestamp
FROM manhattan_wms.wm_inventory w
JOIN manhattan_wms.item_cbo i ON i.item_id = w.item_id
JOIN manhattan_wms.facility f ON f.facility_id = w.c_facility_id
LEFT JOIN manhattan_wms.item_facility_mapping_wms m ON m.item_id = w.item_id AND m.facility_id = w.c_facility_id
GROUP BY i.item_name, f.whse, m.min_invn_qty, m.max_invn_qty
