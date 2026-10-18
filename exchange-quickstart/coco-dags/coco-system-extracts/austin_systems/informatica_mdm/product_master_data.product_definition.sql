-- Extract: Informatica MDM (Austin) -> Product Master Data / product_definition
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.product_master_data.product_definition
-- Active c_b_product golden records; type and lifecycle codes to lower-case words.
SELECT
  p.product_cd::varchar(20) AS product_code,
  p.product_nm::varchar(120) AS product_name,
  p.product_desc AS product_description,
  lower(p.product_type_cd)::varchar(40) AS product_type,
  p.active_ingredient_nm::varchar(120) AS active_ingredient_name,
  p.strength_txt::varchar(40) AS product_strength,
  lower(p.lifecycle_status_cd)::varchar(20) AS product_current_status,
  p.version_no::varchar(20) AS product_current_version
FROM informatica_mdm.c_b_product p
WHERE p.hub_state_ind = 1
