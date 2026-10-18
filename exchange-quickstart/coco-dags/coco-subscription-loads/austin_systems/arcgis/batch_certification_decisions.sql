-- Subscription: aus_arcgis__batch_certification_decisions - Esri ArcGIS Enterprise (Austin) receives Batch Certification Decisions
-- Destination: austin_systems.arcgis (SoftwareServer::AUS-SYS-044::SN-GIS-AU-20230601)
-- Why it subscribes: Therapy Delivery Events depends on it (therapy released)
-- Keeps the release decisions for Austin patient therapy batches (the batches the courier layer tracks) in the NEW
-- therapy_release hosted table, so the dashboard shows which shipments may leave and under what storage conditions.
-- Release of non-patient Austin batches (shipped as ordinary freight) and other estates' batches are discarded; the
-- track point layer is untouched.

UPDATE incoming_certification_decision i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
UPDATE incoming_certification_decision i SET discard_reason = 'not a patient therapy batch tracked in ArcGIS'
 WHERE i.discard_reason IS NULL AND i.batch_identifier !~ '^A[0-9]{2}-[0-9]{4}-P'
   AND NOT EXISTS (SELECT 1 FROM arcgis.therapy_shipment_track_pts t WHERE t.batch_no = i.batch_identifier);
INSERT INTO arcgis.therapy_release
       (batch_no, market, release_status, release_date, released_qty, record_complete, deviation_ref, storage_text)
SELECT i.batch_identifier, i.market_code, i.batch_certification_status, i.batch_certification_date,
       i.batch_released_quantity, i.batch_record_complete_flag, i.deviation_identifier, i.shipment_storage_description
  FROM incoming_certification_decision i
 WHERE i.discard_reason IS NULL
ON CONFLICT (batch_no, market) DO UPDATE SET
       release_status = EXCLUDED.release_status, release_date = EXCLUDED.release_date,
       released_qty = EXCLUDED.released_qty, record_complete = EXCLUDED.record_complete,
       deviation_ref = EXCLUDED.deviation_ref, storage_text = EXCLUDED.storage_text;
