-- Subscription: aus_oracle_tms__worker_qualifications - Oracle TMS (Austin) receives Worker Qualifications
-- Destination: austin_systems.oracle_tms (SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (certificated signatory)
-- Keeps the dangerous goods (hazmat shipping) qualifications of Austin workers in the NEW dg_signatory_qualification
-- table checked when a declaration is signed; TMS cannot resolve a pseudonym to a login, so it keeps the pseudonym
-- and certificate number as delivered. Other qualifications and Coco workers are discarded.

UPDATE incoming_worker_qualification i SET discard_reason = 'other estate: not an Austin worker'
 WHERE i.worker_pseudonym_identifier NOT LIKE 'WP-%';
UPDATE incoming_worker_qualification i SET discard_reason = 'not a dangerous goods qualification'
 WHERE i.discard_reason IS NULL AND i.competency_code NOT IN ('CMP-DG-SHIP', 'DG-AIR', 'DG-ROAD');
INSERT INTO oracle_tms.dg_signatory_qualification
       (worker_ref, competency_code, certificate_number, valid_from, valid_to, qualification_status, role_code)
SELECT i.worker_pseudonym_identifier, i.competency_code, i.certificate_identifier, i.qualification_start_date,
       i.qualification_expiry_date, i.qualification_current_status, i.role_code
  FROM incoming_worker_qualification i
 WHERE i.discard_reason IS NULL
ON CONFLICT (worker_ref, competency_code) DO UPDATE SET
       certificate_number = EXCLUDED.certificate_number, valid_from = EXCLUDED.valid_from,
       valid_to = EXCLUDED.valid_to, qualification_status = EXCLUDED.qualification_status,
       role_code = EXCLUDED.role_code;
