-- Extract: LIMS LabWare Enterprise (Bucharest) -> Laboratory Test Results / certificate_of_analysis
-- Source: bucharest_systems.labware_lims (SoftwareServer::SYS-004::LIMS LabWare Enterprise)
-- Target: coco_data_hub.laboratory_test_results.certificate_of_analysis
-- Approved or rejected lots carrying an EKG certificate (BA- release bulletin for raw lots, CA- certificate for
-- batches).
SELECT
  l.c_coa_number::varchar(40) AS certificate_identifier,
  (CASE WHEN l.c_lot_type = 'FINISHED' THEN l.lot_name END)::varchar(40) AS batch_identifier,
  (CASE WHEN l.c_lot_type = 'RAW' THEN l.lot_name END)::varchar(40) AS lot_identifier,
  l.c_coa_date AS certificate_date,
  (l.status = 'A') AS certificate_conformity_flag,
  l.approved_by::varchar(40) AS certificate_approver_identifier
FROM labware_lims.lot l
WHERE l.c_coa_number IS NOT NULL AND l.status IN ('A', 'R')
