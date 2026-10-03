-- Subscription: coco_ledgers__general_ledger_balances - Coco Ledgers (Coco core) receives General Ledger Balances
-- Destination: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Why it subscribes: Manual Journal Approvals depends on it (material entries for review)
-- Keeps nothing: the Coco legal entities' transactions and balances are Coco Ledgers' own (gl_journal_line,
-- gl_period_balance), so they come back as rows it already holds; the US01 (Austin) and RO01 (EKG) ledgers
-- belong to the acquired estates, whose finance is not integrated with Coco Ledgers.

UPDATE incoming_ledger_transaction SET discard_reason = 'Coco ledger transaction - supplied by Coco Ledgers'
 WHERE legal_entity_code IN (SELECT entity_id FROM coco_ledgers.gl_entity);
UPDATE incoming_ledger_transaction SET discard_reason = 'Austin or EKG ledger (' || legal_entity_code || ') - finance not integrated with Coco Ledgers'
 WHERE discard_reason IS NULL;

UPDATE incoming_ledger_account_balance SET discard_reason = 'Coco ledger balance - supplied by Coco Ledgers'
 WHERE legal_entity_code IN (SELECT entity_id FROM coco_ledgers.gl_entity);
UPDATE incoming_ledger_account_balance SET discard_reason = 'Austin or EKG ledger (' || legal_entity_code || ') - finance not integrated with Coco Ledgers'
 WHERE discard_reason IS NULL;
