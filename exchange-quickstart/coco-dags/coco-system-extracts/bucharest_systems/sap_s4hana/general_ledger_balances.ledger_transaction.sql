-- Extract: SAP ERP S/4HANA (Bucharest) -> General Ledger Balances / ledger_transaction
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.general_ledger_balances.ledger_transaction
-- Every acdoca line of the leading ledger; feed identifier for IDoc-created documents, journal entry identifier for
-- documents posted from a parked journal (tcode FBV0 keeps the parked document number).
SELECT
  (a.rbukrs || '-' || a.gjahr || '-' || a.belnr || '-' || a.docln)::varchar(40) AS transaction_identifier,
  a.rbukrs::varchar(10) AS legal_entity_code,
  (a.gjahr || '-' || substr(a.poper, 2, 2))::varchar(10) AS accounting_period_code,
  ltrim(a.racct, '0')::varchar(20) AS ledger_account_code,
  a.hsl::numeric(18,2) AS transaction_amount,
  a.rhcur::varchar(3) AS transaction_currency_code,
  ((to_date(b.cpudt, 'YYYYMMDD') + b.cputm::time) AT TIME ZONE 'UTC') AS transaction_posted_timestamp,
  (CASE WHEN b.awtyp = 'IDOC' THEN b.awkey END)::varchar(40) AS feed_identifier,
  (CASE WHEN b.tcode = 'FBV0' THEN b.belnr END)::varchar(40) AS journal_entry_identifier
FROM sap_s4hana.acdoca a
JOIN sap_s4hana.bkpf b ON b.mandt = a.rclnt AND b.bukrs = a.rbukrs AND b.gjahr = a.gjahr AND b.belnr = a.belnr
WHERE a.rclnt = '300' AND a.rldnr = '0L'
