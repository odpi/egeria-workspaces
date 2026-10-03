-- Subscription: aus_sap_s4hana__general_ledger_balances - SAP S/4HANA (Austin) receives General Ledger Balances
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Manual Journal Approvals depends on it (material entries for review)
-- Keeps nothing: SAP is the Austin source of General Ledger Balances, so the US01 transactions and balances are its
-- own universal journal coming back (writing them would loop into its extracts). Coco ledgers and EKG's SAP (RO01)
-- are other estates' and are discarded.

UPDATE incoming_ledger_transaction i SET discard_reason = 'already held: supplied by SAP S/4HANA'
 WHERE i.legal_entity_code = 'US01';
UPDATE incoming_ledger_transaction SET discard_reason = 'other estate: not company code US01' WHERE discard_reason IS NULL;

UPDATE incoming_ledger_account_balance i SET discard_reason = 'already held: supplied by SAP S/4HANA'
 WHERE i.legal_entity_code = 'US01';
UPDATE incoming_ledger_account_balance SET discard_reason = 'other estate: not company code US01' WHERE discard_reason IS NULL;
