-- Extract: Austin HazMat Inventory (Coco core) -> Occupational Exposure Bands / substance_exposure_band
-- Source: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Target: coco_data_hub.occupational_exposure_bands.substance_exposure_band
-- chemical rows with a band; band number rendered in the Coco OEBn form (bands themselves come from the Coco HazMat Inventory).
SELECT
  c.chem_id::varchar(20)           AS substance_code,
  c.chem_name::varchar(200)        AS substance_name,
  ('OEB' || c.oeb)::varchar(10)    AS substance_banding_code,
  c.primary_hazard::varchar(20)    AS substance_hazard_code,
  c.oeb_assigned                   AS substance_banding_date,
  c.incident_no::varchar(40)       AS incident_identifier
FROM austin_haz_mat.chemical c
WHERE c.oeb IS NOT NULL
