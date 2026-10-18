-- Extract: SAP S/4HANA (Austin) -> Subledger Postings / posting_line
-- Source: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Target: coco_data_hub.subledger_postings.posting_line
-- acdoca lines of documents created by inbound IDocs, numbered within each IDoc.
SELECT
  b.awkey::varchar(40) AS feed_identifier,
  (row_number() OVER (PARTITION BY b.awkey ORDER BY a.belnr, a.docln))::integer AS posting_line_number,
  ltrim(a.racct, '0')::varchar(20) AS ledger_account_code,
  a.rbukrs::varchar(10) AS legal_entity_code,
  (a.rbukrs || '-' || a.gjahr || '-' || a.belnr || '-' || a.docln)::varchar(40) AS transaction_identifier,
  a.hsl::numeric(18,2) AS posting_amount,
  a.rhcur::varchar(3) AS posting_currency_code
FROM sap_s4hana.bkpf b
JOIN sap_s4hana.acdoca a ON a.rclnt = b.mandt AND a.rbukrs = b.bukrs AND a.gjahr = b.gjahr AND a.belnr = b.belnr AND a.rldnr = '0L'
WHERE b.mandt = '100' AND b.awtyp = 'IDOC'
