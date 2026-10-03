-- Extract: Siemens Opcenter MES (Bucharest) -> Batch Execution Records / equipment_usage
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.batch_execution_records.equipment_usage
-- resourceusagehistory joined to resourcedef (asset number), its step and batch; qualification codes mapped to words.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  h.stepsequence AS execution_step_number,
  r.resourcename::varchar(40) AS equipment_identifier,
  (CASE ru.qualstatusatuse WHEN 'Qualified' THEN 'qualified' WHEN 'RequalDue' THEN 'requalification due'
        ELSE 'not qualified' END)::varchar(20) AS equipment_qualified_status,
  ru.calibrationduedateatuse AS equipment_calibration_end_date
FROM opcenter_mes.resourceusagehistory ru
JOIN opcenter_mes.resourcedef r ON r.resourceid = ru.resourceid
JOIN opcenter_mes.historymainline h ON h.historymainlineid = ru.historymainlineid
JOIN opcenter_mes.container c ON c.containerid = h.containerid
