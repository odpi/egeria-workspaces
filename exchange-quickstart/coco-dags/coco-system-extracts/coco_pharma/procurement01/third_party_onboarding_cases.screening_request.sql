-- Extract: Coco Pharmaceuticals Procurement (Coco core) -> Third Party Onboarding Cases / screening_request
-- Source: coco_pharma.procurement01 (System::procurement01)
-- Target: coco_data_hub.third_party_onboarding_cases.screening_request
-- vendor_screening raised from an onboarding case; type codes expanded.
SELECT
  s.screen_ref::varchar(40)      AS screening_identifier,
  s.case_no::varchar(40)         AS onboarding_case_identifier,
  s.requested_ts                 AS screening_requested_timestamp,
  (CASE s.screen_type WHEN 'SANC' THEN 'sanctions' WHEN 'PEP' THEN 'politically exposed persons'
                      WHEN 'ADVM' THEN 'adverse media' ELSE 'all' END)::varchar(40) AS screening_type,
  (CASE s.risk_rating WHEN 'LOW' THEN 'low' WHEN 'MED' THEN 'medium' WHEN 'HIGH' THEN 'high' END)::varchar(20) AS supplier_rating
FROM procurement01.vendor_screening s
WHERE s.case_no IS NOT NULL
