-- Subscription: aus_opcenter_mes__laboratory_test_results - Siemens Opcenter MES (Austin) receives Laboratory Test Results
-- Destination: austin_systems.opcenter_mes (SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601)
-- Why it subscribes: Batch Execution Records depends on it (in-process results)
-- Keeps the in-process and finished-product samples of Austin batches the MES executed (a container with that name)
-- and their results, in the NEW qualitysample and qualityresult tables the step logic checks before moving a batch
-- on. Raw-material samples, certificates of analysis (released through the EBR) and EKG results are discarded.

UPDATE incoming_sample i SET discard_reason = 'raw material sample: no batch in the MES'
 WHERE i.batch_identifier IS NULL AND coalesce(i.lot_identifier, '') ~ '^RM[0-9]{2}-';
UPDATE incoming_sample i SET discard_reason = 'other estate: not an Austin sample'
 WHERE i.discard_reason IS NULL AND coalesce(i.batch_identifier, '') !~ '^A[0-9]{2}-';
UPDATE incoming_sample i SET discard_reason = 'batch not executed in the MES'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
INSERT INTO opcenter_mes.qualitysample (samplename, containerid, sampletype, sampledate, samplestatus)
SELECT i.sample_identifier, c.containerid, i.sample_type, i.sample_collection_timestamp, i.sample_current_status
  FROM incoming_sample i JOIN opcenter_mes.container c ON c.containername = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (samplename) DO UPDATE SET
       containerid = EXCLUDED.containerid, sampletype = EXCLUDED.sampletype, sampledate = EXCLUDED.sampledate,
       samplestatus = EXCLUDED.samplestatus;

UPDATE incoming_test_result i SET discard_reason = 'sample not kept by the MES'
 WHERE NOT EXISTS (SELECT 1 FROM opcenter_mes.qualitysample s WHERE s.samplename = i.sample_identifier);
INSERT INTO opcenter_mes.qualityresult
       (resultname, samplename, testname, resultvalue, uom, lowerlimit, upperlimit, passfail, completeddate, analyst)
SELECT i.test_result_identifier, i.sample_identifier, i.test_code, i.test_value, i.test_unit,
       i.specification_minimum_value, i.specification_maximum_value,
       CASE WHEN i.test_conformity_flag THEN 'Pass' ELSE 'Fail' END, i.test_completed_timestamp, i.test_analyst_identifier
  FROM incoming_test_result i
 WHERE i.discard_reason IS NULL
ON CONFLICT (resultname) DO UPDATE SET
       samplename = EXCLUDED.samplename, testname = EXCLUDED.testname, resultvalue = EXCLUDED.resultvalue,
       uom = EXCLUDED.uom, lowerlimit = EXCLUDED.lowerlimit, upperlimit = EXCLUDED.upperlimit,
       passfail = EXCLUDED.passfail, completeddate = EXCLUDED.completeddate, analyst = EXCLUDED.analyst;

UPDATE incoming_certificate_of_analysis i SET discard_reason = 'other estate: not an Austin lot or batch'
 WHERE coalesce(i.batch_identifier, i.lot_identifier, '') !~ '^(A|RM)[0-9]{2}-';
UPDATE incoming_certificate_of_analysis SET discard_reason = 'certificate of analysis not used in execution'
 WHERE discard_reason IS NULL;
