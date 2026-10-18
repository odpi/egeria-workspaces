-- Extract: SAP Ariba SRM (Austin) -> Supplier Payment Detail Changes / payment_detail_change
-- Source: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Target: coco_data_hub.supplier_payment_detail_changes.payment_detail_change
-- sm_bank_change_request joined to sm_supplier for the SAP vendor number; approval status translated.
SELECT
  c.change_request_id::varchar(40) AS payment_detail_change_identifier,
  v.erp_vendor_id::varchar(40) AS supplier_identifier,
  c.submitted_at AS payment_detail_change_requested_timestamp,
  c.submitted_by::varchar(40) AS payment_detail_change_requester_identifier,
  c.old_bank_ref::varchar(40) AS bank_account_previous_identifier,
  c.new_bank_ref::varchar(40) AS bank_account_current_identifier,
  (CASE c.approval_status WHEN 'Verified' THEN 'verified' WHEN 'Rejected' THEN 'rejected' ELSE 'pending verification' END)::varchar(20) AS payment_detail_change_status
FROM sap_ariba.sm_bank_change_request c
JOIN sap_ariba.sm_supplier v ON v.sm_vendor_id = c.sm_vendor_id
