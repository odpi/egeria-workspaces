-- Extract: IBM Maximo CMMS (Austin) -> Equipment Qualification Status / equipment
-- Source: austin_systems.ibm_maximo (SoftwareServer::AUS-SYS-029::SN-CMM-AU-20190401)
-- Target: coco_data_hub.equipment_qualification_status.equipment
-- asset; site AUSTIN mapped to plant US10; Maximo status mapped to in service / out of service / retired.
SELECT
  a.assetnum::varchar(40) AS equipment_identifier,
  a.description::varchar(120) AS equipment_name,
  initcap(lower(a.assettype))::varchar(60) AS equipment_type,
  (CASE a.siteid WHEN 'AUSTIN' THEN 'US10' ELSE a.siteid END)::varchar(20) AS site_code,
  (CASE WHEN a.status IN ('OPERATING', 'ACTIVE') THEN 'in service'
        WHEN a.status = 'DECOMMISSIONED' THEN 'retired' ELSE 'out of service' END)::varchar(20) AS equipment_current_status
FROM ibm_maximo.asset a
