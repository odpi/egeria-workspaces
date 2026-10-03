-- Subscription: aus_manhattan_wms__laboratory_test_results - Manhattan WMS (Austin) receives Laboratory Test Results
-- Destination: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Why it subscribes: Material Quarantine Dispositions depends on it (test results)
-- Keeps the laboratory's certificate of analysis for each Austin lot or batch the WMS holds (batch_master) in the
-- NEW batch_coa table, which the receiving team checks before asking for release; the lot status itself changes only
-- on the SAP usage decision. Individual samples and test results (not WMS business), lots unknown to the WMS and EKG
-- results are discarded.

UPDATE incoming_sample i SET discard_reason = 'other estate: not an Austin sample'
 WHERE coalesce(i.batch_identifier, i.lot_identifier, '') !~ '^(RM|A)[0-9]{2}-';
UPDATE incoming_sample SET discard_reason = 'samples not kept by the WMS' WHERE discard_reason IS NULL;
UPDATE incoming_test_result i SET discard_reason = 'other estate: not an Austin sample'
 WHERE i.sample_identifier !~ '^S[0-9]{2}-0[0-9]{5}$';
UPDATE incoming_test_result SET discard_reason = 'individual results not kept by the WMS' WHERE discard_reason IS NULL;

UPDATE incoming_certificate_of_analysis i SET discard_reason = 'other estate: not an Austin lot or batch'
 WHERE coalesce(i.lot_identifier, i.batch_identifier, '') !~ '^(RM|A)[0-9]{2}-';
UPDATE incoming_certificate_of_analysis i SET discard_reason = 'lot not held in the WMS'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM manhattan_wms.batch_master b
                    WHERE b.batch_nbr = coalesce(i.lot_identifier, i.batch_identifier));
INSERT INTO manhattan_wms.batch_coa (batch_nbr, coa_nbr, coa_date, conforming, approved_by)
SELECT coalesce(i.lot_identifier, i.batch_identifier), i.certificate_identifier, i.certificate_date,
       CASE WHEN i.certificate_conformity_flag THEN 'Y' ELSE 'N' END, i.certificate_approver_identifier
  FROM incoming_certificate_of_analysis i
 WHERE i.discard_reason IS NULL
ON CONFLICT (batch_nbr, coa_nbr) DO UPDATE SET
       coa_date = EXCLUDED.coa_date, conforming = EXCLUDED.conforming, approved_by = EXCLUDED.approved_by;
