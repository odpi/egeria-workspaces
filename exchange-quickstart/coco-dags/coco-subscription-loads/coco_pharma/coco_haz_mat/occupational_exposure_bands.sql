-- Subscription: coco_haz_mat__occupational_exposure_bands - Coco HazMat Inventory (Coco core) receives Occupational Exposure Bands
-- Destination: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Why it subscribes: Transport Classifications depends on it (shared substance classification)
-- Keeps nothing: the bands of substances at Coco's non-Austin sites and the band containment definitions are
-- this system's own (hm_subst.oeb_cd, hm_band), so they come back as rows it already holds; the AHM- substances
-- are banded by Austin HazMat Inventory for the Austin site.

UPDATE incoming_substance_exposure_band b SET discard_reason = 'band recorded in Coco HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_haz_mat.hm_subst s WHERE s.subst_cd = b.substance_code);
UPDATE incoming_substance_exposure_band SET discard_reason = 'Austin site substance - banded by Austin HazMat Inventory'
 WHERE discard_reason IS NULL;

UPDATE incoming_band_containment_requirement r SET discard_reason = 'band defined in Coco HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM coco_haz_mat.hm_band b WHERE b.band_cd = r.band_code);
UPDATE incoming_band_containment_requirement SET discard_reason = 'band not used by Coco HazMat Inventory'
 WHERE discard_reason IS NULL;
