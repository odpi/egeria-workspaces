-- Subscription: coco_procurement01__payment_anomaly_findings - Coco Pharmaceuticals Procurement (Coco core) receives Payment Anomaly Findings
-- Destination: coco_pharma.procurement01 (System::procurement01)
-- Why it subscribes: Supplier Master Data depends on it (raise supplier concern)
-- Keeps findings about Coco vendors (numeric supplier ids below 100000) or Coco workers (CW- pseudonyms) and
-- their monitored transactions in anomaly_alert and anomaly_alert_txn (both NEW) for a buyer to review; only a
-- confirmed concern becomes a vendor_anomaly row.  Discards findings about Austin or EKG suppliers and
-- workers.  No system supplies this product yet, so nothing arrives today.

UPDATE incoming_anomaly_finding SET discard_reason = 'Austin or EKG supplier or worker - not a procurement01 vendor'
 WHERE NOT (coalesce(supplier_identifier, '') ~ '^[0-9]{1,5}$' OR coalesce(worker_pseudonym_identifier, '') LIKE 'CW-%');

INSERT INTO procurement01.anomaly_alert (alert_ref, detected_ts, alert_type, vendor_no, worker_ref, alert_text, severity, alert_status)
SELECT f.anomaly_identifier, f.anomaly_detected_timestamp, f.anomaly_type,
       (CASE WHEN f.supplier_identifier ~ '^[0-9]{1,5}$' THEN f.supplier_identifier::integer END),
       f.worker_pseudonym_identifier, f.anomaly_description, f.anomaly_severity, f.anomaly_current_status
  FROM incoming_anomaly_finding f
 WHERE f.discard_reason IS NULL
ON CONFLICT (alert_ref) DO UPDATE SET detected_ts = EXCLUDED.detected_ts, alert_type = EXCLUDED.alert_type,
       vendor_no = EXCLUDED.vendor_no, worker_ref = EXCLUDED.worker_ref, alert_text = EXCLUDED.alert_text,
       severity = EXCLUDED.severity, alert_status = EXCLUDED.alert_status;

UPDATE incoming_monitored_transaction t SET discard_reason = 'transaction of a finding procurement01 does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM procurement01.anomaly_alert a WHERE a.alert_ref = t.anomaly_identifier);

INSERT INTO procurement01.anomaly_alert_txn (alert_ref, txn_ref, txn_type, txn_amount, txn_date)
SELECT t.anomaly_identifier, t.transaction_identifier, t.transaction_type, t.transaction_amount, t.transaction_date
  FROM incoming_monitored_transaction t
 WHERE t.discard_reason IS NULL
ON CONFLICT (alert_ref, txn_ref) DO UPDATE SET txn_type = EXCLUDED.txn_type, txn_amount = EXCLUDED.txn_amount,
       txn_date = EXCLUDED.txn_date;
