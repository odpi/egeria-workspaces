-- Extract: Coco Product Management (Coco core) -> Product Master Data / product_definition
-- Source: coco_pharma.coco_products (System::cocoProducts)
-- Target: coco_data_hub.product_master_data.product_definition
-- prd_mstr; type and status codes expanded.
SELECT
  p.prd_cd::varchar(20)          AS product_code,
  p.prd_nm::varchar(120)         AS product_name,
  p.prd_desc                     AS product_description,
  (CASE p.prd_typ WHEN 'S' THEN 'standard' WHEN 'P' THEN 'personalised' WHEN 'I' THEN 'investigational' END)::varchar(40) AS product_type,
  p.actv_ingr::varchar(120)      AS active_ingredient_name,
  p.strgth::varchar(40)          AS product_strength,
  (CASE p.sts_cd WHEN 'DEV' THEN 'in development' WHEN 'MKT' THEN 'marketed' WHEN 'SUS' THEN 'suspended' WHEN 'WDN' THEN 'withdrawn' END)::varchar(20) AS product_current_status,
  p.cur_ver::varchar(20)         AS product_current_version
FROM coco_products.prd_mstr p
