-- Extract: Coco Pharmaceuticals Procurement (Coco core) -> Supplier Master Data / supplier_payment_details
-- Source: coco_pharma.procurement01 (System::procurement01)
-- Target: coco_data_hub.supplier_master_data.supplier_payment_details
-- active vendor_bank row per vendor; country names to ISO codes.
SELECT
  b.vendor_no::varchar(40)       AS supplier_identifier,
  b.acct_masked::varchar(40)     AS bank_account_current_identifier,
  b.bank_name::varchar(120)      AS bank_account_provider_name,
  (CASE b.bank_country WHEN 'UK' THEN 'GB' WHEN 'USA' THEN 'US' WHEN 'Netherland' THEN 'NL' WHEN 'Germany' THEN 'DE' WHEN 'India' THEN 'IN'
               WHEN 'Brazil' THEN 'BR' WHEN 'Sweden' THEN 'SE' WHEN 'Malta' THEN 'MT' ELSE b.bank_country END)::varchar(60) AS bank_account_country,
  b.change_ref::varchar(40)      AS payment_detail_change_identifier,
  b.verified_on                  AS payment_detail_verified_date
FROM procurement01.vendor_bank b
WHERE b.active_ind = 'Y'
