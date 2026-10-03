-- Extract: Informatica MDM (Austin) -> Product Master Data / handling_requirement
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.product_master_data.handling_requirement
-- c_b_product_handling joined to its product.
SELECT
  p.product_cd::varchar(20) AS product_code,
  h.min_storage_temp_c::double precision AS product_storage_minimum_temperature,
  h.max_storage_temp_c::double precision AS product_storage_maximum_temperature,
  h.transport_hazard_cd::varchar(20) AS product_hazard_code,
  h.packaging_desc AS product_packaging_description,
  h.shelf_life_days AS product_expiry_duration
FROM informatica_mdm.c_b_product_handling h
JOIN informatica_mdm.c_b_product p ON p.rowid_object = h.rowid_product
WHERE h.hub_state_ind = 1
