-- Extract: Warehouse Management System (WMS) (Bucharest) -> Goods Inventory Stock / material_issue
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.goods_inventory_stock.material_issue
-- CONSUM movements (ref_doc = production batch); the lot's quarantine state at issue from carantina (lots received
-- before 2026 predate the quarantine table and were released).
SELECT
  m.id_misc::varchar(40) AS stock_movement_identifier,
  m.ref_doc::varchar(40) AS batch_identifier,
  m.cod_art::varchar(20) AS raw_material_code,
  m.lot::varchar(40) AS lot_identifier,
  m.cant AS raw_material_issued_quantity,
  (CASE coalesce(c.stare, 'E') WHEN 'E' THEN 'released' WHEN 'C' THEN 'quarantined' ELSE 'rejected' END)::varchar(20) AS lot_quarantine_status
FROM ekg_wms.miscari m
LEFT JOIN ekg_wms.carantina c ON c.lot_intern = m.lot
WHERE m.tip = 'CONSUM'
