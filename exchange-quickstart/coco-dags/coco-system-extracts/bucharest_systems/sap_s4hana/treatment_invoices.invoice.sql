-- Extract: SAP ERP S/4HANA (Bucharest) -> Treatment Invoices / invoice
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.treatment_invoices.invoice
-- Named-patient billing documents (vbrk.fkart = ZNPF) with the sales order from vbrp, gross = net + VAT, the net due
-- date of the customer line in acdoca; open items past due are overdue, cleared items paid.
SELECT
  k.xblnr::varchar(40) AS invoice_number,
  to_date(k.fkdat, 'YYYYMMDD') AS invoice_date,
  ltrim(p.aubel, '0')::varchar(40) AS order_identifier,
  ltrim(k.kunrg, '0')::varchar(40) AS customer_identifier,
  (k.netwr + k.mwsbk)::numeric(18,2) AS invoice_total_amount,
  k.waerk::varchar(3) AS invoice_currency_code,
  to_date(a.netdt, 'YYYYMMDD') AS invoice_due_date,
  (CASE WHEN a.augbl IS NOT NULL THEN 'paid' WHEN to_date(a.netdt, 'YYYYMMDD') < current_date THEN 'overdue'
        ELSE 'open' END)::varchar(20) AS invoice_current_status
FROM sap_s4hana.vbrk k
JOIN sap_s4hana.vbrp p ON p.mandt = k.mandt AND p.vbeln = k.vbeln AND p.posnr = '000010'
JOIN sap_s4hana.acdoca a ON a.rclnt = k.mandt AND a.awtyp = 'VBRK' AND a.awref = k.vbeln AND a.koart = 'D' AND a.rldnr = '0L'
WHERE k.mandt = '300' AND k.fkart = 'ZNPF'
