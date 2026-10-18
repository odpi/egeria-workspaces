-- Extract: SAP ERP S/4HANA (Bucharest) -> Treatment Invoices / revenue_recognition
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.treatment_invoices.revenue_recognition
-- Named-patient billing documents joined to the revenue line of their accounting document (awtyp VBRK, account
-- 701000); revenue is the credit amount; delivery date from vbrp.fbuda.
SELECT
  k.xblnr::varchar(40) AS invoice_number,
  to_date(a.budat, 'YYYYMMDD') AS revenue_recognition_date,
  (-a.hsl)::numeric(18,2) AS revenue_amount,
  to_date(p.fbuda, 'YYYYMMDD') AS order_delivery_date,
  ltrim(a.racct, '0')::varchar(20) AS ledger_account_code
FROM sap_s4hana.vbrk k
JOIN sap_s4hana.vbrp p ON p.mandt = k.mandt AND p.vbeln = k.vbeln AND p.posnr = '000010'
JOIN sap_s4hana.acdoca a ON a.rclnt = k.mandt AND a.awtyp = 'VBRK' AND a.awref = k.vbeln AND a.racct = '0000701000'
WHERE k.mandt = '300' AND a.rldnr = '0L' AND k.fkart = 'ZNPF'
