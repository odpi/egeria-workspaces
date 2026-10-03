-- Extract: Coco Pharmaceuticals Procurement (Coco core) -> Supplier Master Data / supplier
-- Source: coco_pharma.procurement01 (System::procurement01)
-- Target: coco_data_hub.supplier_master_data.supplier
-- vendor; class and status codes expanded, country names to ISO codes.
SELECT
  v.vendor_no::varchar(40)       AS supplier_identifier,
  v.vendor_name::varchar(200)    AS supplier_name,
  (CASE v.vendor_class WHEN 'MAT' THEN 'material supplier' WHEN 'SVC' THEN 'service provider'
                       WHEN 'HCO' THEN 'healthcare organisation' ELSE 'other' END)::varchar(40) AS supplier_type,
  (CASE v.inc_country WHEN 'UK' THEN 'GB' WHEN 'USA' THEN 'US' WHEN 'Netherland' THEN 'NL' WHEN 'Germany' THEN 'DE' WHEN 'India' THEN 'IN'
               WHEN 'Brazil' THEN 'BR' WHEN 'Sweden' THEN 'SE' WHEN 'Malta' THEN 'MT' ELSE v.inc_country END)::varchar(60) AS supplier_country,
  (v.approved_ind = 'Y')         AS supplier_approved_flag,
  v.approved_on                  AS supplier_approved_date,
  (CASE v.vendor_status WHEN 'A' THEN 'active' WHEN 'S' THEN 'suspended' ELSE 'closed' END)::varchar(20) AS supplier_current_status
FROM procurement01.vendor v
