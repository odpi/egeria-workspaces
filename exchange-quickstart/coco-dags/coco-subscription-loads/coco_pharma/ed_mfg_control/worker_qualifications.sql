-- Subscription: coco_ed_mfg_control__worker_qualifications - Edmonton Manufacturing Control System (Coco core) receives Worker Qualifications
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Batch Execution Records (operator qualification) and Electronic Batch Records (signature authority) depend on it
-- Keeps the qualifications of Edmonton's registered operators (operator, matched on the HRIM pseudonym) in
-- operator_qualification (NEW, keyed by employee number), and sets operator.active from the electronic signature
-- competency EBR-SIG - Y while current or lapsing, N once lapsed - which is the signature authority the EBR
-- relies on.  Discards workers who are not Edmonton operators and Austin/EKG workers.

UPDATE incoming_worker_qualification SET discard_reason = 'Austin or EKG worker' WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker_qualification q SET discard_reason = 'not an Edmonton operator'
 WHERE q.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM ed_mfg_control.operator o WHERE o.worker_ref = q.worker_pseudonym_identifier);

INSERT INTO ed_mfg_control.operator_qualification (emp_no, competency, competency_name, qualified_on, expires_on, qual_status,
       training_ref, certificate_no)
SELECT o.emp_no, q.competency_code, q.competency_name, q.qualification_start_date, q.qualification_expiry_date,
       q.qualification_current_status, q.training_completion_identifier, q.certificate_identifier
  FROM incoming_worker_qualification q
  JOIN ed_mfg_control.operator o ON o.worker_ref = q.worker_pseudonym_identifier
 WHERE q.discard_reason IS NULL
ON CONFLICT (emp_no, competency) DO UPDATE SET competency_name = EXCLUDED.competency_name, qualified_on = EXCLUDED.qualified_on,
       expires_on = EXCLUDED.expires_on, qual_status = EXCLUDED.qual_status, training_ref = EXCLUDED.training_ref,
       certificate_no = EXCLUDED.certificate_no;

UPDATE ed_mfg_control.operator o
   SET active = (CASE WHEN q.qualification_current_status = 'lapsed' THEN 'N' ELSE 'Y' END)
  FROM incoming_worker_qualification q
 WHERE q.discard_reason IS NULL AND q.competency_code = 'EBR-SIG' AND q.worker_pseudonym_identifier = o.worker_ref
   AND o.active IS DISTINCT FROM (CASE WHEN q.qualification_current_status = 'lapsed' THEN 'N' ELSE 'Y' END);
