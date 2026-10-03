-- Extract: Coco HazMat Inventory (Coco core) -> Transport Classifications / transport_classification
-- Source: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Target: coco_data_hub.transport_classifications.transport_classification
-- hm_tpt as is.
SELECT
  t.tpt_id::varchar(40)            AS transport_classification_identifier,
  t.subst_cd::varchar(20)          AS substance_code,
  t.prd_cd::varchar(20)            AS product_code,
  t.form_desc::text                AS substance_form_description,
  t.un_no::varchar(20)             AS transport_classification_code,
  t.pkg_grp::varchar(5)            AS transport_classification_packing_group_code,
  t.haz_cls::varchar(10)           AS transport_classification_hazard_class_code,
  t.lbl_desc                       AS transport_classification_labelling_description,
  t.docs_desc                      AS transport_classification_documentation_description,
  t.deriv_dt                       AS transport_classification_date
FROM coco_haz_mat.hm_tpt t
