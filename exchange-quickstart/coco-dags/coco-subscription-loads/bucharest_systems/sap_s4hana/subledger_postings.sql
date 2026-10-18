-- Subscription: buc_sap_s4hana__subledger_postings - SAP ERP S/4HANA (Bucharest) receives Subledger Postings
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: General Ledger Balances depends on it (post transactions)
-- The subledger postings are SAP's own inbound IDoc feeds (edidc) and the documents they created, so every EKG feed and
-- posting line is already held here and is discarded (no feedback loop); feeds of other ledgers are discarded as Coco
-- group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_posting_batch i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.edidc e WHERE e.mandt = '300' AND e.docnum = i.feed_identifier);
UPDATE incoming_posting_line i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE i.legal_entity_code = 'RO01'
    OR EXISTS (SELECT 1 FROM sap_s4hana.edidc e WHERE e.mandt = '300' AND e.docnum = i.feed_identifier);
UPDATE incoming_posting_batch SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_posting_line SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
