-- Extract: Coco Product Management (Coco core) -> Product Master Data / handling_requirement
-- Source: coco_pharma.coco_products (System::cocoProducts)
-- Target: coco_data_hub.product_master_data.handling_requirement
-- prd_hndl; shelf life months converted to days (30 per month).
SELECT
  h.prd_cd::varchar(20)          AS product_code,
  h.store_min_c::double precision AS product_storage_minimum_temperature,
  h.store_max_c::double precision AS product_storage_maximum_temperature,
  h.un_no::varchar(20)           AS product_hazard_code,
  h.pkg_note                     AS product_packaging_description,
  (h.shelf_life_mths * 30)::integer AS product_expiry_duration
FROM coco_products.prd_hndl h
