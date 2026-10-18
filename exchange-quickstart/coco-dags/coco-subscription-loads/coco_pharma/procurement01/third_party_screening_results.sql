-- Subscription: coco_procurement01__third_party_screening_results - Coco Pharmaceuticals Procurement (Coco core) receives Third Party Screening Results
-- Destination: coco_pharma.procurement01 (System::procurement01)
-- Why it subscribes: Third Party Onboarding Cases depends on it (screening result)
-- Keeps the results of screenings procurement01 requested (screen_ref in vendor_screening) and their watch-list
-- matches in screen_result and screen_hit (both NEW); the buyer then records the outcome on vendor_screening,
-- which is not written directly because it feeds Supplier Master Data.  Discards results of screenings other
-- systems requested.  No system supplies this product yet, so nothing arrives today.

UPDATE incoming_screening_result r SET discard_reason = 'not a screening requested by procurement01'
 WHERE NOT EXISTS (SELECT 1 FROM procurement01.vendor_screening s WHERE s.screen_ref = r.screening_identifier);

INSERT INTO procurement01.screen_result (screen_ref, party_name, result_dt, result_status, match_cnt, rating)
SELECT r.screening_identifier, r.third_party_name, r.screening_date, r.screening_status, r.screening_match_count,
       r.screening_rating
  FROM incoming_screening_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (screen_ref) DO UPDATE SET party_name = EXCLUDED.party_name, result_dt = EXCLUDED.result_dt,
       result_status = EXCLUDED.result_status, match_cnt = EXCLUDED.match_cnt, rating = EXCLUDED.rating;

UPDATE incoming_screening_match m SET discard_reason = 'match of a screening procurement01 did not request'
 WHERE NOT EXISTS (SELECT 1 FROM procurement01.screen_result r WHERE r.screen_ref = m.screening_identifier);

INSERT INTO procurement01.screen_hit (screen_ref, list_name, hit_name, hit_rating, hit_text)
SELECT m.screening_identifier, m.screening_match_list_name, m.screening_match_name, m.screening_match_rating,
       m.screening_match_description
  FROM incoming_screening_match m
 WHERE m.discard_reason IS NULL
ON CONFLICT (screen_ref, list_name, hit_name) DO UPDATE SET hit_rating = EXCLUDED.hit_rating, hit_text = EXCLUDED.hit_text;
