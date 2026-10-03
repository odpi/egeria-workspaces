-- Subscription: coco_aus_inventory__material_quarantine_dispositions - Austin Inventory (Coco core) receives Material Quarantine Dispositions
-- Destination: coco_pharma.aus_inventory (System::aus-inventory)
-- Why it subscribes: Goods Inventory Stock depends on it (release for use)
-- Keeps nothing: quarantine and disposition of lots received at the Austin site are recorded in Austin Inventory
-- itself (lot_status, lot_disposition), so they come back as rows it already holds; the other lots are at
-- Coco Inventory's locations, in Austin's own SAP stock (AUS1) or EKG's.

UPDATE incoming_quarantine_record q SET discard_reason = 'quarantine recorded in Austin Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM aus_inventory.lot_status l WHERE l.lot_no = q.lot_identifier);
UPDATE incoming_quarantine_record SET discard_reason = 'Austin''s own SAP stock - not tracked by Austin Inventory'
 WHERE discard_reason IS NULL AND warehouse_code IN ('AUS1', 'AUS2');
UPDATE incoming_quarantine_record SET discard_reason = 'lot at another location' WHERE discard_reason IS NULL;

UPDATE incoming_release_disposition d SET discard_reason = 'disposition recorded in Austin Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM aus_inventory.lot_status l WHERE l.lot_no = d.lot_identifier);
UPDATE incoming_release_disposition SET discard_reason = 'lot not held in Austin Inventory' WHERE discard_reason IS NULL;
