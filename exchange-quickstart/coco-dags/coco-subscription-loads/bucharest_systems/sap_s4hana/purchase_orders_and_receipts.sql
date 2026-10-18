-- Subscription: buc_sap_s4hana__purchase_orders_and_receipts - SAP ERP S/4HANA (Bucharest) receives Purchase Orders And Receipts
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Supplier Payments depends on it (order and receipt)
-- EKG's purchase orders are created and received in SAP S/4HANA itself, so an EKG order (supplier in lfa1) or goods
-- receipt (an EKG order or an inspection lot of the receipt) is already held and is discarded; other orders are
-- discarded as Coco group data (EKG is not yet integrated).  Nothing is written.  The product has no source yet.
UPDATE incoming_purchase_order i SET discard_reason = 'EKG purchase orders are created in SAP - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_goods_receipt_confirmation g SET discard_reason = 'EKG goods receipts are posted in SAP - already held'
 WHERE EXISTS (SELECT 1 FROM incoming_purchase_order o WHERE o.order_identifier = g.order_identifier AND o.discard_reason IS NOT NULL
                AND o.discard_reason <> 'Coco group data - EKG not yet integrated')
    OR EXISTS (SELECT 1 FROM sap_s4hana.qals q WHERE q.mandt = '300' AND q.ebeln = g.order_identifier)
    OR EXISTS (SELECT 1 FROM sap_s4hana.rseg r WHERE r.mandt = '300' AND r.ebeln = g.order_identifier);
UPDATE incoming_purchase_order SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_goods_receipt_confirmation SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
