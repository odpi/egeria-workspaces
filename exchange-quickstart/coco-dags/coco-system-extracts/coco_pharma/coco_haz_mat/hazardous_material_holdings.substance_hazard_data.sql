-- Extract: Coco HazMat Inventory (Coco core) -> Hazardous Material Holdings / substance_hazard_data
-- Source: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Target: coco_data_hub.hazardous_material_holdings.substance_hazard_data
-- hm_subst; transport code resolved to the UN number via hm_tpt.
SELECT
  h.subst_cd::varchar(20)          AS substance_code,
  h.subst_nm::varchar(200)         AS substance_name,
  h.ghs_cls::varchar(20)           AS substance_hazard_code,
  h.haz_desc                       AS substance_hazard_description,
  h.oeb_cd::varchar(10)            AS substance_banding_code,
  t.un_no::varchar(20)             AS substance_transport_code
FROM coco_haz_mat.hm_subst h
LEFT JOIN coco_haz_mat.hm_tpt t ON t.tpt_id = h.tpt_ref
