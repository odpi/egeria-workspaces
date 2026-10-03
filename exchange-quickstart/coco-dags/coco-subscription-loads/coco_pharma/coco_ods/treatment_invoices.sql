-- Subscription: coco_ods__treatment_invoices - Coco Pharmaceuticals Operational Data Store (Coco core) receives Treatment Invoices
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills orders (invoiced values)
-- Keeps the invoiced value of Coco orders already in the ODS: order_details.unit_price becomes the invoice total
-- divided by the quantity ordered (the ODS has no invoice table).  Discards invoices for orders not in the ODS -
-- today all Coco invoices, because their orders could not be loaded (customers missing) - Austin's and EKG's
-- invoices, and revenue recognition, which the ODS does not hold.

UPDATE incoming_invoice SET discard_reason = 'Austin or EKG invoice - not a Coco customer order'
 WHERE order_identifier NOT LIKE 'SO-%';
UPDATE incoming_invoice i SET discard_reason = 'order not in the ODS'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ods.order_details d
                    WHERE d.order_id = (CASE WHEN right(i.order_identifier, 5) ~ '^[0-9]{5}$' THEN right(i.order_identifier, 5)::integer END));

UPDATE coco_ods.order_details d SET unit_price = (i.invoice_total_amount / d.quantity)::real
  FROM incoming_invoice i
 WHERE i.discard_reason IS NULL AND d.order_id = (CASE WHEN right(i.order_identifier, 5) ~ '^[0-9]{5}$' THEN right(i.order_identifier, 5)::integer END)
   AND d.quantity > 0
   AND d.unit_price IS DISTINCT FROM (i.invoice_total_amount / d.quantity)::real;

UPDATE incoming_revenue_recognition SET discard_reason = 'the ODS holds no revenue recognition';
