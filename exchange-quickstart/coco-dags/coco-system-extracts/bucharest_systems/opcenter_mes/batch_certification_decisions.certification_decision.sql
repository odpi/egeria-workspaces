-- Extract: Siemens Opcenter MES (Bucharest) -> Batch Certification Decisions / certification_decision
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.batch_certification_decisions.certification_decision
-- Releases reviewed by exception in the MES (no QMS disposition reference; batches with a deviation are certified in
-- Veeva QMS); completeness from ebrheader.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  r.marketcode::varchar(8) AS market_code,
  e.employeename::varchar(40) AS batch_certifier_identifier,
  r.certdate AS batch_certification_date,
  (CASE r.decision WHEN 'Released' THEN 'certified' ELSE 'rejected' END)::varchar(20) AS batch_certification_status,
  r.releasedqty AS batch_released_quantity,
  (h.reviewcompleteflag = 1) AS batch_record_complete_flag,
  NULL::varchar(40) AS deviation_identifier,
  r.comments AS batch_certification_notes,
  r.storagecondition AS shipment_storage_description
FROM opcenter_mes.batchreleasehistory r
JOIN opcenter_mes.container c ON c.containerid = r.containerid
JOIN opcenter_mes.employee e ON e.employeeid = r.qpemployeeid
JOIN opcenter_mes.ebrheader h ON h.containerid = r.containerid
WHERE r.qmsdispositionref IS NULL
