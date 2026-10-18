-- Extract: Global customer ordering system (Coco core) -> Treatment Invoices / invoice
-- Source: coco_pharma.global_crm (System::globalCRM)
-- Target: coco_data_hub.treatment_invoices.invoice
-- invoice__c for Personalized Therapy orders; status normalised.
SELECT
  v.name::varchar(40)                   AS invoice_number,
  v.invoice_date__c                     AS invoice_date,
  v.order__c::varchar(40)               AS order_identifier,
  a.accountnumber::varchar(40)          AS customer_identifier,
  v.total_amount__c::numeric(18,2)      AS invoice_total_amount,
  v.currencyisocode::varchar(3)         AS invoice_currency_code,
  v.due_date__c                         AS invoice_due_date,
  lower(v.status__c)::varchar(20)       AS invoice_current_status
FROM global_crm.invoice__c v
JOIN global_crm.sales_order o ON o.ordernumber = v.order__c
JOIN global_crm.account a ON a.id = v.account__c
WHERE o.order_type__c = 'Personalized Therapy'
