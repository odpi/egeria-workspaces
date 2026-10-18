-- Extract: Informatica MDM (Austin) -> Product Change Notifications / product_change
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.product_change_notifications.product_change
-- c_b_product_change joined to its product.
SELECT
  c.change_ref::varchar(40) AS product_change_identifier,
  p.product_cd::varchar(20) AS product_code,
  c.change_desc AS product_change_description,
  c.effective_dt AS product_change_start_date,
  c.published_ts AS product_change_published_timestamp
FROM informatica_mdm.c_b_product_change c
JOIN informatica_mdm.c_b_product p ON p.rowid_object = c.rowid_product
