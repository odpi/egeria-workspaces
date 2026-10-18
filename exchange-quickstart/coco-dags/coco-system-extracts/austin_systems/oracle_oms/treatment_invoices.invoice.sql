-- Extract: Oracle Order Management (Austin) -> Treatment Invoices / invoice
-- Source: austin_systems.oracle_oms (SoftwareServer::AUS-SYS-011::SN-OMS-AU-20200310)
-- Target: coco_data_hub.treatment_invoices.invoice
-- ra_customer_trx_all with summed lines, joined to the originating order (portal order number) and customer account;
-- OP/CL to open/paid.
SELECT
  t.trx_number::varchar(40) AS invoice_number,
  t.trx_date AS invoice_date,
  h.source_order_number::varchar(40) AS order_identifier,
  c.account_number::varchar(40) AS customer_identifier,
  sum(l.extended_amount)::numeric(18,2) AS invoice_total_amount,
  t.invoice_currency_code::varchar(3) AS invoice_currency_code,
  t.term_due_date AS invoice_due_date,
  (CASE t.status_trx WHEN 'CL' THEN 'paid' WHEN 'OP' THEN 'open' ELSE 'credited' END)::varchar(20) AS invoice_current_status
FROM oracle_oms.ra_customer_trx_all t
JOIN oracle_oms.ra_customer_trx_lines_all l ON l.customer_trx_id = t.customer_trx_id AND l.line_type = 'LINE'
JOIN oracle_oms.doo_headers_all h ON h.order_number = t.interface_header_attribute1
JOIN oracle_oms.hz_cust_accounts c ON c.cust_account_id = t.bill_to_customer_id
WHERE t.complete_flag = 'Y'
GROUP BY t.trx_number, t.trx_date, h.source_order_number, c.account_number, t.invoice_currency_code, t.term_due_date, t.status_trx
