-- Extract: Trackwise Digital (Bucharest) -> Deviations And CAPAs / deviation
-- Source: bucharest_systems.trackwise (SoftwareServer::SYS-005::Trackwise Digital)
-- Target: coco_data_hub.deviations_and_capas.deviation
-- Trackwise-originated quality events only (copies from Veeva QMS are excluded, Veeva is their source); category
-- mapped to source type; severity and status lower-cased.
SELECT
  e.name::varchar(40) AS deviation_identifier,
  e.createddate AS deviation_raised_timestamp,
  (CASE e.cmpl123qms__category__c WHEN 'Regulatory Inspection' THEN 'inspection' WHEN 'Internal Audit' THEN 'audit'
        WHEN 'Supplier' THEN 'supplier' ELSE 'other' END)::varchar(100) AS deviation_source_type,
  e.cmpl123qms__batch_number__c::varchar(40) AS batch_identifier,
  e.cmpl123qms__product_code__c::varchar(20) AS product_code,
  NULL::varchar(40) AS signal_identifier,
  e.cmpl123qms__description__c AS deviation_description,
  lower(e.cmpl123qms__severity__c)::varchar(20) AS deviation_severity,
  (CASE e.cmpl123qms__status__c WHEN 'Open' THEN 'open' WHEN 'Closed' THEN 'closed' ELSE 'under investigation' END)::varchar(20) AS deviation_current_status
FROM trackwise.cmpl123qms__quality_event__c e
WHERE NOT e.isdeleted AND e.cmpl123qms__origin_system__c = 'Trackwise'
