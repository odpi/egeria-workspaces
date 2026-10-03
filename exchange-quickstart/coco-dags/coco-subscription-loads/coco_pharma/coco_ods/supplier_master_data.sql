-- Subscription: coco_ods__supplier_master_data - Coco Pharmaceuticals Operational Data Store (Coco core) receives Supplier Master Data
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills suppliers
-- Keeps Coco suppliers (numeric ids below 100000) in suppliers: company name and country (in the ODS's own
-- country names); new suppliers are added without contact or address, which no product supplies.  Discards
-- Austin (100xxx) and EKG (700xxx) suppliers, which are not Coco's and do not fit supplier_id, and the screening
-- and bank details, which the ODS does not hold.

UPDATE incoming_supplier SET discard_reason = 'Austin or EKG supplier - not a Coco supplier'
 WHERE coalesce((CASE WHEN supplier_identifier ~ '^[0-9]{1,5}$' THEN supplier_identifier::integer END), 99999) > 32767;

INSERT INTO coco_ods.suppliers (supplier_id, company_name, country)
SELECT s.supplier_identifier::smallint, left(s.supplier_name, 40),
       (CASE s.supplier_country WHEN 'GB' THEN 'UK' WHEN 'US' THEN 'USA' WHEN 'NL' THEN 'Netherland' WHEN 'DE' THEN 'Germany'
             WHEN 'IN' THEN 'India' WHEN 'BR' THEN 'Brazil' WHEN 'SE' THEN 'Sweden' ELSE left(s.supplier_country, 15) END)
  FROM incoming_supplier s
 WHERE s.discard_reason IS NULL
ON CONFLICT (supplier_id) DO UPDATE SET company_name = EXCLUDED.company_name, country = EXCLUDED.country;

UPDATE incoming_supplier_risk_status SET discard_reason = 'the ODS holds no supplier screening';
UPDATE incoming_supplier_payment_details SET discard_reason = 'the ODS holds no supplier bank details';
