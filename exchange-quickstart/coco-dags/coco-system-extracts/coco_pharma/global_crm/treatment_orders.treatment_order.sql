-- Extract: Global customer ordering system (Coco core) -> Treatment Orders / treatment_order
-- Source: coco_pharma.global_crm (System::globalCRM)
-- Target: coco_data_hub.treatment_orders.treatment_order
-- sales_order (Personalized Therapy only) with its item and account; order status normalised.
SELECT
  o.ordernumber::varchar(40)            AS order_identifier,
  o.effectivedate                       AS order_date,
  o.patient_mrn__c::varchar(40)         AS patient_identifier,
  o.prescriber__c::varchar(40)          AS clinician_identifier,
  a.accountnumber::varchar(40)          AS hospital_identifier,
  i.productcode::varchar(20)            AS product_code,
  i.quantity::integer                   AS order_quantity,
  lower(o.status)::varchar(20)          AS order_current_status
FROM global_crm.sales_order o
JOIN global_crm.account a ON a.id = o.accountid
JOIN global_crm.sales_order_item i ON i.ordernumber = o.ordernumber AND i.linenumber = 1
WHERE o.order_type__c = 'Personalized Therapy'
