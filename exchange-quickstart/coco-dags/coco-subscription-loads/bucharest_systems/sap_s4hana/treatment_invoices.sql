-- Subscription: buc_sap_s4hana__treatment_invoices - SAP ERP S/4HANA (Bucharest) receives Treatment Invoices
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Subledger Postings depends on it (revenue postings)
-- SAP S/4HANA is the source of EKG's named-patient invoices (billing documents vbrk fkart ZNPF), so every EKG invoice
-- and revenue line is already held here and is discarded (no feedback loop); other invoices are discarded as Coco group
-- data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_invoice i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.vbrk k WHERE k.mandt = '300' AND k.xblnr = i.invoice_number);
UPDATE incoming_revenue_recognition i SET discard_reason = 'EKG data supplied by this system - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.vbrk k WHERE k.mandt = '300' AND k.xblnr = i.invoice_number);
UPDATE incoming_invoice SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_revenue_recognition SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
