-- Extract: Coco HazMat Inventory (Coco core) -> Occupational Exposure Bands / band_containment_requirement
-- Source: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Target: coco_data_hub.occupational_exposure_bands.band_containment_requirement
-- hm_band as is.
SELECT
  b.band_cd::varchar(10)           AS band_code,
  b.oel_max::double precision      AS band_maximum_value,
  b.oel_unit::varchar(20)          AS band_unit,
  b.contain_desc                   AS band_containment_description
FROM coco_haz_mat.hm_band b
