-- Subscription: aus_informatica_mdm__product_master_data - Informatica MDM (Austin) receives Product Master Data
-- Destination: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Why it subscribes: Product Change Notifications depends on it (publish change)
-- Keeps nothing today: MDM is the Austin source of Product Master Data and already masters every Austin-made product
-- (AU- and Coco 3000/2050/9000), so those rows are its own golden records coming back; Coco products made elsewhere
-- are discarded. An Austin-made product it does not yet master would land in C_L_PRODUCT (with its handling) and its
-- packs and authorisations in C_L_PRODUCT_PACK / C_L_PRODUCT_MKT_AUTH for the stage job.

UPDATE incoming_product_definition i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
UPDATE incoming_product_definition i SET discard_reason = 'already held: golden product record'
 WHERE i.discard_reason IS NULL AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_product p WHERE p.product_cd = i.product_code);
INSERT INTO informatica_mdm.c_l_product
       (rowid_system, pkey_src_object, product_cd, product_nm, product_desc, product_type_cd, active_ingredient_nm,
        strength_txt, lifecycle_status_cd, version_no)
SELECT 'DATA_HUB', i.product_code, i.product_code, i.product_name, i.product_description,
       upper(i.product_type), i.active_ingredient_name, i.product_strength, upper(i.product_current_status),
       i.product_current_version
  FROM incoming_product_definition i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       product_cd = EXCLUDED.product_cd, product_nm = EXCLUDED.product_nm, product_desc = EXCLUDED.product_desc,
       product_type_cd = EXCLUDED.product_type_cd, active_ingredient_nm = EXCLUDED.active_ingredient_nm,
       strength_txt = EXCLUDED.strength_txt, lifecycle_status_cd = EXCLUDED.lifecycle_status_cd,
       version_no = EXCLUDED.version_no;

UPDATE incoming_pack_configuration i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
UPDATE incoming_pack_configuration i SET discard_reason = 'already held: golden product record'
 WHERE i.discard_reason IS NULL AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_product p WHERE p.product_cd = i.product_code);
INSERT INTO informatica_mdm.c_l_product_pack
       (rowid_system, pkey_src_object, product_cd, pack_desc, units_per_pack, destination_mkt_cd, serialised_ind)
SELECT 'DATA_HUB', i.pack_code, i.product_code, i.pack_description, i.pack_quantity, i.pack_destination_code,
       CASE WHEN i.pack_serialised_flag THEN 'Y' ELSE 'N' END
  FROM incoming_pack_configuration i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       product_cd = EXCLUDED.product_cd, pack_desc = EXCLUDED.pack_desc, units_per_pack = EXCLUDED.units_per_pack,
       destination_mkt_cd = EXCLUDED.destination_mkt_cd, serialised_ind = EXCLUDED.serialised_ind;

UPDATE incoming_handling_requirement i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
UPDATE incoming_handling_requirement i SET discard_reason = 'already held: golden product record'
 WHERE i.discard_reason IS NULL AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_product p WHERE p.product_cd = i.product_code);
UPDATE incoming_handling_requirement i SET discard_reason = 'product not landed'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM informatica_mdm.c_l_product l
                    WHERE l.rowid_system = 'DATA_HUB' AND l.pkey_src_object = i.product_code);
UPDATE informatica_mdm.c_l_product l
   SET min_storage_temp_c = i.product_storage_minimum_temperature,
       max_storage_temp_c = i.product_storage_maximum_temperature, transport_hazard_cd = i.product_hazard_code,
       packaging_desc = i.product_packaging_description, shelf_life_days = i.product_expiry_duration
  FROM incoming_handling_requirement i
 WHERE i.discard_reason IS NULL AND l.rowid_system = 'DATA_HUB' AND l.pkey_src_object = i.product_code
   AND (l.min_storage_temp_c, l.max_storage_temp_c, l.transport_hazard_cd, l.packaging_desc, l.shelf_life_days)
       IS DISTINCT FROM (i.product_storage_minimum_temperature, i.product_storage_maximum_temperature,
                         i.product_hazard_code, i.product_packaging_description, i.product_expiry_duration);

UPDATE incoming_authorised_market_assignment i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
UPDATE incoming_authorised_market_assignment i SET discard_reason = 'already held: golden product record'
 WHERE i.discard_reason IS NULL AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_product p WHERE p.product_cd = i.product_code);
INSERT INTO informatica_mdm.c_l_product_mkt_auth
       (rowid_system, pkey_src_object, product_cd, market_cd, authorisation_no, start_dt, end_dt)
SELECT 'DATA_HUB', i.product_code || '|' || i.market_code, i.product_code, i.market_code,
       i.authorisation_identifier, i.authorisation_start_date, i.authorisation_end_date
  FROM incoming_authorised_market_assignment i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       product_cd = EXCLUDED.product_cd, market_cd = EXCLUDED.market_cd,
       authorisation_no = EXCLUDED.authorisation_no, start_dt = EXCLUDED.start_dt, end_dt = EXCLUDED.end_dt;
