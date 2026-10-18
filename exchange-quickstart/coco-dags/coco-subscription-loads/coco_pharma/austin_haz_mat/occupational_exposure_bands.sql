-- Subscription: coco_austin_haz_mat__occupational_exposure_bands - Austin HazMat Inventory (Coco core) receives Occupational Exposure Bands
-- Destination: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Why it subscribes: Transport Classifications depends on it (shared substance classification)
-- Keeps Coco's band definitions (OEB1-OEB5 with exposure limit and containment, defined in Coco HazMat
-- Inventory) in oeb_band (NEW), so the band numbers in chemical.oeb carry the same meaning at Austin.  Discards
-- the substance bands: the Austin site's are this system's own (chemical.oeb) and the HM substances are banded
-- by Coco HazMat Inventory for the other sites.

UPDATE incoming_substance_exposure_band b SET discard_reason = 'band recorded in Austin HazMat Inventory - supplied by this system'
 WHERE EXISTS (SELECT 1 FROM austin_haz_mat.chemical c WHERE c.chem_id = b.substance_code);
UPDATE incoming_substance_exposure_band SET discard_reason = 'held at another Coco site - banded by Coco HazMat Inventory'
 WHERE discard_reason IS NULL;

UPDATE incoming_band_containment_requirement SET discard_reason = 'not an OEB1-OEB5 band'
 WHERE band_code !~ '^OEB[1-5]$';

INSERT INTO austin_haz_mat.oeb_band (oeb, oel_upper, oel_unit, containment)
SELECT substr(r.band_code, 4)::smallint, r.band_maximum_value, r.band_unit, r.band_containment_description
  FROM incoming_band_containment_requirement r
 WHERE r.discard_reason IS NULL
ON CONFLICT (oeb) DO UPDATE SET oel_upper = EXCLUDED.oel_upper, oel_unit = EXCLUDED.oel_unit, containment = EXCLUDED.containment;
