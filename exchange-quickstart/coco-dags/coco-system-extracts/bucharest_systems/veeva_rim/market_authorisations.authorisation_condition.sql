-- Extract: Veeva Vault RIM (Bucharest) -> Market Authorisations / authorisation_condition
-- Source: bucharest_systems.veeva_rim (SoftwareServer::SYS-021::Veeva Vault RIM)
-- Target: coco_data_hub.market_authorisations.authorisation_condition
-- commitment__v joined to its registration; commitment type API names to words.
SELECT
  r.name__v::varchar(40) AS authorisation_identifier,
  m.commitment_number__c AS authorisation_requirement_number,
  replace(replace(m.commitment_type__c, '__c', ''), '_', ' ')::varchar(40) AS authorisation_requirement_type,
  m.description__v AS authorisation_requirement_description,
  m.start_date__c AS authorisation_requirement_start_date
FROM veeva_rim.commitment__v m
JOIN veeva_rim.registration__v r ON r.id = m.registration__v
