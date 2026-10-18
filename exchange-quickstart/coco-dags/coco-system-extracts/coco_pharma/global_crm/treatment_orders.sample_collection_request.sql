-- Extract: Global customer ordering system (Coco core) -> Treatment Orders / sample_collection_request
-- Source: coco_pharma.global_crm (System::globalCRM)
-- Target: coco_data_hub.treatment_orders.sample_collection_request
-- collection_request__c, one per personalised order.
SELECT
  c.order__c::varchar(40)               AS order_identifier,
  left(c.collection_site__c, 40)::varchar(40) AS sample_collection_location,
  c.window_start__c                     AS sample_collection_start_date,
  c.window_end__c                       AS sample_collection_end_date,
  c.material_required__c::varchar(60)   AS sample_material_type
FROM global_crm.collection_request__c c
