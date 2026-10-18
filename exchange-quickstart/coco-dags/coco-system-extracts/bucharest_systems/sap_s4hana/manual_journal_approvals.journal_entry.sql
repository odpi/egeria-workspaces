-- Extract: SAP ERP S/4HANA (Bucharest) -> Manual Journal Approvals / journal_entry
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.manual_journal_approvals.journal_entry
-- Parked G/L documents (vbkpf, blart SA) with the debit total of their parked lines (vbsegs).
SELECT
  v.belnr::varchar(40) AS journal_entry_identifier,
  (v.gjahr || '-' || v.monat)::varchar(10) AS accounting_period_code,
  v.bukrs::varchar(10) AS legal_entity_code,
  sum(s.dmbtr) FILTER (WHERE s.shkzg = 'S')::numeric(18,2) AS journal_entry_amount,
  v.bktxt AS journal_entry_description,
  lower(v.usnam)::varchar(40) AS journal_entry_preparer_identifier,
  ((to_date(v.cpudt, 'YYYYMMDD') + v.cputm::time) AT TIME ZONE 'UTC') AS journal_entry_submitted_timestamp
FROM sap_s4hana.vbkpf v
JOIN sap_s4hana.vbsegs s ON s.mandt = v.mandt AND s.bukrs = v.bukrs AND s.belnr = v.belnr AND s.gjahr = v.gjahr
WHERE v.mandt = '300' AND v.blart = 'SA'
GROUP BY v.belnr, v.gjahr, v.monat, v.bukrs, v.bktxt, v.usnam, v.cpudt, v.cputm
