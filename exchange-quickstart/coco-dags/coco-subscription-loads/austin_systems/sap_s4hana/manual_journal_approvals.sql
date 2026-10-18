-- Subscription: aus_sap_s4hana__manual_journal_approvals - SAP S/4HANA (Austin) receives Manual Journal Approvals
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: General Ledger Balances depends on it (approved adjustments)
-- Keeps nothing: SAP is the Austin source of Manual Journal Approvals, so the US01 parked journals and their
-- workflow approvals are its own (parked document number in VBKPF). Coco and EKG journals are other estates' and are
-- discarded.

UPDATE incoming_journal_entry i SET discard_reason = 'already held: supplied by SAP S/4HANA'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.vbkpf v WHERE v.mandt = '100' AND v.bukrs = 'US01' AND v.belnr = i.journal_entry_identifier);
UPDATE incoming_journal_entry SET discard_reason = 'other estate: not company code US01' WHERE discard_reason IS NULL;

UPDATE incoming_journal_approval i SET discard_reason = 'already held: supplied by SAP S/4HANA'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.vbkpf v WHERE v.mandt = '100' AND v.bukrs = 'US01' AND v.belnr = i.journal_entry_identifier);
UPDATE incoming_journal_approval SET discard_reason = 'other estate: not company code US01' WHERE discard_reason IS NULL;
