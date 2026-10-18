-- Extract: SAP Ariba SRM (Austin) -> Third Party Onboarding Cases / onboarding_case
-- Source: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Target: coco_data_hub.third_party_onboarding_cases.onboarding_case
-- sm_supplier_request left-joined to sm_supplier for the created supplier's SAP number; workflow status to screening /
-- risk assessment / approved / rejected.
SELECT
  r.request_id::varchar(40) AS onboarding_case_identifier,
  r.supplier_name::varchar(200) AS third_party_name,
  r.country_code::varchar(60) AS third_party_country,
  r.business_owner_description AS third_party_owner_description,
  r.requester_user::varchar(40) AS onboarding_case_requester_identifier,
  r.created_date AS onboarding_case_start_date,
  lower(r.request_status)::varchar(20) AS onboarding_case_current_status,
  v.erp_vendor_id::varchar(40) AS supplier_identifier
FROM sap_ariba.sm_supplier_request r
LEFT JOIN sap_ariba.sm_supplier v ON v.sm_vendor_id = r.sm_vendor_id
