-- Extract: Informatica MDM (Austin) -> Product Master Data / pack_configuration
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.product_master_data.pack_configuration
-- c_b_product_pack joined to its product; serialised Y/N to boolean.
SELECT
  k.pack_cd::varchar(20) AS pack_code,
  p.product_cd::varchar(20) AS product_code,
  k.pack_desc AS pack_description,
  k.units_per_pack AS pack_quantity,
  k.destination_mkt_cd::varchar(8) AS pack_destination_code,
  (k.serialised_ind = 'Y') AS pack_serialised_flag
FROM informatica_mdm.c_b_product_pack k
JOIN informatica_mdm.c_b_product p ON p.rowid_object = k.rowid_product
WHERE k.hub_state_ind = 1
