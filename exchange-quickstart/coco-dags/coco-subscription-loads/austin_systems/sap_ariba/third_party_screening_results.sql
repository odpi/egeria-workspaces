-- Subscription: aus_sap_ariba__third_party_screening_results - SAP Ariba SRM (Austin) receives Third Party Screening Results
-- Destination: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Why it subscribes: Third Party Onboarding Cases depends on it (screening result)
-- Keeps the results of screenings Ariba requested (screening ID in srm_risk_screening) in the NEW
-- srm_screening_result and srm_screening_match tables, which the supplier request workflow reads to move the request
-- on; srm_risk_screening, which feeds Third Party Onboarding Cases, is updated only by that workflow. Results of
-- screenings requested elsewhere (Coco, EKG) are discarded.

UPDATE incoming_screening_result i SET discard_reason = 'screening not requested by Ariba (other estate)'
 WHERE NOT EXISTS (SELECT 1 FROM sap_ariba.srm_risk_screening s WHERE s.screening_id = i.screening_identifier);
INSERT INTO sap_ariba.srm_screening_result
       (screening_id, screened_name, screening_date, result_status, match_count, risk_rating)
SELECT i.screening_identifier, i.third_party_name, i.screening_date, i.screening_status, i.screening_match_count,
       i.screening_rating
  FROM incoming_screening_result i
 WHERE i.discard_reason IS NULL
ON CONFLICT (screening_id) DO UPDATE SET
       screened_name = EXCLUDED.screened_name, screening_date = EXCLUDED.screening_date,
       result_status = EXCLUDED.result_status, match_count = EXCLUDED.match_count,
       risk_rating = EXCLUDED.risk_rating;

UPDATE incoming_screening_match i SET discard_reason = 'screening not requested by Ariba (other estate)'
 WHERE NOT EXISTS (SELECT 1 FROM sap_ariba.srm_screening_result r WHERE r.screening_id = i.screening_identifier);
INSERT INTO sap_ariba.srm_screening_match
       (screening_id, list_name, matched_name, match_rating, match_description)
SELECT i.screening_identifier, i.screening_match_list_name, i.screening_match_name, i.screening_match_rating,
       i.screening_match_description
  FROM incoming_screening_match i
 WHERE i.discard_reason IS NULL
ON CONFLICT (screening_id, list_name, matched_name) DO UPDATE SET
       match_rating = EXCLUDED.match_rating, match_description = EXCLUDED.match_description;
