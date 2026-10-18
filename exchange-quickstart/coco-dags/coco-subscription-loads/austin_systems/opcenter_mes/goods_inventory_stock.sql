-- Subscription: aus_opcenter_mes__goods_inventory_stock - Siemens Opcenter MES (Austin) receives Goods Inventory Stock
-- Destination: austin_systems.opcenter_mes (SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601)
-- Why it subscribes: Batch Execution Records depends on it (issue material)
-- Keeps line-side availability: the stock positions of the Austin plant stores (AUS1) go to the NEW erpinventory
-- table that the weigh-and-dispense step checks. Finished goods at the distribution centre (AUS2), movement history
-- and the WMS's own copies of production issues (the MES records issues itself in componentissuehistory) are
-- discarded, as are Coco's Austin Inventory (AUS-*) and EKG rows.

UPDATE incoming_stock_position i SET discard_reason = 'other estate: not an Austin (Manhattan) warehouse'
 WHERE i.warehouse_code NOT IN ('AUS1', 'AUS2');
UPDATE incoming_stock_position i SET discard_reason = 'finished goods at the distribution centre, not line-side'
 WHERE i.discard_reason IS NULL AND i.warehouse_code = 'AUS2';
INSERT INTO opcenter_mes.erpinventory
       (productname, warehouse, lotname, qtyonhand, minqty, maxqty, lastupdated)
SELECT i.product_code, i.warehouse_code, i.lot_identifier, i.stock_level, i.stock_minimum_level,
       i.stock_maximum_level, i.stock_current_timestamp
  FROM incoming_stock_position i
 WHERE i.discard_reason IS NULL
ON CONFLICT (productname, warehouse) DO UPDATE SET
       lotname = EXCLUDED.lotname, qtyonhand = EXCLUDED.qtyonhand, minqty = EXCLUDED.minqty,
       maxqty = EXCLUDED.maxqty, lastupdated = EXCLUDED.lastupdated;

UPDATE incoming_stock_movement SET discard_reason = 'movement history not kept by the MES';

UPDATE incoming_material_issue i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_material_issue i SET discard_reason = 'other estate: Coco Austin Inventory record'
 WHERE i.discard_reason IS NULL AND i.stock_movement_identifier !~ '^[0-9]+$';
UPDATE incoming_material_issue SET discard_reason = 'already held: issue recorded by the MES (component issue)'
 WHERE discard_reason IS NULL;
