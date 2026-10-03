-- Subscription: aus_informatica_mdm__payment_anomaly_findings - Informatica MDM (Austin) receives Payment Anomaly Findings
-- Destination: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Why it subscribes: Supplier Master Data depends on it (raise supplier concern)
-- Keeps anomaly findings about Austin suppliers in the C_L_PARTY_SCREENING landing table (screen status REV, anomaly
-- reference set), so the supplier's golden risk status shows the concern. Findings about workers or other estates'
-- suppliers, and the monitored transactions behind them, are discarded.

UPDATE incoming_anomaly_finding i SET discard_reason = 'not a supplier finding'
 WHERE i.supplier_identifier IS NULL;
UPDATE incoming_anomaly_finding i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.discard_reason IS NULL AND i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO informatica_mdm.c_l_party_screening
       (rowid_system, pkey_src_object, party_src_key, screen_status_cd, screened_dt, risk_rating_cd, screening_ref,
        anomaly_ref, notes_txt)
SELECT 'DATA_HUB', i.anomaly_identifier, i.supplier_identifier, 'REV', i.anomaly_detected_timestamp::date,
       upper(i.anomaly_severity), NULL, i.anomaly_identifier, i.anomaly_type || ': ' || i.anomaly_description
  FROM incoming_anomaly_finding i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       party_src_key = EXCLUDED.party_src_key, screened_dt = EXCLUDED.screened_dt,
       risk_rating_cd = EXCLUDED.risk_rating_cd, anomaly_ref = EXCLUDED.anomaly_ref, notes_txt = EXCLUDED.notes_txt;

UPDATE incoming_monitored_transaction SET discard_reason = 'transaction detail not mastered in MDM';
