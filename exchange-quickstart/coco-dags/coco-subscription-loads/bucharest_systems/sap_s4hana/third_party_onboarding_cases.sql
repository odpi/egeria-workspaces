-- Subscription: buc_sap_s4hana__third_party_onboarding_cases - SAP ERP S/4HANA (Bucharest) receives Third Party Onboarding Cases
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Supplier Master Data depends on it (create supplier record)
-- EKG onboards and screens its own suppliers in SAP S/4HANA (vendor creation and zekg_vend_scrn), so a case whose
-- supplier is already an EKG vendor is discarded as already held, and the Coco and Austin onboarding cases in the
-- product are discarded as Coco group data (EKG is not yet integrated).  Nothing is written (creating vendors from the
-- product would feed back into Supplier Master Data).
UPDATE incoming_onboarding_case i SET discard_reason = 'supplier already created in SAP'
 WHERE i.supplier_identifier IS NOT NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_screening_request s SET discard_reason = 'supplier already created in SAP'
 WHERE EXISTS (SELECT 1 FROM incoming_onboarding_case c WHERE c.onboarding_case_identifier = s.onboarding_case_identifier
                AND c.discard_reason = 'supplier already created in SAP');
UPDATE incoming_onboarding_case SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_screening_request SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
