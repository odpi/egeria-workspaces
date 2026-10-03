-- Subscription: coco_ledgers__subledger_postings - Coco Ledgers (Coco core) receives Subledger Postings
-- Destination: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Why it subscribes: General Ledger Balances depends on it (post transactions)
-- Keeps feeds from Coco systems (System:: identifiers) and their lines for the Coco legal entities in the journal
-- import interface gl_feed_batch and gl_interface (both NEW); the import creates the FEED journals, so nothing
-- is posted to gl_journal directly.  Discards the Austin (US01) and EKG (RO01) subledger feeds, which post to
-- the acquired estates' own ledgers - the only feeds in the product today.

UPDATE incoming_posting_batch SET discard_reason = 'Austin or EKG subledger feed - posts to the acquired estate''s own ledger'
 WHERE system_identifier NOT LIKE 'System::%';

INSERT INTO coco_ledgers.gl_feed_batch (feed_batch_id, source_sys, period_name, posted_at, line_count, control_total, feed_status)
SELECT b.feed_identifier, b.system_identifier, to_char(to_date(b.accounting_period_code, 'YYYY-MM'), 'Mon-YY'),
       b.feed_posted_timestamp, b.feed_line_count, b.feed_total_amount, upper(b.feed_current_status)
  FROM incoming_posting_batch b
 WHERE b.discard_reason IS NULL
ON CONFLICT (feed_batch_id) DO UPDATE SET source_sys = EXCLUDED.source_sys, period_name = EXCLUDED.period_name,
       posted_at = EXCLUDED.posted_at, line_count = EXCLUDED.line_count, control_total = EXCLUDED.control_total,
       feed_status = EXCLUDED.feed_status;

UPDATE incoming_posting_line SET discard_reason = 'Austin or EKG legal entity (' || legal_entity_code || ') - not kept in Coco Ledgers'
 WHERE legal_entity_code NOT IN (SELECT entity_id FROM coco_ledgers.gl_entity);
UPDATE incoming_posting_line l SET discard_reason = 'line of a feed Coco Ledgers does not import'
 WHERE l.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ledgers.gl_feed_batch b WHERE b.feed_batch_id = l.feed_identifier);

INSERT INTO coco_ledgers.gl_interface (feed_batch_id, line_no, entity_id, acct_no, txn_ref, amount, ccy)
SELECT l.feed_identifier, l.posting_line_number, l.legal_entity_code, l.ledger_account_code, l.transaction_identifier,
       l.posting_amount, l.posting_currency_code
  FROM incoming_posting_line l
 WHERE l.discard_reason IS NULL
ON CONFLICT (feed_batch_id, line_no) DO UPDATE SET entity_id = EXCLUDED.entity_id, acct_no = EXCLUDED.acct_no,
       txn_ref = EXCLUDED.txn_ref, amount = EXCLUDED.amount, ccy = EXCLUDED.ccy;
