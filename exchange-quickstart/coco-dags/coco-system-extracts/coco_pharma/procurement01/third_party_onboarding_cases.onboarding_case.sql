-- Extract: Coco Pharmaceuticals Procurement (Coco core) -> Third Party Onboarding Cases / onboarding_case
-- Source: coco_pharma.procurement01 (System::procurement01)
-- Target: coco_data_hub.third_party_onboarding_cases.onboarding_case
-- onboard_case; status codes expanded, country names to ISO codes.
SELECT
  c.case_no::varchar(40)         AS onboarding_case_identifier,
  c.prop_name::varchar(200)      AS third_party_name,
  (CASE c.prop_country WHEN 'UK' THEN 'GB' WHEN 'USA' THEN 'US' WHEN 'Netherland' THEN 'NL' WHEN 'Germany' THEN 'DE' WHEN 'India' THEN 'IN'
               WHEN 'Brazil' THEN 'BR' WHEN 'Sweden' THEN 'SE' WHEN 'Malta' THEN 'MT' ELSE c.prop_country END)::varchar(60) AS third_party_country,
  c.ubo_decl                     AS third_party_owner_description,
  c.requested_by::varchar(40)    AS onboarding_case_requester_identifier,
  c.opened_on                    AS onboarding_case_start_date,
  (CASE c.case_status WHEN 'SCR' THEN 'screening' WHEN 'RISK' THEN 'risk assessment' WHEN 'APPR' THEN 'approved'
                      WHEN 'REJ' THEN 'rejected' END)::varchar(20) AS onboarding_case_current_status,
  c.vendor_no::varchar(40)       AS supplier_identifier
FROM procurement01.onboard_case c
