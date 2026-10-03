-- Extract: Coco HazMat Inventory (Coco core) -> Hazardous Material Holdings / substance_holding
-- Source: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Target: coco_data_hub.hazardous_material_holdings.substance_holding
-- hm_hold as is.
SELECT
  h.subst_cd::varchar(20)          AS substance_code,
  h.loc_cd::varchar(20)            AS warehouse_code,
  h.qty::double precision          AS substance_quantity,
  h.uom::varchar(20)               AS substance_unit,
  h.form_desc::text                AS substance_form_description,
  h.upd_ts                         AS substance_current_timestamp
FROM coco_haz_mat.hm_hold h
