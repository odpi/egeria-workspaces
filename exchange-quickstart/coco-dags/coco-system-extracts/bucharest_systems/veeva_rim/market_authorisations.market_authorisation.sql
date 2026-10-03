-- Extract: Veeva Vault RIM (Bucharest) -> Market Authorisations / market_authorisation
-- Source: bucharest_systems.veeva_rim (SoftwareServer::SYS-021::Veeva Vault RIM)
-- Target: coco_data_hub.market_authorisations.market_authorisation
-- registration__v joined to product and country; Vault status names translated.
SELECT
  r.name__v::varchar(40) AS authorisation_identifier,
  p.product_code__c::varchar(20) AS product_code,
  c.abbreviation__c::varchar(8) AS market_code,
  r.health_authority__c::varchar(20) AS authorisation_regulator_code,
  r.approval_date__v AS authorisation_start_date,
  r.expiration_date__v AS authorisation_end_date,
  (CASE r.registration_status__v WHEN 'approved__v' THEN 'authorised' WHEN 'renewal_pending__c' THEN 'renewal pending'
        WHEN 'withdrawn__v' THEN 'withdrawn' WHEN 'suspended__v' THEN 'suspended' ELSE replace(r.registration_status__v, '__v', '') END)::varchar(20) AS authorisation_current_status,
  r.related_signal__c::varchar(40) AS signal_identifier
FROM veeva_rim.registration__v r
JOIN veeva_rim.product__v p ON p.id = r.product__v
JOIN veeva_rim.country__v c ON c.id = r.country__v
