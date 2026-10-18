-- Subscription: buc_sap_concur__expense_approvals - SAP Concur (Bucharest) receives Expense Approvals
-- Destination: bucharest_systems.sap_concur (SoftwareServer::SYS-012::SAP Concur)
-- Why it subscribes: Employee Expense Claims depends on it (approval decision)
-- Concur runs EKG's expense approval workflow, so every EKG claim and approval decision is already held here and is
-- discarded (no feedback loop); Coco and Austin approvals are discarded too (EKG is not yet integrated).  Nothing is
-- written.
UPDATE incoming_expense_claim i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_concur.report r WHERE r.report_id = i.claim_identifier);
UPDATE incoming_approval_decision i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_concur.report r WHERE r.report_id = i.claim_identifier);
UPDATE incoming_expense_claim SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_approval_decision SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
