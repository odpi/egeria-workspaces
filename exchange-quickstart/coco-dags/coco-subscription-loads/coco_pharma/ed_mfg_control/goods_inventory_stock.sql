-- Subscription: coco_ed_mfg_control__goods_inventory_stock - Edmonton Manufacturing Control System (Coco core) receives Goods Inventory Stock
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Batch Execution Records depends on it (issue material)
-- Keeps the issues of component lots to Edmonton lots in component_issue (NEW), reconciled against consumption.
-- Discards stock positions and other movements (stock is kept by Coco Inventory, not the control system) and
-- issues to other factories' batches.

UPDATE incoming_stock_position SET discard_reason = 'stock levels are kept by the inventory systems, not the control system';
UPDATE incoming_stock_movement SET discard_reason = 'stock movements are kept by the inventory systems, not the control system';

UPDATE incoming_material_issue m SET discard_reason = 'issue to a batch of another factory' WHERE NOT (EXISTS (SELECT 1 FROM ed_mfg_control.prod_lot p WHERE p.lot_id = m.batch_identifier) OR m.batch_identifier ~ '^E[0-9]{2}-');

INSERT INTO ed_mfg_control.component_issue (movement_no, lot_id, item_no, component_lot, qty_issued, quarantine_status)
SELECT m.stock_movement_identifier, m.batch_identifier, m.raw_material_code, m.lot_identifier, m.raw_material_issued_quantity,
       initcap(m.lot_quarantine_status)
  FROM incoming_material_issue m
 WHERE m.discard_reason IS NULL
ON CONFLICT (movement_no) DO UPDATE SET lot_id = EXCLUDED.lot_id, item_no = EXCLUDED.item_no, component_lot = EXCLUDED.component_lot,
       qty_issued = EXCLUDED.qty_issued, quarantine_status = EXCLUDED.quarantine_status;
