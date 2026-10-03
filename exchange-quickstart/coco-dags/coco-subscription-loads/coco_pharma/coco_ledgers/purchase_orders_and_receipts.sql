-- Subscription: coco_ledgers__purchase_orders_and_receipts - Coco Ledgers (Coco core) receives Purchase Orders And Receipts
-- Destination: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Why it subscribes: Supplier Payments depends on it (order and receipt)
-- Keeps orders placed with Coco suppliers (numeric supplier ids below 100000) and their receipt confirmations
-- in ap_po and ap_po_receipt (both NEW), the order and receipt legs of the three-way match for ap_invoice.
-- Discards Austin (100xxx) and EKG (700xxx) suppliers' orders, which are paid by the acquired estates' own
-- payables.  No system supplies this product yet, so nothing arrives today.

UPDATE incoming_purchase_order SET discard_reason = 'Austin or EKG supplier - paid by the acquired estate''s own payables'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO coco_ledgers.ap_po (po_no, vendor_no, po_date, po_amount, ccy, approved_by, po_status)
SELECT o.order_identifier, o.supplier_identifier::integer, o.order_date, o.order_total_amount, o.order_currency_code,
       o.order_approver_identifier, o.order_current_status
  FROM incoming_purchase_order o
 WHERE o.discard_reason IS NULL
ON CONFLICT (po_no) DO UPDATE SET vendor_no = EXCLUDED.vendor_no, po_date = EXCLUDED.po_date, po_amount = EXCLUDED.po_amount,
       ccy = EXCLUDED.ccy, approved_by = EXCLUDED.approved_by, po_status = EXCLUDED.po_status;

UPDATE incoming_goods_receipt_confirmation r SET discard_reason = 'receipt against an order Coco Ledgers does not pay'
 WHERE NOT EXISTS (SELECT 1 FROM coco_ledgers.ap_po p WHERE p.po_no = r.order_identifier);

INSERT INTO coco_ledgers.ap_po_receipt (grn_ref, po_no, line_no, rcv_date, rcv_qty)
SELECT r.goods_receipt_identifier, r.order_identifier, r.line_item_number, r.goods_receipt_date, r.goods_receipt_quantity
  FROM incoming_goods_receipt_confirmation r
 WHERE r.discard_reason IS NULL
ON CONFLICT (grn_ref, po_no, line_no) DO UPDATE SET rcv_date = EXCLUDED.rcv_date, rcv_qty = EXCLUDED.rcv_qty;
