-- Extract: Maximo Asset Management (Bucharest) -> Equipment Qualification Status / qualification_status
-- Source: bucharest_systems.maximo (SoftwareServer::SYS-016::Maximo Asset Management)
-- Target: coco_data_hub.equipment_qualification_status.qualification_status
-- assetspec GMP_QUAL_STATUS; last closed QUAL/CAL work orders give the dates, the QUAL/CAL pm nextdate the end dates.
WITH last_wo AS (
  SELECT assetnum, siteid, worktype, max(actfinish)::date AS done
  FROM maximo.workorder WHERE status IN ('COMP', 'CLOSE') GROUP BY assetnum, siteid, worktype
)
SELECT
  a.assetnum::varchar(40) AS equipment_identifier,
  (CASE s.alnvalue WHEN 'QUALIFIED' THEN 'qualified' WHEN 'REQUAL DUE' THEN 'requalification due'
        ELSE 'not qualified' END)::varchar(20) AS equipment_qualified_status,
  q.done AS equipment_qualified_date,
  qp.nextdate AS equipment_qualified_end_date,
  c.done AS equipment_calibration_date,
  cp.nextdate AS equipment_calibration_end_date
FROM maximo.asset a
JOIN maximo.assetspec s ON s.assetnum = a.assetnum AND s.siteid = a.siteid AND s.assetattrid = 'GMP_QUAL_STATUS'
JOIN last_wo q ON q.assetnum = a.assetnum AND q.siteid = a.siteid AND q.worktype = 'QUAL'
JOIN last_wo c ON c.assetnum = a.assetnum AND c.siteid = a.siteid AND c.worktype = 'CAL'
JOIN maximo.pm qp ON qp.assetnum = a.assetnum AND qp.siteid = a.siteid AND qp.worktype = 'QUAL'
JOIN maximo.pm cp ON cp.assetnum = a.assetnum AND cp.siteid = a.siteid AND cp.worktype = 'CAL'
