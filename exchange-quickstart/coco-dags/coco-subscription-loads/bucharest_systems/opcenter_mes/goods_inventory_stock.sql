-- Subscription: buc_opcenter_mes__goods_inventory_stock - Siemens Opcenter MES (Bucharest) receives Goods Inventory Stock
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Batch Execution Records depends on it (issue material)
-- Keeps the WMS stock of EKG raw materials and packaging (RO10 zones; finished products are not issued to production)
-- in the new table materialinventory, used to check component availability before a batch starts.  Movements are the
-- WMS's business, and issues to MES batches are already recorded by the MES itself (componentissuehistory), so both are
-- discarded; other sites' stock is discarded (Coco group data - EKG is not yet integrated).
UPDATE incoming_stock_position SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE warehouse_code IS NULL OR warehouse_code NOT LIKE 'RO10-%';
UPDATE incoming_stock_position SET discard_reason = 'finished product - not issued to production'
 WHERE discard_reason IS NULL AND product_code LIKE 'PF-%';
UPDATE incoming_stock_movement SET discard_reason = 'the MES keeps stock levels, not WMS movements'
 WHERE warehouse_code LIKE 'RO10-%';
UPDATE incoming_stock_movement SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_material_issue i SET discard_reason = 'issue already recorded by the MES (componentissuehistory)'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_material_issue SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO opcenter_mes.materialinventory (productname, location, lot, qty, minqty, maxqty, wmsupdatedate)
SELECT i.product_code, i.warehouse_code, i.lot_identifier, coalesce(i.stock_level, 0), i.stock_minimum_level,
       i.stock_maximum_level, i.stock_current_timestamp
  FROM incoming_stock_position i
 WHERE i.discard_reason IS NULL
ON CONFLICT (productname, location) DO UPDATE
   SET lot = EXCLUDED.lot, qty = EXCLUDED.qty, minqty = EXCLUDED.minqty, maxqty = EXCLUDED.maxqty,
       wmsupdatedate = EXCLUDED.wmsupdatedate;
