-- Extract: Workday HCM (Bucharest) -> Payroll Results / payroll_run
-- Source: bucharest_systems.workday_hcm (SoftwareServer::SYS-013::Workday HCM)
-- Target: coco_data_hub.payroll_results.payroll_run
-- Completed pay_run headers (worker count and gross total cover salaried and shift workers).
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
