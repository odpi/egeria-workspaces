-- Subscription: buc_opcenter_mes__worker_qualifications - Siemens Opcenter MES (Bucharest) receives Worker Qualifications
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority)
-- Keeps the qualifications of this MES's employees (employeenumber = Workday employee ID, matched through the EKG
-- pseudonym rule) in the new table employeecertification, checked when a step is performed or e-signed.  Workers who
-- are not MES employees are discarded: today they are all Coco or Austin workers (EKG is not yet integrated), because
-- EKG's own training records are not yet in the product.
UPDATE incoming_worker_qualification i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker_qualification i SET discard_reason = 'not an EKG MES employee'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.employee e
                    WHERE 'WP-' || upper(substr(md5('EKG:' || e.employeenumber), 1, 12)) = i.worker_pseudonym_identifier);

INSERT INTO opcenter_mes.employeecertification (employeeid, certificationname, description, effectivedate, expirationdate,
                                                certstatus, trainingrecordref, rolename, lastchangedate)
SELECT e.employeeid, i.competency_code, left(i.competency_name, 120), i.qualification_start_date, i.qualification_expiry_date,
       coalesce(i.qualification_current_status, 'qualified'), coalesce(i.training_completion_identifier, i.certificate_identifier),
       i.role_code, now()
  FROM incoming_worker_qualification i
  JOIN opcenter_mes.employee e ON 'WP-' || upper(substr(md5('EKG:' || e.employeenumber), 1, 12)) = i.worker_pseudonym_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (employeeid, certificationname) DO UPDATE
   SET description = EXCLUDED.description, effectivedate = EXCLUDED.effectivedate, expirationdate = EXCLUDED.expirationdate,
       certstatus = EXCLUDED.certstatus, trainingrecordref = EXCLUDED.trainingrecordref, rolename = EXCLUDED.rolename,
       lastchangedate = now()
 WHERE (opcenter_mes.employeecertification.description, opcenter_mes.employeecertification.effectivedate,
        opcenter_mes.employeecertification.expirationdate, opcenter_mes.employeecertification.certstatus,
        opcenter_mes.employeecertification.trainingrecordref, opcenter_mes.employeecertification.rolename)
       IS DISTINCT FROM (EXCLUDED.description, EXCLUDED.effectivedate, EXCLUDED.expirationdate, EXCLUDED.certstatus,
                         EXCLUDED.trainingrecordref, EXCLUDED.rolename);
