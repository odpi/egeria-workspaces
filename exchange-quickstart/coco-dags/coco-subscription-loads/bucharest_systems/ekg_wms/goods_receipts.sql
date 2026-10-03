-- Subscription: buc_ekg_wms__goods_receipts - Warehouse Management System (WMS) (Bucharest) receives Goods Receipts
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Material Quarantine Dispositions depends on it (place in quarantine)
-- The WMS is the source of EKG's goods receipts (the receipt is identified by the SAP material document it got back), so
-- every EKG receipt and receipt inspection is already held here and is discarded (no feedback loop); Coco and Austin
-- receipts are discarded too (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_goods_receipt i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM ekg_wms.receptii r WHERE r.sap_doc_mat = i.goods_receipt_identifier);
UPDATE incoming_receipt_inspection i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM ekg_wms.receptii r WHERE r.sap_doc_mat = i.goods_receipt_identifier);
UPDATE incoming_goods_receipt SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_receipt_inspection SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
