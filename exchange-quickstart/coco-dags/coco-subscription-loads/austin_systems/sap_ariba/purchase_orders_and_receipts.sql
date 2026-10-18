-- Subscription: aus_sap_ariba__purchase_orders_and_receipts - SAP Ariba SRM (Austin) receives Purchase Orders And Receipts
-- Destination: austin_systems.sap_ariba (SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617)
-- Why it subscribes: Supplier Payments depends on it (order and receipt)
-- Keeps the Austin purchase orders (Austin suppliers) and their goods receipt confirmations as ERP copies in the NEW
-- erp_purchase_order and erp_receipt tables, which invoice reconciliation matches invoices against;
-- invoice_reconciliation, which feeds Supplier Payments, only changes when an invoice is reconciled. Orders of other
-- estates' suppliers, and receipts for orders it does not hold, are discarded.

UPDATE incoming_purchase_order i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO sap_ariba.erp_purchase_order
       (po_number, erp_vendor_id, order_date, total_amount, currency, approver, order_status)
SELECT i.order_identifier, i.supplier_identifier, i.order_date, i.order_total_amount, i.order_currency_code,
       i.order_approver_identifier, i.order_current_status
  FROM incoming_purchase_order i
 WHERE i.discard_reason IS NULL
ON CONFLICT (po_number) DO UPDATE SET
       erp_vendor_id = EXCLUDED.erp_vendor_id, order_date = EXCLUDED.order_date,
       total_amount = EXCLUDED.total_amount, currency = EXCLUDED.currency, approver = EXCLUDED.approver,
       order_status = EXCLUDED.order_status;

UPDATE incoming_goods_receipt_confirmation i SET discard_reason = 'order not held (other estate)'
 WHERE NOT EXISTS (SELECT 1 FROM sap_ariba.erp_purchase_order p WHERE p.po_number = i.order_identifier);
INSERT INTO sap_ariba.erp_receipt (receipt_id, po_number, po_line_number, receipt_date, received_qty)
SELECT i.goods_receipt_identifier, i.order_identifier, i.line_item_number, i.goods_receipt_date,
       i.goods_receipt_quantity
  FROM incoming_goods_receipt_confirmation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (receipt_id, po_number, po_line_number) DO UPDATE SET
       receipt_date = EXCLUDED.receipt_date, received_qty = EXCLUDED.received_qty;
