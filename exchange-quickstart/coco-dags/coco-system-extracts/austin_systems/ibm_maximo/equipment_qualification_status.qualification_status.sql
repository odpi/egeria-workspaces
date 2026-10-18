-- Extract: IBM Maximo CMMS (Austin) -> Equipment Qualification Status / qualification_status
-- Source: austin_systems.ibm_maximo (SoftwareServer::AUS-SYS-029::SN-CMM-AU-20190401)
-- Target: coco_data_hub.equipment_qualification_status.qualification_status
-- assetspec GMP_QUAL_STATUS; last completed QUAL/CAL work orders give the dates, the QUAL/CAL pm nextdate the end
-- dates.
WITH last_wo AS (
  SELECT assetnum, siteid, worktype, max(actfinish)::date AS done
  FROM ibm_maximo.workorder WHERE status IN ('COMP', 'CLOSE') GROUP BY assetnum, siteid, worktype
)
SELECT
  a.assetnum::varchar(40) AS equipment_identifier,
  (CASE s.alnvalue WHEN 'QUALIFIED' THEN 'qualified' WHEN 'REQUAL DUE' THEN 'requalification due'
        ELSE 'not qualified' END)::varchar(20) AS equipment_qualified_status,
  q.done AS equipment_qualified_date,
  qp.nextdate AS equipment_qualified_end_date,
  c.done AS equipment_calibration_date,
  cp.nextdate AS equipment_calibration_end_date
FROM ibm_maximo.asset a
JOIN ibm_maximo.assetspec s ON s.assetnum = a.assetnum AND s.siteid = a.siteid AND s.assetattrid = 'GMP_QUAL_STATUS'
JOIN last_wo q ON q.assetnum = a.assetnum AND q.siteid = a.siteid AND q.worktype = 'QUAL'
JOIN last_wo c ON c.assetnum = a.assetnum AND c.siteid = a.siteid AND c.worktype = 'CAL'
JOIN ibm_maximo.pm qp ON qp.assetnum = a.assetnum AND qp.siteid = a.siteid AND qp.worktype = 'QUAL'
JOIN ibm_maximo.pm cp ON cp.assetnum = a.assetnum AND cp.siteid = a.siteid AND cp.worktype = 'CAL'
