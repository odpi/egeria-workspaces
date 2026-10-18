-- Extract: Coco Ledgers (Coco core) -> General Ledger Balances / ledger_transaction
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.general_ledger_balances.ledger_transaction
-- posted gl_journal_line rows; one transaction per line, signed amount (debit positive), period text to YYYY-MM.
SELECT
  (l.je_id || '-' || l.line_no)::varchar(40) AS transaction_identifier,
  j.entity_id::varchar(10)       AS legal_entity_code,
  to_char(to_date(j.period_name, 'Mon-YY'), 'YYYY-MM')::varchar(10) AS accounting_period_code,
  l.acct_no::varchar(20)         AS ledger_account_code,
  (l.dr_amt - l.cr_amt)::numeric(18,2) AS transaction_amount,
  l.ccy::varchar(3)              AS transaction_currency_code,
  j.posted_at                    AS transaction_posted_timestamp,
  j.feed_batch_id::varchar(40)   AS feed_identifier,
  (CASE WHEN j.je_source = 'MAN' THEN j.je_id END)::varchar(40) AS journal_entry_identifier
FROM coco_ledgers.gl_journal_line l
JOIN coco_ledgers.gl_journal j ON j.je_id = l.je_id
WHERE j.je_status = 'POSTED'
