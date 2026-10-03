-- Subscription: aus_sap_s4hana__treatment_invoices - SAP S/4HANA (Austin) receives Treatment Invoices
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Subledger Postings depends on it (revenue postings)
-- Keeps Oracle Receivables treatment invoices for Austin orders not yet billed in SAP, staged as customer invoice
-- documents for BAPI_ACC_DOCUMENT_POST (NEW BAPIACHE09/BAPIACGL09: receivable against personalised therapy revenue).
-- Invoices already billed (VBRK reference = Oracle invoice number), SAP's own revenue recognition lines and Coco and
-- EKG invoices are discarded.

UPDATE incoming_invoice i SET discard_reason = 'other estate: not an Austin treatment invoice'
 WHERE i.invoice_number NOT LIKE 'AR-%' OR i.invoice_currency_code <> 'USD';
UPDATE incoming_invoice i SET discard_reason = 'already billed (VBRK)'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.vbrk k WHERE k.mandt = '100' AND k.xblnr = i.invoice_number);

INSERT INTO sap_s4hana.bapiache09
       (mandt, obj_type, obj_key, obj_sys, bus_act, username, header_txt, comp_code, doc_date, pstng_date,
        fisc_year, fis_period, doc_type, ref_doc_no, currency, zz_status)
SELECT '100', 'ZBIL', i.invoice_number, 'DATAHUB', 'RFBU', 'ORACLE_AR', left('Treatment ' || i.order_identifier, 25), 'US01',
       to_char(i.invoice_date, 'YYYYMMDD'), to_char(i.invoice_date, 'YYYYMMDD'), to_char(i.invoice_date, 'YYYY'),
       to_char(i.invoice_date, 'MM'), 'DR', left(i.invoice_number, 16), i.invoice_currency_code, 'R'
  FROM incoming_invoice i WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key) DO UPDATE SET
       header_txt = EXCLUDED.header_txt, doc_date = EXCLUDED.doc_date, pstng_date = EXCLUDED.pstng_date,
       fisc_year = EXCLUDED.fisc_year, fis_period = EXCLUDED.fis_period, ref_doc_no = EXCLUDED.ref_doc_no,
       currency = EXCLUDED.currency;
INSERT INTO sap_s4hana.bapiacgl09
       (mandt, obj_type, obj_key, itemno_acc, gl_account, item_text, costcenter, vendor_no, customer, amt_doccur,
        alloc_nmbr)
SELECT '100', 'ZBIL', i.invoice_number, v.itemno, v.acct, left('Treatment order ' || i.order_identifier, 50), NULL,
       NULL, v.customer, v.amount, left(i.order_identifier, 18)
  FROM incoming_invoice i
  CROSS JOIN LATERAL (VALUES ('0000000001', '0001200000', lpad(i.customer_identifier, 10, '0'), i.invoice_total_amount),
                             ('0000000002', '0004000300', NULL::varchar, -i.invoice_total_amount))
                     AS v(itemno, acct, customer, amount)
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key, itemno_acc) DO UPDATE SET
       gl_account = EXCLUDED.gl_account, item_text = EXCLUDED.item_text, costcenter = EXCLUDED.costcenter,
       vendor_no = EXCLUDED.vendor_no, customer = EXCLUDED.customer, amt_doccur = EXCLUDED.amt_doccur,
       alloc_nmbr = EXCLUDED.alloc_nmbr;

UPDATE incoming_revenue_recognition i SET discard_reason = 'already held: revenue recognised on the SAP billing document'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.vbrk k WHERE k.mandt = '100' AND k.xblnr = i.invoice_number);
UPDATE incoming_revenue_recognition i SET discard_reason = 'other estate: not an Austin treatment invoice'
 WHERE i.discard_reason IS NULL;
