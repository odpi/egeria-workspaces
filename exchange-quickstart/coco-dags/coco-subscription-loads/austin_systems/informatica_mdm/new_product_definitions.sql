-- Subscription: aus_informatica_mdm__new_product_definitions - Informatica MDM (Austin) receives New Product Definitions
-- Destination: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Why it subscribes: Product Master Data depends on it (new product definition)
-- Keeps Austin candidate products (AU- codes) that it does not yet master in the C_L_PRODUCT landing table
-- (lifecycle DEVELOPMENT) and their presentations in C_L_PRODUCT_PACK, so the golden record exists before launch.
-- Candidates of other estates and product specifications (held in LIMS, not MDM) are discarded.

UPDATE incoming_candidate_product_definition i SET discard_reason = 'other estate: not an Austin product code'
 WHERE i.product_code NOT LIKE 'AU-%';
UPDATE incoming_candidate_product_definition i SET discard_reason = 'already held: golden product record'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_product p WHERE p.product_cd = i.product_code);
INSERT INTO informatica_mdm.c_l_product
       (rowid_system, pkey_src_object, product_cd, product_nm, product_type_cd, active_ingredient_nm, strength_txt,
        lifecycle_status_cd, version_no, candidate_ref, formulation_ref, clinical_trial_ref, handover_dt)
SELECT 'DATA_HUB', i.product_code, i.product_code, i.product_name, 'STANDARD', i.active_ingredient_name,
       i.product_strength, 'DEVELOPMENT', '0.1', i.candidate_identifier, i.formulation_identifier,
       i.clinical_trial_identifier, i.candidate_handover_date
  FROM incoming_candidate_product_definition i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       product_cd = EXCLUDED.product_cd, product_nm = EXCLUDED.product_nm,
       active_ingredient_nm = EXCLUDED.active_ingredient_nm, strength_txt = EXCLUDED.strength_txt,
       candidate_ref = EXCLUDED.candidate_ref, formulation_ref = EXCLUDED.formulation_ref,
       clinical_trial_ref = EXCLUDED.clinical_trial_ref, handover_dt = EXCLUDED.handover_dt;

UPDATE incoming_product_presentation i SET discard_reason = 'product not landed (other estate or already mastered)'
 WHERE NOT EXISTS (SELECT 1 FROM informatica_mdm.c_l_product l
                    WHERE l.rowid_system = 'DATA_HUB' AND l.pkey_src_object = i.product_code
                      AND l.lifecycle_status_cd = 'DEVELOPMENT');
INSERT INTO informatica_mdm.c_l_product_pack
       (rowid_system, pkey_src_object, product_cd, pack_desc, units_per_pack, destination_mkt_cd, serialised_ind)
SELECT 'DATA_HUB', i.pack_code, i.product_code, i.pack_description, i.pack_quantity, 'US', 'Y'
  FROM incoming_product_presentation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       product_cd = EXCLUDED.product_cd, pack_desc = EXCLUDED.pack_desc, units_per_pack = EXCLUDED.units_per_pack;

UPDATE incoming_product_specification SET discard_reason = 'specifications are held in LIMS, not MDM';
