-- Subscription: buc_opcenter_mes__product_master_data - Siemens Opcenter MES (Bucharest) receives Product Master Data
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Batch Certification Decisions depends on it (product and market requirements)
-- For EKG products known to this MES (product.productname = product code) keeps the description and current version
-- (productrevision) and the authorised markets (new table productmarket, checked at release).  Packs and handling
-- requirements are not used by the MES (storage conditions are entered on the release).  Today the product holds only
-- Coco and Austin products, which are discarded (Coco group data - EKG is not yet integrated).
UPDATE incoming_product_definition i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.product p WHERE p.productname = i.product_code);
UPDATE incoming_pack_configuration i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.product p WHERE p.productname = i.product_code);
UPDATE incoming_pack_configuration SET discard_reason = 'pack presentations are not used by the MES' WHERE discard_reason IS NULL;
UPDATE incoming_handling_requirement i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.product p WHERE p.productname = i.product_code);
UPDATE incoming_handling_requirement SET discard_reason = 'storage conditions are entered on the release' WHERE discard_reason IS NULL;
UPDATE incoming_authorised_market_assignment i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.product p WHERE p.productname = i.product_code);

UPDATE opcenter_mes.product p
   SET description = left(coalesce(i.product_name, p.description), 255),
       productrevision = left(coalesce(i.product_current_version, p.productrevision), 10)
  FROM incoming_product_definition i
 WHERE i.discard_reason IS NULL AND p.productname = i.product_code;

INSERT INTO opcenter_mes.productmarket (productid, marketcode, authorisationref, effectivedate, expirationdate, lastchangedate)
SELECT p.productid, i.market_code, i.authorisation_identifier, i.authorisation_start_date, i.authorisation_end_date, now()
  FROM incoming_authorised_market_assignment i JOIN opcenter_mes.product p ON p.productname = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (productid, marketcode) DO UPDATE
   SET authorisationref = EXCLUDED.authorisationref, effectivedate = EXCLUDED.effectivedate,
       expirationdate = EXCLUDED.expirationdate, lastchangedate = now()
 WHERE (opcenter_mes.productmarket.authorisationref, opcenter_mes.productmarket.effectivedate, opcenter_mes.productmarket.expirationdate)
       IS DISTINCT FROM (EXCLUDED.authorisationref, EXCLUDED.effectivedate, EXCLUDED.expirationdate);
