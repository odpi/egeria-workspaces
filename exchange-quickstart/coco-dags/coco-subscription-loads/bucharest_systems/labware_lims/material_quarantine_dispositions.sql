-- Subscription: buc_labware_lims__material_quarantine_dispositions - LIMS LabWare Enterprise (Bucharest) receives Material Quarantine Dispositions
-- Destination: bucharest_systems.labware_lims (SoftwareServer::SYS-004::LIMS LabWare Enterprise)
-- Why it subscribes: Laboratory Test Results depends on it (request incoming testing)
-- Keeps EKG lots placed in quarantine by the WMS (RO10 warehouse) that are not yet logged in as a LIMS lot, as incoming
-- testing requests in the new custom table c_quarantine_request; lots already logged in are discarded.  The usage
-- decision is SAP's decision on this LIMS lot approval, so LIMS keeps nothing from it.  Coco and Austin lots are
-- discarded (EKG is not yet integrated).
UPDATE incoming_quarantine_record SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE warehouse_code IS NULL OR warehouse_code NOT LIKE 'RO10-%';
UPDATE incoming_quarantine_record i SET discard_reason = 'lot already logged in LIMS'
 WHERE i.discard_reason IS NULL AND EXISTS (SELECT 1 FROM labware_lims.lot l WHERE l.lot_name = i.lot_identifier);
UPDATE incoming_release_disposition i SET discard_reason = 'usage decision follows this LIMS lot approval - already held'
 WHERE EXISTS (SELECT 1 FROM labware_lims.lot l WHERE l.lot_name = i.lot_identifier)
    OR EXISTS (SELECT 1 FROM labware_lims.c_quarantine_request q WHERE q.lot_name = i.lot_identifier);
UPDATE incoming_release_disposition SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO labware_lims.c_quarantine_request (lot_name, product, receipt_ref, quarantined_on, location, quantity,
                                               wms_sample_ref, wms_status, request_status, received_on)
SELECT i.lot_identifier, coalesce(i.raw_material_code, '?'), i.goods_receipt_identifier, i.lot_quarantine_start_timestamp,
       i.warehouse_code, i.lot_quantity, i.sample_identifier, i.lot_quarantine_status, 'P', now()
  FROM incoming_quarantine_record i
 WHERE i.discard_reason IS NULL
ON CONFLICT (lot_name) DO UPDATE
   SET product = EXCLUDED.product, receipt_ref = EXCLUDED.receipt_ref, quarantined_on = EXCLUDED.quarantined_on,
       location = EXCLUDED.location, quantity = EXCLUDED.quantity, wms_sample_ref = EXCLUDED.wms_sample_ref,
       wms_status = EXCLUDED.wms_status
 WHERE (labware_lims.c_quarantine_request.product, labware_lims.c_quarantine_request.receipt_ref,
        labware_lims.c_quarantine_request.quarantined_on, labware_lims.c_quarantine_request.location,
        labware_lims.c_quarantine_request.quantity, labware_lims.c_quarantine_request.wms_sample_ref,
        labware_lims.c_quarantine_request.wms_status)
       IS DISTINCT FROM (EXCLUDED.product, EXCLUDED.receipt_ref, EXCLUDED.quarantined_on, EXCLUDED.location,
                         EXCLUDED.quantity, EXCLUDED.wms_sample_ref, EXCLUDED.wms_status);
