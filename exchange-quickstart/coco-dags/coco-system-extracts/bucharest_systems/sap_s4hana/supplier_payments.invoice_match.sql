-- Extract: SAP ERP S/4HANA (Bucharest) -> Supplier Payments / invoice_match
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.supplier_payments.invoice_match
-- Supplier invoices (rbkp) with their first item (rseg: purchase order, goods receipt material document); status from
-- invoice status and payment block.
SELECT
  r.xblnr::varchar(40) AS invoice_number,
  ltrim(r.lifnr, '0')::varchar(40) AS supplier_identifier,
  i.ebeln::varchar(40) AS order_identifier,
  i.lfbnr::varchar(40) AS goods_receipt_identifier,
  r.rmwwr::numeric(18,2) AS invoice_total_amount,
  r.waers::varchar(3) AS invoice_currency_code,
  (CASE WHEN r.rbstat = 'A' THEN 'parked' WHEN r.zlspr = 'R' THEN 'price variance' WHEN r.zlspr = 'Q' THEN 'quality block'
        ELSE 'matched' END)::varchar(20) AS invoice_match_status
FROM sap_s4hana.rbkp r
JOIN sap_s4hana.rseg i ON i.mandt = r.mandt AND i.belnr = r.belnr AND i.gjahr = r.gjahr AND i.buzei = '000001'
WHERE r.mandt = '300'
