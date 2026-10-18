-- Extract: Workday Human Capital Management (Austin) -> Payroll Results / payroll_run
-- Source: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Target: coco_data_hub.payroll_results.payroll_run
-- pay_run header (worker count and gross total cover salaried and hourly workers).
SELECT
  r.pay_run_id::varchar(40) AS payroll_run_identifier,
  r.company_id::varchar(10) AS legal_entity_code,
  to_char(r.period_end_date, 'YYYY-MM')::varchar(10) AS payroll_period_code,
  r.payment_date AS payroll_run_date,
  r.worker_count AS payroll_run_count,
  r.total_gross_amount::numeric(18,2) AS payroll_run_total_amount,
  r.currency::varchar(3) AS payroll_currency_code
FROM workday_hcm.pay_run r
WHERE r.status = 'Complete'
