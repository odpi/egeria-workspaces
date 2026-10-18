-- Subscription: buc_sap_s4hana__payment_anomaly_findings - SAP ERP S/4HANA (Bucharest) receives Payment Anomaly Findings
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Supplier Master Data depends on it (raise supplier concern)
-- Keeps payment anomaly findings that implicate an EKG vendor (lfa1) in the new Z table zekg_pay_anom, worked by
-- accounts payable before the next payment run; the screening table and vendor block are not changed (the supplier
-- extracts read them).  The monitored transactions are SAP's own documents and are discarded; findings with no
-- supplier (expense-claim patterns) belong to Concur; other findings are Coco group data (EKG not yet integrated).
-- The product has no source yet.
UPDATE incoming_anomaly_finding SET discard_reason = 'no supplier implicated - expense findings are handled in Concur'
 WHERE supplier_identifier IS NULL;
UPDATE incoming_anomaly_finding i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_monitored_transaction t SET discard_reason = 'transaction is an SAP document - already held'
 WHERE EXISTS (SELECT 1 FROM incoming_anomaly_finding f WHERE f.anomaly_identifier = t.anomaly_identifier AND f.discard_reason IS NULL)
    OR EXISTS (SELECT 1 FROM sap_s4hana.zekg_pay_anom z WHERE z.mandt = '300' AND z.anomaly_id = t.anomaly_identifier);
UPDATE incoming_monitored_transaction SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO sap_s4hana.zekg_pay_anom (mandt, anomaly_id, lifnr, anom_type, severity, anom_status, det_date, det_time, descr)
SELECT '300', left(i.anomaly_identifier, 20), lpad(i.supplier_identifier, 10, '0'), coalesce(i.anomaly_type, 'other'),
       i.anomaly_severity, coalesce(i.anomaly_current_status, 'open'),
       to_char(i.anomaly_detected_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD'), to_char(i.anomaly_detected_timestamp AT TIME ZONE 'UTC', 'HH24MISS'),
       i.anomaly_description
  FROM incoming_anomaly_finding i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, anomaly_id) DO UPDATE
   SET lifnr = EXCLUDED.lifnr, anom_type = EXCLUDED.anom_type, severity = EXCLUDED.severity, anom_status = EXCLUDED.anom_status,
       det_date = EXCLUDED.det_date, det_time = EXCLUDED.det_time, descr = EXCLUDED.descr;
