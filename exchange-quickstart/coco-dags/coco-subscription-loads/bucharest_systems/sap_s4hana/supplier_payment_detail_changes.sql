-- Subscription: buc_sap_s4hana__supplier_payment_detail_changes - SAP ERP S/4HANA (Bucharest) receives Supplier Payment Detail Changes
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Supplier Master Data depends on it (verified bank details)
-- EKG changes and verifies supplier bank details in SAP S/4HANA itself (change documents and the zekg_bank_verif
-- call-back record), so a change for an EKG supplier (vendor in lfa1) is already held and is discarded; other changes
-- are discarded as Coco group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_payment_detail_change i SET discard_reason = 'EKG bank changes are made and verified in SAP - already held'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_verification_evidence e SET discard_reason = 'EKG bank changes are made and verified in SAP - already held'
 WHERE EXISTS (SELECT 1 FROM incoming_payment_detail_change c WHERE c.payment_detail_change_identifier = e.payment_detail_change_identifier
                AND c.discard_reason <> 'Coco group data - EKG not yet integrated')
    OR EXISTS (SELECT 1 FROM sap_s4hana.zekg_bank_verif z WHERE z.mandt = '300' AND z.changenr = e.payment_detail_change_identifier);
UPDATE incoming_payment_detail_change SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_verification_evidence SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
