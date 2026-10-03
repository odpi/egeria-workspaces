-- Subscription: buc_sap_s4hana__supplier_payments - SAP ERP S/4HANA (Bucharest) receives Supplier Payments
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Subledger Postings depends on it (payment postings)
-- SAP S/4HANA is the source of EKG's supplier payments (invoice verification rbkp/rseg and the payment run
-- reguh/regup), so every EKG invoice match and payment instruction is already held here and is discarded (no feedback
-- loop); payments to other suppliers are discarded as Coco group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_invoice_match i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_payment_instruction i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_invoice_match SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_payment_instruction SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
