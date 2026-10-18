-- Extract: Human Resources Information Manager (HRIM) (Coco core) -> Role Competency Requirements / role_competency_requirement
-- Source: coco_pharma.coco_hrim (System::coco-hrim)
-- Target: coco_data_hub.role_competency_requirements.role_competency_requirement
-- job_competency joined to competency; Y/N regulated flag to boolean.
SELECT
  r.job_code::varchar(40)          AS role_code,
  r.comp_cd::varchar(40)           AS competency_code,
  c.comp_name::varchar(120)        AS competency_name,
  c.comp_desc                      AS competency_description,
  c.refresh_mths::integer          AS competency_refresh_duration,
  (c.regulated_yn = 'Y')           AS competency_regulated_flag,
  r.eff_date                       AS role_requirement_start_date
FROM coco_hrim.job_competency r
JOIN coco_hrim.competency c ON c.comp_cd = r.comp_cd
