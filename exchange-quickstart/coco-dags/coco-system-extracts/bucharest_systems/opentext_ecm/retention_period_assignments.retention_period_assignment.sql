-- Extract: OpenText ECM (Bucharest) -> Retention Period Assignments / retention_period_assignment
-- Source: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Target: coco_data_hub.retention_period_assignments.retention_period_assignment
-- rm_docxref joined to the RSI and the assigning user; asset identifier = OTCS node id.
SELECT
  ('OTCS-' || x.dataid)::varchar(40) AS asset_identifier,
  r.rsi_code::varchar(40) AS retention_obligation_identifier,
  (r.title || ': ' || r.description) AS retention_basis_description,
  x.calc_archive_date AS retention_archive_date,
  x.calc_destroy_date AS retention_delete_date,
  x.rsi_assigned AS retention_assigned_timestamp,
  lower(k.name)::varchar(40) AS retention_assigner_identifier
FROM opentext_ecm.rm_docxref x
JOIN opentext_ecm.rm_rsi r ON r.rsi_id = x.rsi_id
JOIN opentext_ecm.kuaf k ON k.id = x.assigned_by
