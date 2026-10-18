-- Extract: Austin HazMat Inventory (Coco core) -> Hazardous Material Holdings / substance_hazard_data
-- Source: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Target: coco_data_hub.hazardous_material_holdings.substance_hazard_data
-- chemical; band and UN number of the chemical's own shipped form.
SELECT
  c.chem_id::varchar(20)           AS substance_code,
  c.chem_name::varchar(200)        AS substance_name,
  c.primary_hazard::varchar(20)    AS substance_hazard_code,
  c.hazard_statement               AS substance_hazard_description,
  (CASE WHEN c.oeb IS NOT NULL THEN 'OEB' || c.oeb END)::varchar(10) AS substance_banding_code,
  (SELECT min(d.un_number) FROM austin_haz_mat.dot_classification d WHERE d.chem_id = c.chem_id)::varchar(20) AS substance_transport_code
FROM austin_haz_mat.chemical c
