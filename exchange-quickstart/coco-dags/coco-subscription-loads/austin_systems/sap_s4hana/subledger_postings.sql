-- Subscription: aus_sap_s4hana__subledger_postings - SAP S/4HANA (Austin) receives Subledger Postings
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: General Ledger Balances depends on it (post transactions)
-- Keeps nothing: SAP is the Austin source of Subledger Postings, so the US01 feeds are its own inbound IDocs (docnum
-- in EDIDC) coming back. EKG's SAP feeds (RO01) are another estate's and are discarded.

UPDATE incoming_posting_batch i SET discard_reason = 'already held: supplied by SAP S/4HANA'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.edidc e WHERE e.mandt = '100' AND e.docnum = i.feed_identifier);
UPDATE incoming_posting_batch SET discard_reason = 'other estate: not company code US01' WHERE discard_reason IS NULL;

UPDATE incoming_posting_line i SET discard_reason = 'already held: supplied by SAP S/4HANA'
 WHERE i.legal_entity_code = 'US01';
UPDATE incoming_posting_line SET discard_reason = 'other estate: not company code US01' WHERE discard_reason IS NULL;
