-- Subscription: coco_austin_haz_mat__product_master_data - Austin HazMat Inventory (Coco core) receives Product Master Data
-- Destination: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Why it subscribes: Transport Classifications depends on it (product handling requirements)
-- Keeps the name and handling requirements of the shared Coco products made at the Austin site (3000 Cozaar,
-- 2050 Plavix, 9000 Cisplatin) in product_handling (NEW), from which they are classified for transport
-- (dot_classification).  Discards the other Coco products (classified by Coco HazMat Inventory), Austin's own
-- products (AU-, outside the manufacturing integration), and the pack and market details.

UPDATE incoming_product_definition SET discard_reason = 'Austin''s own product - outside the manufacturing integration'
 WHERE product_code !~ '^[0-9]{4}$';
UPDATE incoming_product_definition SET discard_reason = 'not made at the Austin site - classified by Coco HazMat Inventory'
 WHERE discard_reason IS NULL AND product_code NOT IN ('3000', '2050', '9000');
UPDATE incoming_handling_requirement SET discard_reason = 'Austin''s own product - outside the manufacturing integration'
 WHERE product_code !~ '^[0-9]{4}$';
UPDATE incoming_handling_requirement SET discard_reason = 'not made at the Austin site - classified by Coco HazMat Inventory'
 WHERE discard_reason IS NULL AND product_code NOT IN ('3000', '2050', '9000');

INSERT INTO austin_haz_mat.product_handling (product_code, product_name)
SELECT d.product_code, d.product_name FROM incoming_product_definition d WHERE d.discard_reason IS NULL
ON CONFLICT (product_code) DO UPDATE SET product_name = EXCLUDED.product_name;

INSERT INTO austin_haz_mat.product_handling (product_code, un_number, min_temp_c, max_temp_c, packaging)
SELECT h.product_code, h.product_hazard_code, h.product_storage_minimum_temperature, h.product_storage_maximum_temperature,
       h.product_packaging_description
  FROM incoming_handling_requirement h
 WHERE h.discard_reason IS NULL
ON CONFLICT (product_code) DO UPDATE SET un_number = EXCLUDED.un_number, min_temp_c = EXCLUDED.min_temp_c,
       max_temp_c = EXCLUDED.max_temp_c, packaging = EXCLUDED.packaging;

UPDATE incoming_pack_configuration SET discard_reason = 'pack details are not needed for transport classification';
UPDATE incoming_authorised_market_assignment SET discard_reason = 'market authorisations are not needed for transport classification';
