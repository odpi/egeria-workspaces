-- Subscription: coco_ods__purchase_orders_and_receipts - Coco Pharmaceuticals Operational Data Store (Coco core) receives Purchase Orders And Receipts
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills supply_orders, supply_order_details
-- Keeps orders placed with Coco suppliers (numeric ids below 100000) in supply_orders: the order number's digits
-- as supply_order_number (the same number supplier_invoices uses), the order date, and the order number itself as
-- supplier_reference, which identifies the row (supply_orders has no key).  Discards Austin's and EKG's orders and
-- the receipt confirmations: supply_order_details needs a product and prices, which the product does not carry.
-- No system supplies this product yet.

UPDATE incoming_purchase_order SET discard_reason = 'Austin or EKG supplier - not a Coco order'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';
UPDATE incoming_purchase_order SET discard_reason = 'order number has no digits or is too long for supplier_reference'
 WHERE discard_reason IS NULL AND (order_identifier !~ '[0-9]' OR length(order_identifier) > 20);

UPDATE coco_ods.supply_orders s SET order_date = o.order_date
  FROM incoming_purchase_order o
 WHERE o.discard_reason IS NULL AND s.supplier_reference = o.order_identifier AND s.order_date IS DISTINCT FROM o.order_date;

INSERT INTO coco_ods.supply_orders (supply_order_number, order_date, supplier_reference)
SELECT nullif(regexp_replace(o.order_identifier, '[^0-9]', '', 'g'), '')::numeric, o.order_date, o.order_identifier
  FROM incoming_purchase_order o
 WHERE o.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ods.supply_orders s WHERE s.supplier_reference = o.order_identifier);

UPDATE incoming_goods_receipt_confirmation SET discard_reason = 'supply_order_details needs a product and prices, which are not supplied';
