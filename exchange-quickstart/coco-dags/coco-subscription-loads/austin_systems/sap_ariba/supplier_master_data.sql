-- Subscription: aus_sap_ariba__supplier_master_data - SAP Ariba SRM (Austin) receives Supplier Master Data
-- Destination: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Why it subscribes: Supplier Payments depends on it (supplier and payment details)
-- Keeps the Austin suppliers as ERP vendor replicas in the NEW erp_vendor table (as the cloud integration gateway
-- lands the ERP vendor master), with the screening status and the verified remittance account from the same product,
-- which invoice reconciliation checks before an invoice is approved for payment. sm_supplier, which the extracts
-- read, is not touched. Coco and EKG suppliers are discarded.

UPDATE incoming_supplier i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO sap_ariba.erp_vendor
       (erp_vendor_id, vendor_name, country_code, vendor_type, approved, approved_date, vendor_status)
SELECT i.supplier_identifier, i.supplier_name, left(i.supplier_country, 2), i.supplier_type,
       i.supplier_approved_flag, i.supplier_approved_date, i.supplier_current_status
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (erp_vendor_id) DO UPDATE SET
       vendor_name = EXCLUDED.vendor_name, country_code = EXCLUDED.country_code, vendor_type = EXCLUDED.vendor_type,
       approved = EXCLUDED.approved, approved_date = EXCLUDED.approved_date, vendor_status = EXCLUDED.vendor_status;

UPDATE incoming_supplier_risk_status i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE NOT EXISTS (SELECT 1 FROM sap_ariba.erp_vendor v WHERE v.erp_vendor_id = i.supplier_identifier);
UPDATE sap_ariba.erp_vendor v
   SET screening_status = i.supplier_screened_status, screening_date = i.supplier_screened_date,
       risk_rating = i.supplier_rating, screening_ref = i.screening_identifier, anomaly_ref = i.anomaly_identifier
  FROM incoming_supplier_risk_status i
 WHERE i.discard_reason IS NULL AND v.erp_vendor_id = i.supplier_identifier
   AND (v.screening_status, v.screening_date, v.risk_rating, v.screening_ref, v.anomaly_ref) IS DISTINCT FROM
       (i.supplier_screened_status, i.supplier_screened_date, i.supplier_rating, i.screening_identifier,
        i.anomaly_identifier);

UPDATE incoming_supplier_payment_details i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE NOT EXISTS (SELECT 1 FROM sap_ariba.erp_vendor v WHERE v.erp_vendor_id = i.supplier_identifier);
UPDATE sap_ariba.erp_vendor v
   SET remit_bank_ref = i.bank_account_current_identifier, remit_bank_name = i.bank_account_provider_name,
       remit_bank_country = i.bank_account_country, bank_change_ref = i.payment_detail_change_identifier,
       bank_verified_date = i.payment_detail_verified_date
  FROM incoming_supplier_payment_details i
 WHERE i.discard_reason IS NULL AND v.erp_vendor_id = i.supplier_identifier
   AND (v.remit_bank_ref, v.remit_bank_name, v.remit_bank_country, v.bank_change_ref, v.bank_verified_date)
       IS DISTINCT FROM (i.bank_account_current_identifier, i.bank_account_provider_name, i.bank_account_country,
                         i.payment_detail_change_identifier, i.payment_detail_verified_date);
