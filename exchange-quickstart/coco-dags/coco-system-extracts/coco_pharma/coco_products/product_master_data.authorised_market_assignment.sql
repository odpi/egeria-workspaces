-- Extract: Coco Product Management (Coco core) -> Product Master Data / authorised_market_assignment
-- Source: coco_pharma.coco_products (System::cocoProducts)
-- Target: coco_data_hub.product_master_data.authorised_market_assignment
-- prd_mkt_auth; UK market code to ISO GB.
SELECT
  a.prd_cd::varchar(20)          AS product_code,
  (CASE a.mkt WHEN 'UK' THEN 'GB' ELSE a.mkt END)::varchar(8) AS market_code,
  a.ma_no::varchar(40)           AS authorisation_identifier,
  a.start_dt                     AS authorisation_start_date,
  a.end_dt                       AS authorisation_end_date
FROM coco_products.prd_mkt_auth a
