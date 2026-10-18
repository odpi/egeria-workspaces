-- Extract: Veeva Vault RIM (Bucharest) -> Regulatory Safety Submissions / safety_submission
-- Source: bucharest_systems.veeva_rim (SoftwareServer::SYS-021::Veeva Vault RIM)
-- Target: coco_data_hub.regulatory_safety_submissions.safety_submission
-- Safety-related submissions that have been sent; type and format API names translated.
SELECT
  s.name__v::varchar(40) AS submission_identifier,
  s.safety_case_reference__c::varchar(40) AS safety_case_identifier,
  p.product_code__c::varchar(20) AS product_code,
  c.abbreviation__c::varchar(8) AS market_code,
  s.health_authority__c::varchar(20) AS submission_regulator_code,
  (CASE s.submission_type__v WHEN 'psur__v' THEN 'PSUR' WHEN 'expedited__c' THEN 'expedited'
        WHEN 'safety_variation__c' THEN 'safety variation' ELSE s.submission_type__v END)::varchar(20) AS submission_type,
  s.planned_submission_date__v AS submission_due_date,
  s.actual_submission_date__v AS submission_timestamp,
  (CASE s.submission_format__c WHEN 'cesp__c' THEN 'CESP' WHEN 'e2b_r3__c' THEN 'E2B(R3)' WHEN 'ectd__v' THEN 'eCTD'
        WHEN 'paper__c' THEN 'paper' ELSE s.submission_format__c END)::varchar(20) AS submission_format_code
FROM veeva_rim.submission__v s
JOIN veeva_rim.product__v p ON p.id = s.product__v
JOIN veeva_rim.country__v c ON c.id = s.country__v
WHERE s.safety_related__c AND s.actual_submission_date__v IS NOT NULL
