-- Extract: SAP ERP S/4HANA (Bucharest) -> General Ledger Balances / ledger_account_balance
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.general_ledger_balances.ledger_account_balance
-- Year-to-date balance per company code, account and period (periods 06-09 of 2026) computed from acdoca, with the
-- Romanian account name from skat (language 4).
WITH periods AS (SELECT '2026' AS gjahr, lpad(p::text, 3, '0') AS poper FROM generate_series(6, 9) p),
accts AS (SELECT DISTINCT rbukrs, racct, rhcur FROM sap_s4hana.acdoca WHERE rclnt = '300' AND rldnr = '0L' AND gjahr = '2026')
SELECT
  x.rbukrs::varchar(10) AS legal_entity_code,
  (p.gjahr || '-' || substr(p.poper, 2, 2))::varchar(10) AS accounting_period_code,
  ltrim(x.racct, '0')::varchar(20) AS ledger_account_code,
  coalesce(t.txt50, x.racct)::varchar(120) AS ledger_account_name,
  coalesce((SELECT sum(a.hsl) FROM sap_s4hana.acdoca a
            WHERE a.rclnt = '300' AND a.rldnr = '0L' AND a.rbukrs = x.rbukrs AND a.racct = x.racct
              AND a.gjahr = p.gjahr AND a.poper <= p.poper), 0)::numeric(18,2) AS ledger_account_balance_amount,
  x.rhcur::varchar(3) AS ledger_currency_code
FROM accts x
CROSS JOIN periods p
LEFT JOIN sap_s4hana.skat t ON t.mandt = '300' AND t.spras = '4' AND t.ktopl = 'EKRO' AND t.saknr = x.racct
