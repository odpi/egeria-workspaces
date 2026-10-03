-- Subscription: buc_sap_s4hana__general_ledger_balances - SAP ERP S/4HANA (Bucharest) receives General Ledger Balances
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Manual Journal Approvals depends on it (material entries for review)
-- SAP S/4HANA is the source of EKG's ledger (company code RO01, universal journal acdoca), so every EKG ledger
-- transaction and balance is already held here and is discarded (no feedback loop); other company codes are discarded
-- as Coco group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_ledger_transaction SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE legal_entity_code = 'RO01';
UPDATE incoming_ledger_account_balance SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE legal_entity_code = 'RO01';
UPDATE incoming_ledger_transaction SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_ledger_account_balance SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
