-- Subscription: coco_winch_mfg_control__goods_inventory_stock - Winchester Manufacturing Control System (Coco core) receives Goods Inventory Stock
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Batch Execution Records depends on it (issue material)
-- Keeps the issues of material lots to Winchester batches in wmat_iss (NEW, quarantine status as R/H/X), which
-- the step's material check reconciles against wmatl.  Discards stock positions and other movements (stock is
-- kept by Coco Inventory, not the control system) and issues to other factories' batches.

UPDATE incoming_stock_position SET discard_reason = 'stock levels are kept by the inventory systems, not the control system';
UPDATE incoming_stock_movement SET discard_reason = 'stock movements are kept by the inventory systems, not the control system';

UPDATE incoming_material_issue m SET discard_reason = 'issue to a batch of another factory'
 WHERE NOT (EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = m.batch_identifier) OR m.batch_identifier ~ '^W[0-9]{2}-');

INSERT INTO winch_mfg_control.wmat_iss (mvmt_ref, batch_no, mat_cd, lot_no, qty, q_sts)
SELECT m.stock_movement_identifier, m.batch_identifier, m.raw_material_code, m.lot_identifier, m.raw_material_issued_quantity,
       (CASE m.lot_quarantine_status WHEN 'released' THEN 'R' WHEN 'rejected' THEN 'X' ELSE 'H' END)
  FROM incoming_material_issue m
 WHERE m.discard_reason IS NULL
ON CONFLICT (mvmt_ref) DO UPDATE SET batch_no = EXCLUDED.batch_no, mat_cd = EXCLUDED.mat_cd, lot_no = EXCLUDED.lot_no,
       qty = EXCLUDED.qty, q_sts = EXCLUDED.q_sts;
