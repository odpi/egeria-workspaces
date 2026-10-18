-- Extract: SAP ERP S/4HANA (Bucharest) -> Subledger Postings / posting_batch
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.subledger_postings.posting_batch
-- Inbound IDocs from the operational systems (edidc) with the accounting documents they created (bkpf.awtyp = IDOC,
-- awkey = docnum) and their acdoca lines; partner mapped to the system qualified name; IDoc status 53/51/64 to
-- posted/rejected/pending.
WITH lines AS (
  SELECT b.awkey AS docnum, min(b.gjahr || '-' || b.monat) AS period,
         max(((to_date(b.cpudt, 'YYYYMMDD') + b.cputm::time) AT TIME ZONE 'UTC')) AS posted_at,
         count(a.docln) AS n, coalesce(sum(a.hsl) FILTER (WHERE a.hsl > 0), 0) AS total
  FROM sap_s4hana.bkpf b
  JOIN sap_s4hana.acdoca a ON a.rclnt = b.mandt AND a.rbukrs = b.bukrs AND a.gjahr = b.gjahr AND a.belnr = b.belnr AND a.rldnr = '0L'
  WHERE b.awtyp = 'IDOC'
  GROUP BY b.awkey
)
SELECT
  e.docnum::varchar(40) AS feed_identifier,
  (CASE e.sndprn WHEN 'OPCENTERRO' THEN 'SoftwareServer::SYS-003::Siemens Opcenter MES' WHEN 'CONCUR_EKG' THEN 'SoftwareServer::SYS-012::SAP Concur' WHEN 'WORKDAY_RO' THEN 'SoftwareServer::SYS-013::Workday HCM' WHEN 'MAXIMO_EKG' THEN 'SoftwareServer::SYS-016::Maximo Asset Management' WHEN 'WMS_EKG' THEN 'SoftwareServer::SYS-019::Warehouse Management System (WMS)' ELSE e.sndprn END)::varchar(60) AS system_identifier,
  coalesce(l.period, substr(e.credat, 1, 4) || '-' || substr(e.credat, 5, 2))::varchar(10) AS accounting_period_code,
  coalesce(l.posted_at, ((to_date(e.upddat, 'YYYYMMDD') + e.updtim::time) AT TIME ZONE 'UTC')) AS feed_posted_timestamp,
  coalesce(l.n, 0)::integer AS feed_line_count,
  coalesce(l.total, 0)::numeric(18,2) AS feed_total_amount,
  (CASE e.status WHEN '53' THEN 'posted' WHEN '51' THEN 'rejected' ELSE 'pending' END)::varchar(20) AS feed_current_status
FROM sap_s4hana.edidc e
LEFT JOIN lines l ON l.docnum = e.docnum
WHERE e.mandt = '300' AND e.direct = '2'
