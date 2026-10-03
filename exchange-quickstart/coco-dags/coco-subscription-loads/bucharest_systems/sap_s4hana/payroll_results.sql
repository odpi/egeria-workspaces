-- Subscription: buc_sap_s4hana__payroll_results - SAP ERP S/4HANA (Bucharest) receives Payroll Results
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Subledger Postings depends on it (payroll postings)
-- SAP S/4HANA posts EKG payroll only from Workday's payroll accounting IDoc (partner WORKDAY_RO), so EKG pay runs
-- (company RO01, cost centres RO10-*) are discarded: as already posted where the run's document exists (bkpf xblnr = run),
-- otherwise as awaiting that IDoc - posting them again from the product would double the payroll cost.  Other payrolls
-- are discarded as Coco group data (EKG is not yet integrated).  Nothing is written.
UPDATE incoming_payroll_run i SET discard_reason = 'already posted through the Workday payroll IDoc (WORKDAY_RO)'
 WHERE i.legal_entity_code = 'RO01'
   AND EXISTS (SELECT 1 FROM sap_s4hana.bkpf b WHERE b.mandt = '300' AND b.bukrs = 'RO01' AND b.xblnr = i.payroll_run_identifier);
UPDATE incoming_payroll_run SET discard_reason = 'payroll is posted only from the Workday payroll IDoc'
 WHERE discard_reason IS NULL AND legal_entity_code = 'RO01';
UPDATE incoming_payroll_posting p SET discard_reason = 'already posted through the Workday payroll IDoc (WORKDAY_RO)'
 WHERE EXISTS (SELECT 1 FROM sap_s4hana.bkpf b WHERE b.mandt = '300' AND b.bukrs = 'RO01' AND b.xblnr = p.payroll_run_identifier);
UPDATE incoming_payroll_posting p SET discard_reason = 'payroll is posted only from the Workday payroll IDoc'
 WHERE p.discard_reason IS NULL
   AND (p.cost_centre_code LIKE 'RO10-%'
        OR EXISTS (SELECT 1 FROM incoming_payroll_run r WHERE r.payroll_run_identifier = p.payroll_run_identifier AND r.legal_entity_code = 'RO01'));
UPDATE incoming_payroll_run SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_payroll_posting SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
