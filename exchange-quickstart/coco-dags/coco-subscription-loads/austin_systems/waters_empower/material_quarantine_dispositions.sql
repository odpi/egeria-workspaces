-- Subscription: aus_waters_empower__material_quarantine_dispositions - Waters Empower 3 (Austin) receives Material Quarantine Dispositions
-- Destination: austin_systems.waters_empower (SoftwareServer::AUS-SYS-027::SN-CHR-AU-20180615)
-- Why it subscribes: Laboratory Test Results depends on it (request incoming testing)
-- Keeps the Austin lots still held in quarantine with a LIMS sample, as NEW lims_sample_request rows (the Empower
-- LIMS interface sample list from which the chromatography sample set is built). Lots already released or rejected,
-- release dispositions (not CDS business), Coco's Austin Inventory lots and EKG lots are discarded.

UPDATE incoming_quarantine_record i SET discard_reason = 'other estate: not an Austin (Manhattan) warehouse'
 WHERE i.warehouse_code NOT IN ('AUS1', 'AUS2');
UPDATE incoming_quarantine_record i SET discard_reason = 'lot already dispositioned'
 WHERE i.discard_reason IS NULL AND i.lot_quarantine_status <> 'held';
UPDATE incoming_quarantine_record i SET discard_reason = 'no LIMS sample to test'
 WHERE i.discard_reason IS NULL AND i.sample_identifier IS NULL;
INSERT INTO waters_empower.lims_sample_request
       (sample_name, lot_name, material, requested_on, request_status)
SELECT i.sample_identifier, i.lot_identifier, i.raw_material_code, i.lot_quarantine_start_timestamp, 'Pending'
  FROM incoming_quarantine_record i
 WHERE i.discard_reason IS NULL
ON CONFLICT (sample_name) DO UPDATE SET
       lot_name = EXCLUDED.lot_name, material = EXCLUDED.material, requested_on = EXCLUDED.requested_on;

UPDATE incoming_release_disposition SET discard_reason = 'lot dispositions not kept by the CDS';
