-- Extract: Austin HazMat Inventory (Coco core) -> Hazardous Material Holdings / substance_holding
-- Source: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Target: coco_data_hub.hazardous_material_holdings.substance_holding
-- storage_location_qty; US units converted (GAL to L), unit words lower-cased, physical state expanded.
SELECT
  s.chem_id::varchar(20)           AS substance_code,
  s.storage_loc::varchar(20)       AS warehouse_code,
  (CASE s.unit WHEN 'GAL' THEN round(s.qty_on_hand * 3.78541, 1) ELSE s.qty_on_hand END)::double precision AS substance_quantity,
  (CASE s.unit WHEN 'GAL' THEN 'L' ELSE lower(s.unit) END)::varchar(20) AS substance_unit,
  (CASE s.physical_state WHEN 'S' THEN 'solid (powder)' WHEN 'L' THEN 'liquid' WHEN 'G' THEN 'gas' END)::text AS substance_form_description,
  s.last_count                     AS substance_current_timestamp
FROM austin_haz_mat.storage_location_qty s
