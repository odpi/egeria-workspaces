-- Subscription: coco_products__new_product_definitions - Coco Product Management (Coco core) receives New Product Definitions
-- Destination: coco_pharma.coco_products (System::cocoProducts)
-- Why it subscribes: Product Master Data depends on it (new product definition)
-- Keeps Coco product candidates with their presentations and specification in prd_cand, prd_cand_pack and
-- prd_cand_spec (all NEW); the board creates the prd_mstr and prd_pack entries from them, so the tables that
-- feed Product Master Data are not written directly.  Discards candidates whose code is not a Coco product code
-- (four digits; AU- and PF- codes belong to the acquired estates' own development).  No system supplies this
-- product yet, so nothing arrives today.

UPDATE incoming_candidate_product_definition SET discard_reason = 'not a Coco product code - acquired estate''s own development'
 WHERE product_code !~ '^[0-9]{4}$';

INSERT INTO coco_products.prd_cand (prd_cd, cand_ref, prd_nm, frml_ref, actv_ingr, strgth, trial_ref, hndovr_dt)
SELECT c.product_code, c.candidate_identifier, c.product_name, c.formulation_identifier, c.active_ingredient_name,
       c.product_strength, c.clinical_trial_identifier, c.candidate_handover_date
  FROM incoming_candidate_product_definition c
 WHERE c.discard_reason IS NULL
ON CONFLICT (prd_cd) DO UPDATE SET cand_ref = EXCLUDED.cand_ref, prd_nm = EXCLUDED.prd_nm, frml_ref = EXCLUDED.frml_ref,
       actv_ingr = EXCLUDED.actv_ingr, strgth = EXCLUDED.strgth, trial_ref = EXCLUDED.trial_ref, hndovr_dt = EXCLUDED.hndovr_dt;

UPDATE incoming_product_presentation p SET discard_reason = 'presentation of a candidate Coco Product Management does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_products.prd_cand c WHERE c.prd_cd = p.product_code);

INSERT INTO coco_products.prd_cand_pack (pack_cd, prd_cd, pack_desc, units_per_pack)
SELECT p.pack_code, p.product_code, p.pack_description, p.pack_quantity
  FROM incoming_product_presentation p
 WHERE p.discard_reason IS NULL
ON CONFLICT (pack_cd) DO UPDATE SET prd_cd = EXCLUDED.prd_cd, pack_desc = EXCLUDED.pack_desc, units_per_pack = EXCLUDED.units_per_pack;

UPDATE incoming_product_specification s SET discard_reason = 'specification of a candidate Coco Product Management does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_products.prd_cand c WHERE c.prd_cd = s.product_code);

INSERT INTO coco_products.prd_cand_spec (prd_cd, test_cd, spec_min, spec_max, test_uom)
SELECT s.product_code, s.test_code, s.specification_minimum_value, s.specification_maximum_value, s.test_unit
  FROM incoming_product_specification s
 WHERE s.discard_reason IS NULL
ON CONFLICT (prd_cd, test_cd) DO UPDATE SET spec_min = EXCLUDED.spec_min, spec_max = EXCLUDED.spec_max, test_uom = EXCLUDED.test_uom;
