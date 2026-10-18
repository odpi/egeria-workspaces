-- Extract: Siemens Opcenter MES (Bucharest) -> Electronic Batch Records / release_authorisation
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.electronic_batch_records.release_authorisation
-- batchreleasehistory (decision Released) joined to container and the certifying QP's AD login.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  r.marketcode::varchar(8) AS market_code,
  r.releasedqty AS batch_released_quantity,
  r.certdate AS batch_certification_date,
  e.employeename::varchar(40) AS batch_certifier_identifier
FROM opcenter_mes.batchreleasehistory r
JOIN opcenter_mes.container c ON c.containerid = r.containerid
JOIN opcenter_mes.employee e ON e.employeeid = r.qpemployeeid
WHERE r.decision = 'Released'
