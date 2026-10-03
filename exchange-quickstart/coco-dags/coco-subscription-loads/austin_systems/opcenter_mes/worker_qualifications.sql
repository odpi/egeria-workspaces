-- Subscription: aus_opcenter_mes__worker_qualifications - Siemens Opcenter MES (Austin) receives Worker Qualifications
-- Destination: austin_systems.opcenter_mes (SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601)
-- Why it subscribes: Batch Execution Records depends on it (operator qualification)
-- Keeps the qualifications of Austin workers who are MES users (employee number = the Workday employee ID behind the
-- pseudonym) as employee certifications in the NEW employeecertification table, which Opcenter checks before letting
-- an operator perform or sign a step. Coco (CW-) workers and Austin staff who are not MES users are discarded.

UPDATE incoming_worker_qualification i SET discard_reason = 'other estate: not an Austin worker'
 WHERE i.worker_pseudonym_identifier NOT LIKE 'WP-%';
UPDATE incoming_worker_qualification i SET discard_reason = 'not an Opcenter MES user'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.employee e WHERE 'WP-' || upper(substr(md5('AUS:' || e.employeenumber), 1, 12)) = i.worker_pseudonym_identifier);
INSERT INTO opcenter_mes.employeecertification
       (employeeid, certificationname, certificationdescription, effectivedate, expirydate, certificationstatus,
        trainingrecord, certificatenumber, rolename)
SELECT e.employeeid, i.competency_code, i.competency_name, i.qualification_start_date, i.qualification_expiry_date,
       i.qualification_current_status, i.training_completion_identifier, i.certificate_identifier, i.role_code
  FROM incoming_worker_qualification i
  JOIN opcenter_mes.employee e ON 'WP-' || upper(substr(md5('AUS:' || e.employeenumber), 1, 12)) = i.worker_pseudonym_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (employeeid, certificationname) DO UPDATE SET
       certificationdescription = EXCLUDED.certificationdescription, effectivedate = EXCLUDED.effectivedate,
       expirydate = EXCLUDED.expirydate, certificationstatus = EXCLUDED.certificationstatus,
       trainingrecord = EXCLUDED.trainingrecord, certificatenumber = EXCLUDED.certificatenumber,
       rolename = EXCLUDED.rolename;
