-- Subscription: aus_sap_s4hana__employee_expense_claims - SAP S/4HANA (Austin) receives Employee Expense Claims
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Subledger Postings depends on it (expense postings)
-- Keeps expense claims of Austin claimants (cost centre CC-US..) staged as accounting documents for
-- BAPI_ACC_DOCUMENT_POST (NEW BAPIACHE09 header, BAPIACGL09 lines; account assigned at posting from the expense
-- type). Austin has no expense system feeding the hub, so today every claim is Coco's (posted in Coco Ledgers) or
-- EKG's (SAP Concur) and is discarded, as are the claimant approval limits (expense-system business).

UPDATE incoming_claimant_cost_centre i SET discard_reason = CASE WHEN i.cost_centre_code LIKE 'CC-US%'
       THEN 'approval limits are held in the expense system' ELSE 'other estate: not an Austin cost centre' END;

UPDATE incoming_claim_submission i SET discard_reason = 'other estate: claimant not on an Austin cost centre'
 WHERE NOT EXISTS (SELECT 1 FROM incoming_claimant_cost_centre c
                    WHERE c.worker_pseudonym_identifier = i.worker_pseudonym_identifier
                      AND c.cost_centre_code LIKE 'CC-US%');
UPDATE incoming_claim_submission i SET discard_reason = 'claim not approved for payment'
 WHERE i.discard_reason IS NULL AND i.claim_current_status NOT IN ('approved', 'paid');

INSERT INTO sap_s4hana.bapiache09
       (mandt, obj_type, obj_key, obj_sys, bus_act, username, header_txt, comp_code, doc_date, pstng_date,
        fisc_year, fis_period, doc_type, ref_doc_no, currency, zz_status)
SELECT '100', 'ZEXP', i.claim_identifier, 'DATAHUB', 'RFBU', 'EXPENSE_RFC', left('Expense claim ' || i.claim_identifier, 25), 'US01',
       to_char(i.claim_submitted_timestamp, 'YYYYMMDD'), to_char(i.claim_submitted_timestamp, 'YYYYMMDD'), to_char(i.claim_submitted_timestamp, 'YYYY'),
       to_char(i.claim_submitted_timestamp, 'MM'), 'KR', left(i.claim_identifier, 16), i.claim_currency_code, 'R'
  FROM incoming_claim_submission i WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key) DO UPDATE SET
       header_txt = EXCLUDED.header_txt, doc_date = EXCLUDED.doc_date, pstng_date = EXCLUDED.pstng_date,
       fisc_year = EXCLUDED.fisc_year, fis_period = EXCLUDED.fis_period, ref_doc_no = EXCLUDED.ref_doc_no,
       currency = EXCLUDED.currency;

UPDATE incoming_claim_line i SET discard_reason = 'claim not staged (other estate or not approved)'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.bapiache09 h
                    WHERE h.mandt = '100' AND h.obj_type = 'ZEXP' AND h.obj_key = i.claim_identifier);
INSERT INTO sap_s4hana.bapiacgl09
       (mandt, obj_type, obj_key, itemno_acc, gl_account, item_text, costcenter, vendor_no, customer, amt_doccur,
        alloc_nmbr)
SELECT '100', 'ZEXP', i.claim_identifier, lpad(i.claim_line_number::text, 10, '0'), NULL,
       left(i.claim_line_type || ': ' || i.claim_line_description, 50), c.cost_centre_code, NULL, NULL,
       i.claim_line_amount, i.claim_line_evidence_identifier
  FROM incoming_claim_line i
  JOIN incoming_claim_submission s ON s.claim_identifier = i.claim_identifier
  LEFT JOIN incoming_claimant_cost_centre c ON c.worker_pseudonym_identifier = s.worker_pseudonym_identifier
                                           AND c.cost_centre_code LIKE 'CC-US%'
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, obj_type, obj_key, itemno_acc) DO UPDATE SET
       gl_account = EXCLUDED.gl_account, item_text = EXCLUDED.item_text, costcenter = EXCLUDED.costcenter,
       vendor_no = EXCLUDED.vendor_no, customer = EXCLUDED.customer, amt_doccur = EXCLUDED.amt_doccur,
       alloc_nmbr = EXCLUDED.alloc_nmbr;
