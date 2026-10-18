-- Subscription: coco_procurement01__third_party_onboarding_cases - Coco Pharmaceuticals Procurement (Coco core) receives Third Party Onboarding Cases
-- Destination: coco_pharma.procurement01 (System::procurement01)
-- Why it subscribes: Supplier Master Data depends on it (create supplier record)
-- Keeps nothing: Coco's onboarding cases and their screening requests are procurement01's own (onboard_case,
-- vendor_screening), so they come back as rows it already holds; the other cases (SR- numbers, requested by
-- Austin buyers) are Austin's onboarding of its own suppliers, which never become procurement01 vendors.

UPDATE incoming_onboarding_case c SET discard_reason = 'Coco onboarding case - supplied by procurement01'
 WHERE EXISTS (SELECT 1 FROM procurement01.onboard_case o WHERE o.case_no = c.onboarding_case_identifier);
UPDATE incoming_onboarding_case SET discard_reason = 'Austin onboarding case - Austin onboards its own suppliers'
 WHERE discard_reason IS NULL;

UPDATE incoming_screening_request r SET discard_reason = 'Coco screening request - supplied by procurement01'
 WHERE EXISTS (SELECT 1 FROM procurement01.vendor_screening s WHERE s.screen_ref = r.screening_identifier);
UPDATE incoming_screening_request SET discard_reason = 'Austin screening request - Austin onboards its own suppliers'
 WHERE discard_reason IS NULL;
