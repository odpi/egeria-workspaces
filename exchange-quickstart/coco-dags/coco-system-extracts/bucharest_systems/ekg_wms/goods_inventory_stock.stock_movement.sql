-- Extract: Warehouse Management System (WMS) (Bucharest) -> Goods Inventory Stock / stock_movement
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.goods_inventory_stock.stock_movement
-- miscari; movement type codes translated; local-time text to UTC; zone prefixed with the plant.
SELECT
  m.id_misc::varchar(40) AS stock_movement_identifier,
  m.cod_art::varchar(20) AS product_code,
  m.lot::varchar(40) AS lot_identifier,
  (CASE m.tip WHEN 'INTRARE' THEN 'receipt' WHEN 'INTRARE_PF' THEN 'production receipt' WHEN 'TRANSFER' THEN 'transfer'
        WHEN 'CONSUM' THEN 'issue' WHEN 'LIVRARE' THEN 'despatch' ELSE lower(m.tip) END)::varchar(20) AS stock_movement_type,
  m.cant AS stock_movement_quantity,
  (to_timestamp(m.data_misc, 'DD.MM.YYYY HH24:MI')::timestamp AT TIME ZONE 'Europe/Bucharest') AS stock_movement_timestamp,
  ('RO10-' || m.depozit)::varchar(20) AS warehouse_code
FROM ekg_wms.miscari m
