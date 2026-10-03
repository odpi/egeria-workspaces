-- Subscription: coco_sus__employee_expense_claims - Coco Pharmaceuticals Sustainability Data Marts (Coco core) receives Employee Expense Claims
-- Destination: coco_pharma.coco_sus (System::coco-sus)
-- Why it subscribes: reporting: fills ghg_emissions.biz_travel, customer_travel
-- Keeps nothing: ghg_emissions.biz_travel and customer_travel hold emissions calculated from distance and travel
-- mode, and an expense claim line carries only a grouped type, date, amount and free-text description - no
-- distance, route, mode or customer.  Until a travel booking source is available, spend cannot be turned into
-- emissions here.  EKG's claims are outside Coco's emissions reporting (no Bucharest site in coco_sus.sites).

UPDATE incoming_claim_submission SET discard_reason = 'EKG claim - Bucharest is not in Coco''s emissions reporting'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_claim_submission SET discard_reason = 'claim totals are not emissions data' WHERE discard_reason IS NULL;

UPDATE incoming_claim_line l SET discard_reason = 'EKG claim - Bucharest is not in Coco''s emissions reporting'
 WHERE l.claim_identifier NOT LIKE 'RPT-%';
UPDATE incoming_claim_line SET discard_reason = 'travel spend without distance or mode - emissions cannot be calculated'
 WHERE discard_reason IS NULL AND claim_line_type = 'travel';
UPDATE incoming_claim_line SET discard_reason = 'not travel - no emissions to report' WHERE discard_reason IS NULL;

UPDATE incoming_claimant_cost_centre SET discard_reason = 'claimant cost centres are not emissions data';
