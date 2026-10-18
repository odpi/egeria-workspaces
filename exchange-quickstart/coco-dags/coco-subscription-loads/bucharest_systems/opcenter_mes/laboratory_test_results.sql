-- Subscription: buc_opcenter_mes__laboratory_test_results - Siemens Opcenter MES (Bucharest) receives Laboratory Test Results
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results)
-- Keeps the in-process control samples of EKG batches of this MES and their results (LabWare and Empower) in the new
-- tables labsample and labresult, which release the next step.  Finished-product results reach the EBR as the batch's
-- certificate of analysis through the LabWare interface (LABRESULTS section), so finished-product samples, results and
-- certificates are discarded, as are raw-material ones (released by SAP QM) and other companies' (Coco group data - EKG
-- is not yet integrated).
UPDATE incoming_sample i SET discard_reason = 'finished product results reach the EBR as the certificate of analysis'
 WHERE i.sample_type IS DISTINCT FROM 'in-process'
   AND EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_sample SET discard_reason = 'raw material sample - released by SAP QM, not the MES'
 WHERE discard_reason IS NULL AND lot_identifier ~ '^MP[0-9]{2}-[0-9]{4}$';
UPDATE incoming_sample i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);

INSERT INTO opcenter_mes.labsample (samplename, containerid, sampletype, collectiondate, samplestatus, lastchangedate)
SELECT i.sample_identifier, c.containerid, i.sample_type, i.sample_collection_timestamp, i.sample_current_status, now()
  FROM incoming_sample i JOIN opcenter_mes.container c ON c.containername = i.batch_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (samplename) DO UPDATE
   SET containerid = EXCLUDED.containerid, sampletype = EXCLUDED.sampletype, collectiondate = EXCLUDED.collectiondate,
       samplestatus = EXCLUDED.samplestatus, lastchangedate = now()
 WHERE (opcenter_mes.labsample.containerid, opcenter_mes.labsample.sampletype, opcenter_mes.labsample.collectiondate,
        opcenter_mes.labsample.samplestatus)
       IS DISTINCT FROM (EXCLUDED.containerid, EXCLUDED.sampletype, EXCLUDED.collectiondate, EXCLUDED.samplestatus);

UPDATE incoming_test_result r SET discard_reason = s.discard_reason
  FROM incoming_sample s
 WHERE s.sample_identifier = r.sample_identifier AND s.discard_reason IS NOT NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.labsample l WHERE l.samplename = r.sample_identifier);
UPDATE incoming_test_result r SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE r.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.labsample l WHERE l.samplename = r.sample_identifier);

INSERT INTO opcenter_mes.labresult (resultname, samplename, testcode, resultvalue, uom, lowerlimit, upperlimit, passflag,
                                    completeddate, analyst)
SELECT r.test_result_identifier, r.sample_identifier, coalesce(r.test_code, '?'), r.test_value, r.test_unit,
       r.specification_minimum_value, r.specification_maximum_value, (CASE WHEN r.test_conformity_flag THEN 1 ELSE 0 END),
       r.test_completed_timestamp, r.test_analyst_identifier
  FROM incoming_test_result r
 WHERE r.discard_reason IS NULL
ON CONFLICT (resultname) DO UPDATE
   SET samplename = EXCLUDED.samplename, testcode = EXCLUDED.testcode, resultvalue = EXCLUDED.resultvalue, uom = EXCLUDED.uom,
       lowerlimit = EXCLUDED.lowerlimit, upperlimit = EXCLUDED.upperlimit, passflag = EXCLUDED.passflag,
       completeddate = EXCLUDED.completeddate, analyst = EXCLUDED.analyst;

UPDATE incoming_certificate_of_analysis i SET discard_reason = 'already referenced in the EBR (LABRESULTS section)'
 WHERE EXISTS (SELECT 1 FROM opcenter_mes.ebrsectionref s WHERE s.sectiontype = 'LABRESULTS' AND s.externalref = i.certificate_identifier);
UPDATE incoming_certificate_of_analysis i SET discard_reason = 'reaches the EBR through the LabWare interface (LABRESULTS section)'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier);
UPDATE incoming_certificate_of_analysis SET discard_reason = 'raw material certificate - not part of the batch record'
 WHERE discard_reason IS NULL AND lot_identifier ~ '^MP[0-9]{2}-[0-9]{4}$';
UPDATE incoming_certificate_of_analysis SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
