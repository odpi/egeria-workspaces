-- Subscription: buc_veeva_qms__product_master_data - Veeva Vault QMS (Bucharest) receives Product Master Data
-- Destination: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Why it subscribes: Batch Certification Decisions depends on it (product and market requirements)
-- For EKG products known to Vault QMS (product__v.product_code__c) keeps the product name and status (active__v /
-- inactive__v) from the product definition; packs, handling requirements and market assignments are not QMS data (the
-- market is chosen on each disposition).  Today the product holds only Coco and Austin products, which are discarded
-- (Coco group data - EKG is not yet integrated).
UPDATE incoming_product_definition i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_pack_configuration i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_pack_configuration SET discard_reason = 'pack presentations are not kept in the QMS' WHERE discard_reason IS NULL;
UPDATE incoming_handling_requirement i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_handling_requirement SET discard_reason = 'handling requirements are not kept in the QMS' WHERE discard_reason IS NULL;
UPDATE incoming_authorised_market_assignment i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_authorised_market_assignment SET discard_reason = 'market authorisations are kept in Vault RIM' WHERE discard_reason IS NULL;

UPDATE veeva_qms.product__v p
   SET name__v = left(coalesce(i.product_name, p.name__v), 120),
       status__v = (CASE WHEN i.product_current_status IS NULL THEN p.status__v
                         WHEN i.product_current_status IN ('active', 'authorised', 'marketed') THEN 'active__v' ELSE 'inactive__v' END)
  FROM incoming_product_definition i
 WHERE i.discard_reason IS NULL AND p.product_code__c = i.product_code;
