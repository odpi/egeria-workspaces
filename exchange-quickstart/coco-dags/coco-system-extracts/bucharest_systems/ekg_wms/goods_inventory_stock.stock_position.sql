-- Extract: Warehouse Management System (WMS) (Bucharest) -> Goods Inventory Stock / stock_position
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.goods_inventory_stock.stock_position
-- stoc aggregated per article and zone (the lot is given when a single lot is held); limits from articole; local time
-- to UTC.
SELECT
  s.cod_art::varchar(20) AS product_code,
  ('RO10-' || s.depozit)::varchar(20) AS warehouse_code,
  (CASE WHEN count(*) = 1 THEN min(s.lot) END)::varchar(40) AS lot_identifier,
  sum(s.cant)::integer AS stock_level,
  a.stoc_min AS stock_minimum_level,
  a.stoc_max AS stock_maximum_level,
  (max(s.actualizat) AT TIME ZONE 'Europe/Bucharest') AS stock_current_timestamp
FROM ekg_wms.stoc s
JOIN ekg_wms.articole a ON a.cod_art = s.cod_art
GROUP BY s.cod_art, s.depozit, a.stoc_min, a.stoc_max
