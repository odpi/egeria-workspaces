-- Extract: Cornerstone OnDemand LMS (Austin) -> Role Competency Requirements / role_competency_requirement
-- Source: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Target: coco_data_hub.role_competency_requirements.role_competency_requirement
-- ou_competency_requirement joined to competency; regulatory flag Y/N to boolean.
SELECT
  r.ou_id::varchar(40) AS role_code,
  r.competency_id::varchar(40) AS competency_code,
  c.title::varchar(120) AS competency_name,
  c.description AS competency_description,
  c.refresh_interval_months AS competency_refresh_duration,
  (c.regulatory_flag = 'Y') AS competency_regulated_flag,
  r.effective_date AS role_requirement_start_date
FROM cornerstone_lms.ou_competency_requirement r
JOIN cornerstone_lms.competency c ON c.competency_id = r.competency_id
WHERE r.required = 'Y'
