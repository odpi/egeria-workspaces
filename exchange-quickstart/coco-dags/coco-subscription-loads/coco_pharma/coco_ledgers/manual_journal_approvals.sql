-- Subscription: coco_ledgers__manual_journal_approvals - Coco Ledgers (Coco core) receives Manual Journal Approvals
-- Destination: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Why it subscribes: General Ledger Balances depends on it (approved adjustments)
-- Keeps nothing: manual journals of the Coco legal entities are prepared and approved in Coco Ledgers itself
-- (gl_journal, gl_je_review), so they come back as rows it already holds; US01 (Austin) and RO01 (EKG) journals
-- are approved and posted in the acquired estates' own ledgers.

UPDATE incoming_journal_entry SET discard_reason = 'Coco manual journal - supplied by Coco Ledgers'
 WHERE legal_entity_code IN (SELECT entity_id FROM coco_ledgers.gl_entity);
UPDATE incoming_journal_entry SET discard_reason = 'Austin or EKG journal (' || legal_entity_code || ') - finance not integrated with Coco Ledgers'
 WHERE discard_reason IS NULL;

UPDATE incoming_journal_approval a SET discard_reason = 'Coco journal approval - supplied by Coco Ledgers'
 WHERE EXISTS (SELECT 1 FROM coco_ledgers.gl_journal j WHERE j.je_id = a.journal_entry_identifier);
UPDATE incoming_journal_approval SET discard_reason = 'Austin or EKG journal approval - finance not integrated with Coco Ledgers'
 WHERE discard_reason IS NULL;
