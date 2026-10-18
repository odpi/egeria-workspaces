-- Extract: Coco Product Management (Coco core) -> Product Master Data / pack_configuration
-- Source: coco_pharma.coco_products (System::cocoProducts)
-- Target: coco_data_hub.product_master_data.pack_configuration
-- prd_pack; UK market code to ISO GB, Y/N serialisation flag to boolean.
SELECT
  k.pack_cd::varchar(20)         AS pack_code,
  k.prd_cd::varchar(20)          AS product_code,
  k.pack_desc::text              AS pack_description,
  k.units_per_pack::integer      AS pack_quantity,
  (CASE k.dest_mkt WHEN 'UK' THEN 'GB' ELSE k.dest_mkt END)::varchar(8) AS pack_destination_code,
  (k.serial_yn = 'Y')            AS pack_serialised_flag
FROM coco_products.prd_pack k
