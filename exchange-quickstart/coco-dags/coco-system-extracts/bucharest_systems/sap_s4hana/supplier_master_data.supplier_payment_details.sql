-- Extract: SAP ERP S/4HANA (Bucharest) -> Supplier Master Data / supplier_payment_details
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.supplier_master_data.supplier_payment_details
-- Current lfbk bank account (IBAN, or country-bank key-account where there is none) with the bank name from bnka, the
-- latest vendor change document and its verification.
SELECT
  ltrim(b.lifnr, '0')::varchar(40) AS supplier_identifier,
  coalesce(nullif(b.iban, ''), b.banks || '-' || b.bankl || '-' || b.bankn)::varchar(40) AS bank_account_current_identifier,
  n.banka::varchar(120) AS bank_account_provider_name,
  b.banks::varchar(60) AS bank_account_country,
  v.changenr::varchar(40) AS payment_detail_change_identifier,
  to_date(v.verif_date, 'YYYYMMDD') AS payment_detail_verified_date
FROM sap_s4hana.lfbk b
JOIN sap_s4hana.bnka n ON n.banks = b.banks AND n.bankl = b.bankl
JOIN LATERAL (SELECT z.changenr, z.verif_date FROM sap_s4hana.zekg_bank_verif z
              WHERE z.mandt = b.mandt AND z.lifnr = b.lifnr ORDER BY z.changenr DESC LIMIT 1) v ON true
WHERE b.mandt = '300'
