-- Subscription: coco_haz_mat__product_master_data - Coco HazMat Inventory (Coco core) receives Product Master Data
-- Destination: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Why it subscribes: Transport Classifications depends on it (product handling requirements)
-- Keeps the name and handling requirements (UN number, storage temperatures, packaging) of the Coco products
-- made or stored at the non-Austin sites in hm_prd_hndl (NEW), from which products are classified for transport.
-- Discards the products made at the Austin site (3000, 2050, 9000 - Austin HazMat Inventory's), Austin's own
-- products (AU-), and the pack and market details, which classification does not need.

UPDATE incoming_product_definition SET discard_reason = 'Austin''s own product - not a Coco product'
 WHERE product_code !~ '^[0-9]{4}$';
UPDATE incoming_product_definition SET discard_reason = 'made at the Austin site - classified by Austin HazMat Inventory'
 WHERE discard_reason IS NULL AND product_code IN ('3000', '2050', '9000');
UPDATE incoming_handling_requirement SET discard_reason = 'Austin''s own product - not a Coco product'
 WHERE product_code !~ '^[0-9]{4}$';
UPDATE incoming_handling_requirement SET discard_reason = 'made at the Austin site - classified by Austin HazMat Inventory'
 WHERE discard_reason IS NULL AND product_code IN ('3000', '2050', '9000');

INSERT INTO coco_haz_mat.hm_prd_hndl (prd_cd, prd_nm)
SELECT d.product_code, d.product_name FROM incoming_product_definition d WHERE d.discard_reason IS NULL
ON CONFLICT (prd_cd) DO UPDATE SET prd_nm = EXCLUDED.prd_nm;

INSERT INTO coco_haz_mat.hm_prd_hndl (prd_cd, un_no, store_min_c, store_max_c, pkg_note)
SELECT h.product_code, h.product_hazard_code, h.product_storage_minimum_temperature, h.product_storage_maximum_temperature,
       h.product_packaging_description
  FROM incoming_handling_requirement h
 WHERE h.discard_reason IS NULL
ON CONFLICT (prd_cd) DO UPDATE SET un_no = EXCLUDED.un_no, store_min_c = EXCLUDED.store_min_c, store_max_c = EXCLUDED.store_max_c,
       pkg_note = EXCLUDED.pkg_note;

UPDATE incoming_pack_configuration SET discard_reason = 'pack details are not needed for transport classification';
UPDATE incoming_authorised_market_assignment SET discard_reason = 'market authorisations are not needed for transport classification';
