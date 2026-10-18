-- Extract: Coco HazMat Inventory (Coco core) -> Occupational Exposure Bands / substance_exposure_band
-- Source: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Target: coco_data_hub.occupational_exposure_bands.substance_exposure_band
-- hm_subst rows that have been banded.
SELECT
  h.subst_cd::varchar(20)          AS substance_code,
  h.subst_nm::varchar(200)         AS substance_name,
  h.oeb_cd::varchar(10)            AS substance_banding_code,
  h.ghs_cls::varchar(20)           AS substance_hazard_code,
  h.oeb_dt                         AS substance_banding_date,
  h.oeb_inc_ref::varchar(40)       AS incident_identifier
FROM coco_haz_mat.hm_subst h
WHERE h.oeb_cd IS NOT NULL
