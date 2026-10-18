-- Subscription: aus_informatica_idmc__product_master_data - Informatica IDMC (Austin) receives Product Master Data
-- Destination: austin_systems.informatica_idmc (SoftwareServer::AUS-SYS-042::SN-ETL-AU-20200901)
-- Why it subscribes: Product Change Notifications depends on it (publish change)
-- Keeps nothing: the mapping tasks read the golden product records straight from Informatica MDM, so the Austin
-- product rows (products MDM already masters) are already being distributed, and its activity log - which feeds
-- Product Change Notifications - only records runs. Coco products not made at Austin are discarded too.

UPDATE incoming_product_definition i SET discard_reason = CASE WHEN (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'))
       THEN 'already distributed from the MDM golden record' ELSE 'other estate: product not made at Austin' END;
UPDATE incoming_pack_configuration i SET discard_reason = CASE WHEN (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'))
       THEN 'already distributed from the MDM golden record' ELSE 'other estate: product not made at Austin' END;
UPDATE incoming_handling_requirement i SET discard_reason = CASE WHEN (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'))
       THEN 'already distributed from the MDM golden record' ELSE 'other estate: product not made at Austin' END;
UPDATE incoming_authorised_market_assignment i SET discard_reason = CASE WHEN (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'))
       THEN 'already distributed from the MDM golden record' ELSE 'other estate: product not made at Austin' END;
