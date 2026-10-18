-- Extract: Veeva Vault QMS (Bucharest) -> Deviations And CAPAs / deviation
-- Source: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Target: coco_data_hub.deviations_and_capas.deviation
-- quality_event__qdm of type deviation joined to product__v; Vault picklist API names translated.
SELECT
  q.name__v::varchar(40) AS deviation_identifier,
  q.created_date__v AS deviation_raised_timestamp,
  (CASE q.source__c WHEN 'manufacturing_execution__c' THEN 'manufacturing execution' WHEN 'laboratory__c' THEN 'laboratory'
        WHEN 'cold_chain__c' THEN 'cold chain' WHEN 'safety_signal__c' THEN 'safety signal' ELSE 'other' END)::varchar(100) AS deviation_source_type,
  q.batch_number__c::varchar(40) AS batch_identifier,
  p.product_code__c::varchar(20) AS product_code,
  q.signal_reference__c::varchar(40) AS signal_identifier,
  q.description__c AS deviation_description,
  replace(q.severity__c, '__c', '')::varchar(20) AS deviation_severity,
  (CASE q.state__v WHEN 'open_state__c' THEN 'open' WHEN 'investigation_state__c' THEN 'under investigation'
        WHEN 'disposition_state__c' THEN 'dispositioned' ELSE 'closed' END)::varchar(20) AS deviation_current_status
FROM veeva_qms.quality_event__qdm q
LEFT JOIN veeva_qms.product__v p ON p.id = q.product__c
WHERE q.object_type__v = 'deviation__c'
