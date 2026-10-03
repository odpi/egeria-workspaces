-- Subscription: aus_labware_lims__material_quarantine_dispositions - LabWare Enterprise LIMS (Austin) receives Material Quarantine Dispositions
-- Destination: austin_systems.labware_lims (SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820)
-- Why it subscribes: Laboratory Test Results depends on it (request incoming testing)
-- Keeps, for Austin lots placed in quarantine that the laboratory has not yet logged in (no lot row with that lot
-- name), a NEW c_receipt_test_request row from which the sample is logged; lot and sample, which the extracts read,
-- are only written by log-in. Lots already logged, release dispositions (derived from LIMS results), Coco's Austin
-- Inventory lots and EKG lots are discarded.

UPDATE incoming_quarantine_record i SET discard_reason = 'other estate: not an Austin (Manhattan) warehouse'
 WHERE i.warehouse_code NOT IN ('AUS1', 'AUS2');
UPDATE incoming_quarantine_record i SET discard_reason = 'already held: lot logged in LIMS'
 WHERE i.discard_reason IS NULL AND EXISTS (SELECT 1 FROM labware_lims.lot l WHERE l.lot_name = i.lot_identifier);
UPDATE incoming_quarantine_record i SET discard_reason = 'lot no longer in quarantine'
 WHERE i.discard_reason IS NULL AND i.lot_quarantine_status <> 'held';
INSERT INTO labware_lims.c_receipt_test_request
       (lot_name, product, receipt_ref, quarantined_on, warehouse, lot_qty, wms_sample_ref, request_status)
SELECT i.lot_identifier, i.raw_material_code, i.goods_receipt_identifier, i.lot_quarantine_start_timestamp,
       i.warehouse_code, i.lot_quantity, i.sample_identifier, 'P'
  FROM incoming_quarantine_record i
 WHERE i.discard_reason IS NULL
ON CONFLICT (lot_name) DO UPDATE SET
       product = EXCLUDED.product, receipt_ref = EXCLUDED.receipt_ref, quarantined_on = EXCLUDED.quarantined_on,
       warehouse = EXCLUDED.warehouse, lot_qty = EXCLUDED.lot_qty, wms_sample_ref = EXCLUDED.wms_sample_ref;

UPDATE incoming_release_disposition i SET discard_reason = 'other estate: not an Austin lot'
 WHERE i.lot_identifier !~ '^(RM|A)[0-9]{2}-';
UPDATE incoming_release_disposition SET discard_reason = 'already held: disposition follows the LIMS result'
 WHERE discard_reason IS NULL;
