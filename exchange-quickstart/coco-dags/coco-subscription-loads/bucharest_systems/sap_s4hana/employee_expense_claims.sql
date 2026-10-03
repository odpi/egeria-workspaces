-- Subscription: buc_sap_s4hana__employee_expense_claims - SAP ERP S/4HANA (Bucharest) receives Employee Expense Claims
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Subledger Postings depends on it (expense postings)
-- Concur posts EKG's approved expenses to SAP as one accounting IDoc a month (partner CONCUR_EKG); SAP keeps each EKG
-- expense report (Concur report ids Ryyyy-*) in the new Z table zekg_cnq_rpt to reconcile it with that IDoc: recon_stat
-- P where the month's IDoc posted, O where an approved report is not yet in a posted IDoc (the September IDoc failed), N
-- not approved.  Lines are posted by the IDoc and cost centres are SAP master data, so both are discarded; Coco and
-- Austin claims are discarded (EKG is not yet integrated).
UPDATE incoming_claim_submission SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE claim_identifier !~ '^R[0-9]{4}-';
UPDATE incoming_claim_line SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE claim_identifier !~ '^R[0-9]{4}-';
UPDATE incoming_claim_line SET discard_reason = 'lines are posted by the Concur accounting IDoc' WHERE discard_reason IS NULL;
UPDATE incoming_claimant_cost_centre SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE cost_centre_code IS NULL OR cost_centre_code NOT LIKE 'RO10-%';
UPDATE incoming_claimant_cost_centre SET discard_reason = 'cost centres are SAP master data' WHERE discard_reason IS NULL;

WITH posted AS (
  SELECT b.xblnr, max(b.awkey) AS docnum
    FROM sap_s4hana.bkpf b
    JOIN sap_s4hana.edidc e ON e.mandt = b.mandt AND e.docnum = b.awkey AND e.sndprn = 'CONCUR_EKG' AND e.status = '53'
   WHERE b.mandt = '300' AND b.awtyp = 'IDOC'
   GROUP BY b.xblnr
), r AS (
  SELECT i.*, p.docnum,
         (to_char(i.claim_submitted_timestamp AT TIME ZONE 'Europe/Bucharest', 'YYYYMMDD')) AS subm_date,
         (to_char(i.claim_submitted_timestamp AT TIME ZONE 'Europe/Bucharest', 'HH24MISS')) AS subm_time
    FROM incoming_claim_submission i
    LEFT JOIN posted p ON p.xblnr = 'CONCUR-' || to_char(i.claim_submitted_timestamp AT TIME ZONE 'Europe/Bucharest', 'YYYY-MM')
                      AND i.claim_current_status IN ('approved', 'paid')
   WHERE i.discard_reason IS NULL
)
INSERT INTO sap_s4hana.zekg_cnq_rpt (mandt, report_id, pseudo_id, subm_date, subm_time, wrbtr, waers, rpt_status, docnum,
                                     recon_stat, aedat)
SELECT '300', r.claim_identifier, r.worker_pseudonym_identifier, r.subm_date, r.subm_time, coalesce(r.claim_total_amount, 0),
       coalesce(r.claim_currency_code, 'RON'), coalesce(r.claim_current_status, 'submitted'), r.docnum,
       (CASE WHEN r.docnum IS NOT NULL THEN 'P' WHEN r.claim_current_status IN ('approved', 'paid') THEN 'O' ELSE 'N' END),
       to_char(now() AT TIME ZONE 'Europe/Bucharest', 'YYYYMMDD')
  FROM r
ON CONFLICT (mandt, report_id) DO UPDATE
   SET pseudo_id = EXCLUDED.pseudo_id, subm_date = EXCLUDED.subm_date, subm_time = EXCLUDED.subm_time,
       wrbtr = EXCLUDED.wrbtr, waers = EXCLUDED.waers, rpt_status = EXCLUDED.rpt_status, docnum = EXCLUDED.docnum,
       recon_stat = EXCLUDED.recon_stat, aedat = EXCLUDED.aedat
 WHERE (sap_s4hana.zekg_cnq_rpt.pseudo_id, sap_s4hana.zekg_cnq_rpt.subm_date, sap_s4hana.zekg_cnq_rpt.subm_time,
        sap_s4hana.zekg_cnq_rpt.wrbtr, sap_s4hana.zekg_cnq_rpt.waers, sap_s4hana.zekg_cnq_rpt.rpt_status,
        sap_s4hana.zekg_cnq_rpt.docnum, sap_s4hana.zekg_cnq_rpt.recon_stat)
       IS DISTINCT FROM (EXCLUDED.pseudo_id, EXCLUDED.subm_date, EXCLUDED.subm_time, EXCLUDED.wrbtr, EXCLUDED.waers,
                         EXCLUDED.rpt_status, EXCLUDED.docnum, EXCLUDED.recon_stat);
