-- Subscription: buc_sap_s4hana__supplier_master_data - SAP ERP S/4HANA (Bucharest) receives Supplier Master Data
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Supplier Payments depends on it (supplier and payment details)
-- SAP S/4HANA is the source of EKG's supplier master (lfa1, lfbk, the screening and bank-verification Z tables), so
-- every EKG supplier, risk status and payment detail is already held here and is discarded (no feedback loop); other
-- suppliers are discarded as Coco group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_supplier i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_supplier_risk_status i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_supplier_payment_details i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_supplier SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_supplier_risk_status SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_supplier_payment_details SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
