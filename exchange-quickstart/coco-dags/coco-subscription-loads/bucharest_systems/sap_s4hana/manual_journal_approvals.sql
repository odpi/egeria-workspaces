-- Subscription: buc_sap_s4hana__manual_journal_approvals - SAP ERP S/4HANA (Bucharest) receives Manual Journal Approvals
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: General Ledger Balances depends on it (approved adjustments)
-- SAP S/4HANA is the source of EKG's manual journals (parked documents vbkpf and their approval work items), so every
-- EKG journal and approval is already held here and is discarded (no feedback loop); other company codes are discarded
-- as Coco group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_journal_entry SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE legal_entity_code = 'RO01';
UPDATE incoming_journal_approval i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.vbkpf v WHERE v.mandt = '300' AND v.belnr = i.journal_entry_identifier)
    OR EXISTS (SELECT 1 FROM incoming_journal_entry j WHERE j.journal_entry_identifier = i.journal_entry_identifier
                AND j.legal_entity_code = 'RO01');
UPDATE incoming_journal_entry SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_journal_approval SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
