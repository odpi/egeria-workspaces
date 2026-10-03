-- Subscription: coco_ods__treatment_orders - Coco Pharmaceuticals Operational Data Store (Coco core) receives Treatment Orders
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills orders, order_details
-- Keeps Coco's orders (globalCRM SO- orders) for customers the ODS knows: an orders row (order_id from the order
-- number's last five digits, customer, order date) and an order_details row for the product and quantity, priced
-- when the invoice arrives (Treatment Invoices).  Today every Coco order is discarded because its hospital is not
-- in coco_ods.customers, which orders.customer_id must reference - there is no customer master product.  Also
-- discards Austin's orders (TO-), the ODS's own sample collection details, and orders for products not in the ODS.

UPDATE incoming_treatment_order SET discard_reason = 'Austin order - not a Coco customer order'
 WHERE order_identifier NOT LIKE 'SO-%';
UPDATE incoming_treatment_order o SET discard_reason = 'customer ' || o.hospital_identifier || ' not in coco_ods.customers (no customer master product)'
 WHERE o.discard_reason IS NULL AND NOT EXISTS (SELECT 1 FROM coco_ods.customers c WHERE c.customer_id = o.hospital_identifier);
UPDATE incoming_treatment_order o SET discard_reason = 'product not in the ODS'
 WHERE o.discard_reason IS NULL
   AND (o.product_code !~ '^[0-9]{1,4}$' OR NOT EXISTS (SELECT 1 FROM coco_ods.products p WHERE p.product_id::text = o.product_code));
UPDATE incoming_treatment_order SET discard_reason = 'order number does not fit the ODS order_id'
 WHERE discard_reason IS NULL
   AND coalesce((CASE WHEN right(order_identifier, 5) ~ '^[0-9]{5}$' THEN right(order_identifier, 5)::integer END), 99999) > 32767;

INSERT INTO coco_ods.orders (order_id, customer_id, order_date)
SELECT DISTINCT ON (right(o.order_identifier, 5)) right(o.order_identifier, 5)::smallint, o.hospital_identifier, o.order_date
  FROM incoming_treatment_order o
 WHERE o.discard_reason IS NULL
 ORDER BY right(o.order_identifier, 5), o.order_date DESC
ON CONFLICT (order_id) DO UPDATE SET customer_id = EXCLUDED.customer_id, order_date = EXCLUDED.order_date;

INSERT INTO coco_ods.order_details (order_id, product_id, unit_price, quantity, discount)
SELECT DISTINCT ON (right(o.order_identifier, 5), o.product_code)
       right(o.order_identifier, 5)::smallint, o.product_code::smallint, 0, o.order_quantity, 0
  FROM incoming_treatment_order o
 WHERE o.discard_reason IS NULL
 ORDER BY right(o.order_identifier, 5), o.product_code, o.order_date DESC
ON CONFLICT (order_id, product_id) DO UPDATE SET quantity = EXCLUDED.quantity;

UPDATE incoming_sample_collection_request SET discard_reason = 'the ODS holds no sample collection details';
