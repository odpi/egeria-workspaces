-- Extract: Coco Ledgers (Coco core) -> General Ledger Balances / ledger_account_balance
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.general_ledger_balances.ledger_account_balance
-- gl_period_balance with the account name; period text to YYYY-MM.
SELECT
  b.entity_id::varchar(10)       AS legal_entity_code,
  to_char(to_date(b.period_name, 'Mon-YY'), 'YYYY-MM')::varchar(10) AS accounting_period_code,
  b.acct_no::varchar(20)         AS ledger_account_code,
  a.acct_name::varchar(120)      AS ledger_account_name,
  b.closing_balance::numeric(18,2) AS ledger_account_balance_amount,
  b.ccy::varchar(3)              AS ledger_currency_code
FROM coco_ledgers.gl_period_balance b
JOIN coco_ledgers.gl_account a ON a.acct_no = b.acct_no
