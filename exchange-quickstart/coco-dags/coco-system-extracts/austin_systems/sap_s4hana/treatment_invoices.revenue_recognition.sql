-- Extract: SAP S/4HANA (Austin) -> Treatment Invoices / revenue_recognition
-- Source: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Target: coco_data_hub.treatment_invoices.revenue_recognition
-- Billing documents (vbrk/vbrp) joined to the revenue line of their accounting document in acdoca (awtyp VBRK, G/L
-- account 4*); revenue is the credit amount; invoice number is the Oracle Receivables number in xblnr.
SELECT
  k.xblnr::varchar(40) AS invoice_number,
  to_date(a.budat, 'YYYYMMDD') AS revenue_recognition_date,
  (-a.hsl)::numeric(18,2) AS revenue_amount,
  to_date(p.fbuda, 'YYYYMMDD') AS order_delivery_date,
  ltrim(a.racct, '0')::varchar(20) AS ledger_account_code
FROM sap_s4hana.vbrk k
JOIN sap_s4hana.vbrp p ON p.mandt = k.mandt AND p.vbeln = k.vbeln AND p.posnr = '000010'
JOIN sap_s4hana.acdoca a ON a.rclnt = k.mandt AND a.awtyp = 'VBRK' AND a.awref = k.vbeln AND a.racct LIKE '0004%'
WHERE k.mandt = '100' AND a.rldnr = '0L'
