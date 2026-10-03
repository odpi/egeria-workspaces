-- Subscription: aus_sap_s4hana__supplier_payments - SAP S/4HANA (Austin) receives Supplier Payments
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Subledger Postings depends on it (payment postings)
-- Keeps Austin supplier invoices that Ariba has matched but SAP has not yet posted, staged as vendor invoice
-- documents for BAPI_ACC_DOCUMENT_POST (NEW BAPIACHE09/BAPIACGL09, inventory debit and vendor credit like the INVOIC
-- IDoc postings; posting date set when posted). Invoices already posted (reference on BKPF), unmatched or variance
-- invoices, SAP's own payment instructions (payment run) and Coco and EKG items are discarded.

UPDATE incoming_invoice_match i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
UPDATE incoming_invoice_match i SET discard_reason = 'already posted (INVOIC IDoc)'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.bkpf b WHERE b.mandt = '100' AND b.bukrs = 'US01'
                  AND b.xblnr = left(i.invoice_number, 16) AND b.blart = 'RE');
UPDATE incoming_invoice_match i SET discard_reason = 'not matched in Ariba: awaiting reconciliation'
 WHERE i.discard_reason IS NULL AND i.invoice_match_status <> 'matched';

INSERT INTO sap_s4hana.bapiache09
       (mandt, obj_type, obj_key, obj_sys, bus_act, username, header_txt, comp_code, doc_date, pstng_date,
        fisc_year, fis_period, doc_type, ref_doc_no, currency, zz_status)
SELECT '100', 'ZINV', i.supplier_identifier || '/' || i.invoice_number, 'DATAHUB', 'RFBU', 'ARIBA_RFC', left('Ariba invoice ' || i.invoice_number, 25), 'US01',
       to_char(NULL::date, 'YYYYMMDD'), to_char(NULL::date, 'YYYYMMDD'), to_char(NULL::date, 'YYYY'),
       to_char(NULL::date, 'MM'), 'RE', left(i.invoice_number, 16), i.invoice_currency_code, 'R'
  FROM incoming_invoice_match i WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key) DO UPDATE SET
       header_txt = EXCLUDED.header_txt, doc_date = EXCLUDED.doc_date, pstng_date = EXCLUDED.pstng_date,
       fisc_year = EXCLUDED.fisc_year, fis_period = EXCLUDED.fis_period, ref_doc_no = EXCLUDED.ref_doc_no,
       currency = EXCLUDED.currency;
INSERT INTO sap_s4hana.bapiacgl09
       (mandt, obj_type, obj_key, itemno_acc, gl_account, item_text, costcenter, vendor_no, customer, amt_doccur,
        alloc_nmbr)
SELECT '100', 'ZINV', i.supplier_identifier || '/' || i.invoice_number, v.itemno, v.acct,
       left('Ariba invoice ' || i.invoice_number, 50), NULL, v.vendor, NULL, v.amount, left(i.order_identifier, 18)
  FROM incoming_invoice_match i
  CROSS JOIN LATERAL (VALUES ('0000000001', '0001300100', NULL::varchar, i.invoice_total_amount),
                             ('0000000002', '0002100000', lpad(i.supplier_identifier, 10, '0'), -i.invoice_total_amount))
                     AS v(itemno, acct, vendor, amount)
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key, itemno_acc) DO UPDATE SET
       gl_account = EXCLUDED.gl_account, item_text = EXCLUDED.item_text, costcenter = EXCLUDED.costcenter,
       vendor_no = EXCLUDED.vendor_no, customer = EXCLUDED.customer, amt_doccur = EXCLUDED.amt_doccur,
       alloc_nmbr = EXCLUDED.alloc_nmbr;

UPDATE incoming_payment_instruction i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
UPDATE incoming_payment_instruction SET discard_reason = 'already held: payment run of this system'
 WHERE discard_reason IS NULL;
