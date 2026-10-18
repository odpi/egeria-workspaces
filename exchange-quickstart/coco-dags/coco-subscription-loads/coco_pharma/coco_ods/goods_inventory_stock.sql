-- Subscription: coco_ods__goods_inventory_stock - Coco Pharmaceuticals Operational Data Store (Coco core) receives Goods Inventory Stock
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills products (stock levels), supplies (stock levels)
-- Keeps finished-goods positions of Coco products at Coco locations (Winchester, Edmonton, Kansas City, Coco's
-- Austin stores): products.units_in_stock and reorder_level, summed per product and converted to the ODS's sales
-- unit (quantity_per_unit).  Discards raw materials (supplies has no material codes - no raw material master
-- product), Austin's own SAP and EKG stock, movements and issues.  Sums are per delivery, so a partial delivery
-- understates a product until its other locations are delivered again (the ODS has no per-location table).

UPDATE incoming_stock_position SET discard_reason = 'Austin''s own or EKG stock - not Coco''s'
 WHERE warehouse_code !~ '^(WIN|EDM|KC|AUS)-';
UPDATE incoming_stock_position SET discard_reason = 'raw material - supplies has no material codes (no raw material master product)'
 WHERE discard_reason IS NULL AND product_code !~ '^[0-9]{4}$';
UPDATE incoming_stock_position p SET discard_reason = 'product not in the ODS'
 WHERE p.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM coco_ods.products o WHERE o.product_id::text = p.product_code);

UPDATE coco_ods.products o
   SET units_in_stock = s.units, reorder_level = s.reorder
  FROM (SELECT o2.product_id,
               least(round(sum(p.stock_level) / max(coalesce(nullif(substring(o2.quantity_per_unit FROM '^[0-9]+'), '')::numeric, 1))), 32767)::smallint AS units,
               least(round(sum(coalesce(p.stock_minimum_level, 0)) / max(coalesce(nullif(substring(o2.quantity_per_unit FROM '^[0-9]+'), '')::numeric, 1))), 32767)::smallint AS reorder
          FROM incoming_stock_position p
          JOIN coco_ods.products o2 ON o2.product_id::text = p.product_code
         WHERE p.discard_reason IS NULL
         GROUP BY o2.product_id) s
 WHERE s.product_id = o.product_id
   AND (o.units_in_stock, o.reorder_level) IS DISTINCT FROM (s.units, s.reorder);

UPDATE incoming_stock_movement SET discard_reason = 'the ODS holds stock levels, not movements';
UPDATE incoming_material_issue SET discard_reason = 'the ODS holds stock levels, not issues to manufacturing';
