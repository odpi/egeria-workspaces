-- Extract: Maximo Asset Management (Bucharest) -> Equipment Qualification Status / equipment
-- Source: bucharest_systems.maximo (SoftwareServer::SYS-016::Maximo Asset Management)
-- Target: coco_data_hub.equipment_qualification_status.equipment
-- asset; site BUCURESTI mapped to plant RO10; asset type title-cased; Maximo status mapped to in service / out of
-- service / retired.
SELECT
  a.assetnum::varchar(40) AS equipment_identifier,
  a.description::varchar(120) AS equipment_name,
  initcap(lower(a.assettype))::varchar(60) AS equipment_type,
  (CASE a.siteid WHEN 'BUCURESTI' THEN 'RO10' ELSE a.siteid END)::varchar(20) AS site_code,
  (CASE WHEN a.status IN ('OPERATING', 'ACTIVE') THEN 'in service'
        WHEN a.status = 'DECOMMISSIONED' THEN 'retired' ELSE 'out of service' END)::varchar(20) AS equipment_current_status
FROM maximo.asset a
