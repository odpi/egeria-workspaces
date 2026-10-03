-- Extract: Salesforce Sales Cloud CRM (Austin) -> Treatment Orders / treatment_order
-- Source: austin_systems.salesforce_crm (SoftwareServer::AUS-SYS-016::SN-CRM-AU-20200901)
-- Target: coco_data_hub.treatment_orders.treatment_order
-- therapy_order__c joined to account (SAP customer number) and contact (NPI); portal status to lower case.
SELECT
  o.name::varchar(40) AS order_identifier,
  o.order_date__c AS order_date,
  o.patient_reference__c::varchar(40) AS patient_identifier,
  c.npi__c::varchar(40) AS clinician_identifier,
  a.sap_customer_number__c::varchar(40) AS hospital_identifier,
  o.product_code__c::varchar(20) AS product_code,
  o.doses__c::integer AS order_quantity,
  lower(o.status__c)::varchar(20) AS order_current_status
FROM salesforce_crm.therapy_order__c o
JOIN salesforce_crm.account a ON a.sfid = o.account__c
JOIN salesforce_crm.contact c ON c.sfid = o.clinician__c
WHERE NOT o.isdeleted
