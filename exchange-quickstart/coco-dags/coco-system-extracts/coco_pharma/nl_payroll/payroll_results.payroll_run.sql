-- Extract: Netherlands payroll (Coco core) -> Payroll Results / payroll_run
-- Source: coco_pharma.nl_payroll (System::NL payroll)
-- Target: coco_data_hub.payroll_results.payroll_run
-- verloningsrun, final runs only; yyyymm period to YYYY-MM.
SELECT
  v.run_id::varchar(40)             AS payroll_run_identifier,
  v.werkgever::varchar(10)          AS legal_entity_code,
  (left(v.periode::text, 4) || '-' || right(v.periode::text, 2))::varchar(10) AS payroll_period_code,
  v.betaaldatum                     AS payroll_run_date,
  v.aantal_medewerkers::integer     AS payroll_run_count,
  v.totaal_bruto::numeric(18,2)     AS payroll_run_total_amount,
  v.valuta::varchar(3)              AS payroll_currency_code
FROM nl_payroll.verloningsrun v
WHERE v.status = 'definitief'
