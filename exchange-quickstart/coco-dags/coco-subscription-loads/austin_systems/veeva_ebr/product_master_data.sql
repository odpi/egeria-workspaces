-- Subscription: aus_veeva_ebr__product_master_data - Veeva Vault EBR (Austin) receives Product Master Data
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Batch Certification Decisions depends on it (product and market requirements)
-- Keeps the products made at Austin (AU- products and the Coco products 3000, 2050, 9000 under the manufacturing
-- integration): name updates and any new product on product__v (product_code__c is never changed), storage and shelf
-- life in NEW product__v fields, and the markets each may be released to in NEW product_market__c. Pack
-- configurations and the Coco products made elsewhere are discarded.

UPDATE incoming_product_definition i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
INSERT INTO veeva_ebr.product__v (id, name__v, product_code__c, status__v)
SELECT ('00P' || upper(substr(md5(i.product_code), 1, 11))), i.product_name, i.product_code,
       CASE WHEN i.product_current_status IN ('withdrawn', 'discontinued') THEN 'inactive__v' ELSE 'active__v' END
  FROM incoming_product_definition i
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM veeva_ebr.product__v p WHERE p.product_code__c = i.product_code)
ON CONFLICT (id) DO NOTHING;
UPDATE veeva_ebr.product__v p SET name__v = i.product_name
  FROM incoming_product_definition i
 WHERE i.discard_reason IS NULL AND p.product_code__c = i.product_code AND p.name__v IS DISTINCT FROM i.product_name;

UPDATE incoming_pack_configuration SET discard_reason = 'pack configurations not held in this vault';
UPDATE incoming_handling_requirement i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
UPDATE veeva_ebr.product__v p
   SET storage_min_temp__c = i.product_storage_minimum_temperature,
       storage_max_temp__c = i.product_storage_maximum_temperature,
       hazard_code__c = i.product_hazard_code, shelf_life_days__c = i.product_expiry_duration
  FROM incoming_handling_requirement i
 WHERE i.discard_reason IS NULL AND p.product_code__c = i.product_code
   AND (p.storage_min_temp__c, p.storage_max_temp__c, p.hazard_code__c, p.shelf_life_days__c) IS DISTINCT FROM
       (i.product_storage_minimum_temperature, i.product_storage_maximum_temperature, i.product_hazard_code,
        i.product_expiry_duration);

UPDATE incoming_authorised_market_assignment i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
INSERT INTO veeva_ebr.product_market__c
       (id, product__c, market__c, authorisation_number__c, authorised_from__c, authorised_to__c)
SELECT ('0PK' || upper(substr(md5(i.product_code || '|' || i.market_code), 1, 11))), p.id, i.market_code, i.authorisation_identifier,
       i.authorisation_start_date, i.authorisation_end_date
  FROM incoming_authorised_market_assignment i JOIN veeva_ebr.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       product__c = EXCLUDED.product__c, market__c = EXCLUDED.market__c,
       authorisation_number__c = EXCLUDED.authorisation_number__c, authorised_from__c = EXCLUDED.authorised_from__c,
       authorised_to__c = EXCLUDED.authorised_to__c;
