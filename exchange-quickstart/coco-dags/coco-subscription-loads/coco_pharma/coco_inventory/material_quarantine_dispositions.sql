-- Subscription: coco_inventory__material_quarantine_dispositions - Coco Inventory (Coco core) receives Material Quarantine Dispositions
-- Destination: coco_pharma.coco_inventory (System::coco-inventory)
-- Why it subscribes: Goods Inventory Stock depends on it (release for use)
-- Keeps nothing: quarantine records and decisions for lots at Coco's own locations are made in Coco Inventory
-- (inv_qrn, inv_qdisp), so they come back as rows it already holds; lots at the Austin site are Austin
-- Inventory's, and the AUS1 and RO10 lots are Austin's own SAP and EKG stock.

UPDATE incoming_quarantine_record q SET discard_reason = 'quarantine recorded in Coco Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_inventory.inv_qrn n WHERE n.lot_no = q.lot_identifier);
UPDATE incoming_quarantine_record SET discard_reason = 'Austin site lot - kept by Austin Inventory'
 WHERE discard_reason IS NULL AND warehouse_code LIKE 'AUS-%';
UPDATE incoming_quarantine_record SET discard_reason = 'Austin or EKG stock - not a Coco location' WHERE discard_reason IS NULL;

UPDATE incoming_release_disposition d SET discard_reason = 'disposition recorded in Coco Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_inventory.inv_qrn n WHERE n.lot_no = d.lot_identifier);
UPDATE incoming_release_disposition SET discard_reason = 'lot not held in Coco Inventory' WHERE discard_reason IS NULL;
