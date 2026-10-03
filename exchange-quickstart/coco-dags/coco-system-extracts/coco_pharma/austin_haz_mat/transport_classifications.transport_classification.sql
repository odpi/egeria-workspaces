-- Extract: Austin HazMat Inventory (Coco core) -> Transport Classifications / transport_classification
-- Source: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Target: coco_data_hub.transport_classifications.transport_classification
-- dot_classification as is.
SELECT
  d.class_id::varchar(40)          AS transport_classification_identifier,
  d.chem_id::varchar(20)           AS substance_code,
  d.product_code::varchar(20)      AS product_code,
  d.shipped_form::text             AS substance_form_description,
  d.un_number::varchar(20)         AS transport_classification_code,
  d.packing_group::varchar(5)      AS transport_classification_packing_group_code,
  d.hazard_class::varchar(10)      AS transport_classification_hazard_class_code,
  d.label_text                     AS transport_classification_labelling_description,
  d.shipping_docs                  AS transport_classification_documentation_description,
  d.classified_on                  AS transport_classification_date
FROM austin_haz_mat.dot_classification d
