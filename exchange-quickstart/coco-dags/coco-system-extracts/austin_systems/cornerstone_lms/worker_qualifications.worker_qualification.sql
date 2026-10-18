-- Extract: Cornerstone OnDemand LMS (Austin) -> Worker Qualifications / worker_qualification
-- Source: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Target: coco_data_hub.worker_qualifications.worker_qualification
-- certification_user joined to competency; Active/Expiring/Expired mapped to current/lapsing/lapsed.
SELECT
  ('WP-' || upper(substr(md5('AUS:' || q.user_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  q.competency_id::varchar(40) AS competency_code,
  c.title::varchar(120) AS competency_name,
  q.acquired_dt AS qualification_start_date,
  q.expiration_dt AS qualification_expiry_date,
  (CASE q.cert_status WHEN 'Active' THEN 'current' WHEN 'Expiring' THEN 'lapsing' ELSE 'lapsed' END)::varchar(20) AS qualification_current_status,
  q.evidence_reg_num::varchar(40) AS training_completion_identifier,
  q.certification_number::varchar(40) AS certificate_identifier,
  q.position_ou_id::varchar(40) AS role_code
FROM cornerstone_lms.certification_user q
JOIN cornerstone_lms.competency c ON c.competency_id = q.competency_id
