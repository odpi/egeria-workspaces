-- Extract: Siemens Opcenter MES (Austin) -> Batch Execution Records / material_usage
-- Source: austin_systems.opcenter_mes (SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601)
-- Target: coco_data_hub.batch_execution_records.material_usage
-- componentissuehistory joined to its step and batch.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  h.stepsequence AS execution_step_number,
  ci.fromlot::varchar(40) AS lot_identifier,
  ci.issuedproductname::varchar(20) AS raw_material_code,
  ci.qtyissued::double precision AS raw_material_used_quantity,
  ci.uom::varchar(20) AS raw_material_used_unit
FROM opcenter_mes.componentissuehistory ci
JOIN opcenter_mes.historymainline h ON h.historymainlineid = ci.historymainlineid
JOIN opcenter_mes.container c ON c.containerid = h.containerid
