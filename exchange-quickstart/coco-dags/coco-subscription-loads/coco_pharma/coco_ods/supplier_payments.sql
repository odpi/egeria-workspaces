-- Subscription: coco_ods__supplier_payments - Coco Pharmaceuticals Operational Data Store (Coco core) receives Supplier Payments
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills supplier_invoices
-- Keeps the invoices of Coco suppliers (numeric ids below 100000) that have been paid in supplier_invoices:
-- supplier, the order number's digits as supply_order_number, the amount, the invoice number's digits as
-- invoice_number and the payment authorisation date as invoice_date (the only date the product carries);
-- supplier and invoice number identify the row (the table has no key).  Discards unpaid invoices (no date yet),
-- Austin's and EKG's invoices and payments, and payments once their date has been used.

UPDATE incoming_invoice_match SET discard_reason = 'Austin or EKG supplier - not a Coco supplier'
 WHERE coalesce((CASE WHEN supplier_identifier ~ '^[0-9]{1,5}$' THEN supplier_identifier::integer END), 99999) > 32767;
UPDATE incoming_invoice_match SET discard_reason = 'invoice or order number has no digits'
 WHERE discard_reason IS NULL AND (invoice_number !~ '[0-9]' OR order_identifier !~ '[0-9]');
UPDATE incoming_invoice_match m SET discard_reason = 'not paid yet - no invoice date'
 WHERE m.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM incoming_payment_instruction p
                    WHERE p.supplier_identifier = m.supplier_identifier AND p.invoice_number = m.invoice_number);

UPDATE coco_ods.supplier_invoices s
   SET supply_order_number = nullif(regexp_replace(m.order_identifier, '[^0-9]', '', 'g'), '')::numeric,
       invoice_amount = m.invoice_total_amount::money, invoice_date = p.paid_on
  FROM incoming_invoice_match m
  JOIN (SELECT supplier_identifier, invoice_number, min(payment_authorised_timestamp)::date AS paid_on
          FROM incoming_payment_instruction GROUP BY supplier_identifier, invoice_number) p
    ON p.supplier_identifier = m.supplier_identifier AND p.invoice_number = m.invoice_number
 WHERE m.discard_reason IS NULL
   AND s.supplier_id::text = m.supplier_identifier
   AND s.invoice_number = nullif(regexp_replace(m.invoice_number, '[^0-9]', '', 'g'), '')::numeric
   AND (s.supply_order_number, s.invoice_amount, s.invoice_date)
       IS DISTINCT FROM (nullif(regexp_replace(m.order_identifier, '[^0-9]', '', 'g'), '')::numeric, m.invoice_total_amount::money, p.paid_on);

INSERT INTO coco_ods.supplier_invoices (supplier_id, supply_order_number, invoice_amount, invoice_number, invoice_date)
SELECT m.supplier_identifier::smallint, nullif(regexp_replace(m.order_identifier, '[^0-9]', '', 'g'), '')::numeric,
       m.invoice_total_amount::money, nullif(regexp_replace(m.invoice_number, '[^0-9]', '', 'g'), '')::numeric, p.paid_on
  FROM incoming_invoice_match m
  JOIN (SELECT supplier_identifier, invoice_number, min(payment_authorised_timestamp)::date AS paid_on
          FROM incoming_payment_instruction GROUP BY supplier_identifier, invoice_number) p
    ON p.supplier_identifier = m.supplier_identifier AND p.invoice_number = m.invoice_number
 WHERE m.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ods.supplier_invoices s
                    WHERE s.supplier_id::text = m.supplier_identifier
                      AND s.invoice_number = nullif(regexp_replace(m.invoice_number, '[^0-9]', '', 'g'), '')::numeric);

UPDATE incoming_payment_instruction p SET discard_reason = 'payment of an invoice the ODS does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM incoming_invoice_match m
                    WHERE m.discard_reason IS NULL AND m.supplier_identifier = p.supplier_identifier
                      AND m.invoice_number = p.invoice_number);
UPDATE incoming_payment_instruction SET discard_reason = 'payments are not held - the payment date is used as the invoice date'
 WHERE discard_reason IS NULL;
