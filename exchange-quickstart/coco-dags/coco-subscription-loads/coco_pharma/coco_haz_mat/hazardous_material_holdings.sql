-- Subscription: coco_haz_mat__hazardous_material_holdings - Coco HazMat Inventory (Coco core) receives Hazardous Material Holdings
-- Destination: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Why it subscribes: Occupational Exposure Bands (substance holdings) and Transport Classifications (substance identity) depend on it
-- Keeps nothing: the holdings and hazard data of substances at Coco's non-Austin sites are this system's own
-- (hm_hold, hm_subst), so they come back as rows it already holds; the AHM- substances are held at the Austin
-- site and recorded by Austin HazMat Inventory.

UPDATE incoming_substance_holding h SET discard_reason = 'holding recorded in Coco HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_haz_mat.hm_hold o WHERE o.subst_cd = h.substance_code AND o.loc_cd = h.warehouse_code);
UPDATE incoming_substance_holding SET discard_reason = 'Austin site holding - recorded by Austin HazMat Inventory'
 WHERE discard_reason IS NULL;

UPDATE incoming_substance_hazard_data d SET discard_reason = 'substance recorded in Coco HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_haz_mat.hm_subst s WHERE s.subst_cd = d.substance_code);
UPDATE incoming_substance_hazard_data SET discard_reason = 'Austin site substance - recorded by Austin HazMat Inventory'
 WHERE discard_reason IS NULL;
