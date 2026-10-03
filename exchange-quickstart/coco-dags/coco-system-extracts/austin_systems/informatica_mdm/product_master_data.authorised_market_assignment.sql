-- Extract: Informatica MDM (Austin) -> Product Master Data / authorised_market_assignment
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.product_master_data.authorised_market_assignment
-- c_b_product_mkt_auth joined to its product.
SELECT
  p.product_cd::varchar(20) AS product_code,
  a.market_cd::varchar(8) AS market_code,
  a.authorisation_no::varchar(40) AS authorisation_identifier,
  a.start_dt AS authorisation_start_date,
  a.end_dt AS authorisation_end_date
FROM informatica_mdm.c_b_product_mkt_auth a
JOIN informatica_mdm.c_b_product p ON p.rowid_object = a.rowid_product
WHERE a.hub_state_ind = 1
