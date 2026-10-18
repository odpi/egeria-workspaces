-- Subscription: aus_manhattan_wms__material_quarantine_dispositions - Manhattan WMS (Austin) receives Material Quarantine Dispositions
-- Destination: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Why it subscribes: Goods Inventory Stock depends on it (release for use)
-- Keeps the SAP usage decisions on Austin lots: batch_master status (R released, X rejected) and expiry date are set
-- from each release disposition, so the lot becomes allocatable - the change the quarantine extract is meant to
-- report; it is a no-op while WMS and SAP agree. The quarantine records are Manhattan's own, and Coco's Austin
-- Inventory and EKG lots are other estates': all discarded.

UPDATE incoming_quarantine_record i SET discard_reason = 'already held: supplied by Manhattan (batch master)'
 WHERE EXISTS (SELECT 1 FROM manhattan_wms.batch_master b WHERE b.batch_nbr = i.lot_identifier);
UPDATE incoming_quarantine_record SET discard_reason = 'other estate: not an Austin warehouse lot'
 WHERE discard_reason IS NULL;

UPDATE incoming_release_disposition i SET discard_reason = 'other estate: not an Austin lot'
 WHERE i.lot_identifier !~ '^(RM|A)[0-9]{2}-';
UPDATE incoming_release_disposition i SET discard_reason = 'lot not held in the WMS'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM manhattan_wms.batch_master b WHERE b.batch_nbr = i.lot_identifier);
UPDATE incoming_release_disposition i SET discard_reason = 'superseded by a later disposition'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM incoming_release_disposition j WHERE j.lot_identifier = i.lot_identifier
                  AND j.lot_disposition_timestamp > i.lot_disposition_timestamp);
UPDATE manhattan_wms.batch_master b
   SET batch_status = CASE WHEN i.lot_disposition_status LIKE 'released%' THEN 'R' ELSE 'X' END,
       expire_date = coalesce(i.lot_expiry_date, b.expire_date),
       mod_dttm = i.lot_disposition_timestamp
  FROM incoming_release_disposition i
 WHERE i.discard_reason IS NULL AND b.batch_nbr = i.lot_identifier
   AND (b.batch_status, b.expire_date) IS DISTINCT FROM
       (CASE WHEN i.lot_disposition_status LIKE 'released%' THEN 'R' ELSE 'X' END, coalesce(i.lot_expiry_date, b.expire_date));
