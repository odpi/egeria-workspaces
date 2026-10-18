-- Extract: Netherlands payroll (Coco core) -> Payroll Results / payroll_posting
-- Source: coco_pharma.nl_payroll (System::NL payroll)
-- Target: coco_data_hub.payroll_results.payroll_posting
-- loonstrook for final runs; payroll number to pseudonym via medewerker.
SELECT
  l.run_id::varchar(40)             AS payroll_run_identifier,
  m.worker_ref::varchar(40)         AS worker_pseudonym_identifier,
  l.bruto::numeric(18,2)            AS payroll_gross_amount,
  l.werkgeverslasten::numeric(18,2) AS payroll_employer_amount,
  l.netto::numeric(18,2)            AS payroll_net_amount,
  l.kostenplaats::varchar(20)       AS cost_centre_code,
  l.grootboekrekening::varchar(20)  AS ledger_account_code
FROM nl_payroll.loonstrook l
JOIN nl_payroll.medewerker m ON m.personeelsnr = l.personeelsnr
JOIN nl_payroll.verloningsrun v ON v.run_id = l.run_id
WHERE v.status = 'definitief'
