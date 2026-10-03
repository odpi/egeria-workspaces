-- Subscription: buc_sap_concur__employee_expense_claims - SAP Concur (Bucharest) receives Employee Expense Claims
-- Destination: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Why it subscribes: Expense Approvals depends on it (submit for approval)
-- Concur is the source of EKG's expense claims, so every EKG claim, line and claimant cost centre is already held here
-- and is discarded (no feedback loop); Coco and Austin claims are discarded too (EKG is not yet integrated).  Nothing is
-- written.
UPDATE incoming_claim_submission i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_concur.report r WHERE r.report_id = i.claim_identifier);
UPDATE incoming_claim_line i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_concur.report r WHERE r.report_id = i.claim_identifier);
UPDATE incoming_claimant_cost_centre i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_concur.employee e
                WHERE 'WP-' || upper(substr(md5('EKG:' || e.employee_id), 1, 12)) = i.worker_pseudonym_identifier);
UPDATE incoming_claim_submission SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_claim_line SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_claimant_cost_centre SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
