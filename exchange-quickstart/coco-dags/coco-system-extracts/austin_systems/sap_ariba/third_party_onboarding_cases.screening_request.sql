-- Extract: SAP Ariba SRM (Austin) -> Third Party Onboarding Cases / screening_request
-- Source: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Target: coco_data_hub.third_party_onboarding_cases.screening_request
-- srm_risk_screening; screening types to sanctions / politically exposed persons / adverse media / all.
SELECT
  s.screening_id::varchar(40) AS screening_identifier,
  s.request_id::varchar(40) AS onboarding_case_identifier,
  s.requested_at AS screening_requested_timestamp,
  lower(s.screening_type)::varchar(40) AS screening_type,
  lower(s.risk_rating)::varchar(20) AS supplier_rating
FROM sap_ariba.srm_risk_screening s
