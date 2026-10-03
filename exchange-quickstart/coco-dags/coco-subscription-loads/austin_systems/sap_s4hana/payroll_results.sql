-- Subscription: aus_sap_s4hana__payroll_results - SAP S/4HANA (Austin) receives Payroll Results
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Subledger Postings depends on it (payroll postings)
-- Keeps Austin (US01) payroll runs not yet posted, staged as one accounting document per run for
-- BAPI_ACC_DOCUMENT_POST (NEW BAPIACHE09/BAPIACGL09: cost per account and cost centre against accrued payroll). Runs
-- for periods already posted through Workday's ACC_DOCUMENT IDoc (all of them today), and Coco and EKG payrolls, are
-- discarded; postings are not kept per worker.

UPDATE incoming_payroll_run i SET discard_reason = 'other estate: not the Austin (US01) payroll'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_payroll_run i SET discard_reason = 'already posted via the Workday ACC_DOCUMENT IDoc'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.edidc e
                 JOIN sap_s4hana.bkpf b ON b.mandt = e.mandt AND b.awtyp = 'IDOC' AND b.awkey = e.docnum
                WHERE e.mandt = '100' AND e.mestyp = 'ACC_DOCUMENT' AND e.sndprn = 'WORKDAY_US'
                  AND b.bukrs = 'US01' AND b.gjahr || '-' || b.monat = i.payroll_period_code);

INSERT INTO sap_s4hana.bapiache09
       (mandt, obj_type, obj_key, obj_sys, bus_act, username, header_txt, comp_code, doc_date, pstng_date,
        fisc_year, fis_period, doc_type, ref_doc_no, currency, zz_status)
SELECT '100', 'ZPAY', i.payroll_run_identifier, 'DATAHUB', 'RFBU', 'WORKDAY_RFC', left('Payroll ' || i.payroll_run_identifier, 25), 'US01',
       to_char(i.payroll_run_date, 'YYYYMMDD'), to_char(i.payroll_run_date, 'YYYYMMDD'), to_char(i.payroll_run_date, 'YYYY'),
       to_char(i.payroll_run_date, 'MM'), 'SA', left(i.payroll_run_identifier, 16), i.payroll_currency_code, 'R'
  FROM incoming_payroll_run i WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key) DO UPDATE SET
       header_txt = EXCLUDED.header_txt, doc_date = EXCLUDED.doc_date, pstng_date = EXCLUDED.pstng_date,
       fisc_year = EXCLUDED.fisc_year, fis_period = EXCLUDED.fis_period, ref_doc_no = EXCLUDED.ref_doc_no,
       currency = EXCLUDED.currency;

UPDATE incoming_payroll_posting i SET discard_reason = 'run not staged (other estate or already posted)'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.bapiache09 h
                    WHERE h.mandt = '100' AND h.obj_type = 'ZPAY' AND h.obj_key = i.payroll_run_identifier);
INSERT INTO sap_s4hana.bapiacgl09
       (mandt, obj_type, obj_key, itemno_acc, gl_account, item_text, costcenter, vendor_no, customer, amt_doccur,
        alloc_nmbr)
SELECT '100', 'ZPAY', g.run, lpad(row_number() OVER (PARTITION BY g.run ORDER BY g.acct, g.cc)::text, 10, '0'),
       g.acct, 'Payroll cost', g.cc, NULL, NULL, g.amount, g.run
  FROM (SELECT i.payroll_run_identifier AS run, lpad(i.ledger_account_code, 10, '0') AS acct, i.cost_centre_code AS cc,
               sum(i.payroll_gross_amount + i.payroll_employer_amount) AS amount
          FROM incoming_payroll_posting i WHERE i.discard_reason IS NULL GROUP BY 1, 2, 3) g
ON CONFLICT (mandt, obj_type, obj_key, itemno_acc) DO UPDATE SET
       gl_account = EXCLUDED.gl_account, item_text = EXCLUDED.item_text, costcenter = EXCLUDED.costcenter,
       vendor_no = EXCLUDED.vendor_no, customer = EXCLUDED.customer, amt_doccur = EXCLUDED.amt_doccur,
       alloc_nmbr = EXCLUDED.alloc_nmbr;
INSERT INTO sap_s4hana.bapiacgl09
       (mandt, obj_type, obj_key, itemno_acc, gl_account, item_text, costcenter, vendor_no, customer, amt_doccur,
        alloc_nmbr)
SELECT '100', 'ZPAY', i.payroll_run_identifier, '9999999999', '0002300100', 'Accrued payroll and withholdings',
       NULL, NULL, NULL, -sum(i.payroll_gross_amount + i.payroll_employer_amount), i.payroll_run_identifier
  FROM incoming_payroll_posting i WHERE i.discard_reason IS NULL GROUP BY i.payroll_run_identifier
ON CONFLICT (mandt, obj_type, obj_key, itemno_acc) DO UPDATE SET
       gl_account = EXCLUDED.gl_account, item_text = EXCLUDED.item_text, costcenter = EXCLUDED.costcenter,
       vendor_no = EXCLUDED.vendor_no, customer = EXCLUDED.customer, amt_doccur = EXCLUDED.amt_doccur,
       alloc_nmbr = EXCLUDED.alloc_nmbr;
