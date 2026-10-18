-- Subscription: buc_empower_cds__material_quarantine_dispositions - Empower Chromatography (Bucharest) receives Material Quarantine Dispositions
-- Destination: bucharest_systems.empower_cds (SoftwareServer::SYS-027::Empower Chromatography)
-- Why it subscribes: Laboratory Test Results depends on it (request incoming testing)
-- Empower does not take testing requests from the warehouse: incoming testing is requested in LabWare LIMS, which
-- creates the Empower sample sets, so nothing is written.  EKG lots (RO10 warehouse, MPyy-nnnn lots) are discarded for
-- that reason; Coco and Austin lots as Coco group data (EKG is not yet integrated).
UPDATE incoming_quarantine_record SET discard_reason = 'testing is requested through LabWare LIMS, not Empower'
 WHERE warehouse_code LIKE 'RO10-%' OR lot_identifier ~ '^MP[0-9]{2}-[0-9]{4}$';
UPDATE incoming_quarantine_record SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_release_disposition SET discard_reason = 'usage decisions are not kept in Empower'
 WHERE lot_identifier ~ '^MP[0-9]{2}-[0-9]{4}$';
UPDATE incoming_release_disposition SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
