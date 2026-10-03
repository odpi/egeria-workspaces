-- Subscription: coco_austin_haz_mat__hazardous_material_holdings - Austin HazMat Inventory (Coco core) receives Hazardous Material Holdings
-- Destination: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Why it subscribes: Occupational Exposure Bands (substance holdings) and Transport Classifications (substance identity) depend on it
-- Keeps nothing: the Austin site's chemical holdings and hazard data are this system's own (storage_location_qty,
-- chemical), so they come back as rows it already holds; the HM substances are held at Coco's other sites and
-- recorded by Coco HazMat Inventory.

UPDATE incoming_substance_holding h SET discard_reason = 'holding recorded in Austin HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM austin_haz_mat.storage_location_qty s WHERE s.chem_id = h.substance_code AND s.storage_loc = h.warehouse_code);
UPDATE incoming_substance_holding SET discard_reason = 'held at another Coco site - recorded by Coco HazMat Inventory'
 WHERE discard_reason IS NULL;

UPDATE incoming_substance_hazard_data d SET discard_reason = 'chemical recorded in Austin HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM austin_haz_mat.chemical c WHERE c.chem_id = d.substance_code);
UPDATE incoming_substance_hazard_data SET discard_reason = 'held at another Coco site - recorded by Coco HazMat Inventory'
 WHERE discard_reason IS NULL;
