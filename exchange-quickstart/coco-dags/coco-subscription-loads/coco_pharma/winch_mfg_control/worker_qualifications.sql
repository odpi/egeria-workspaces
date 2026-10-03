-- Subscription: coco_winch_mfg_control__worker_qualifications - Winchester Manufacturing Control System (Coco core) receives Worker Qualifications
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Batch Execution Records (operator qualification) and Electronic Batch Records (signature authority) depend on it
-- Keeps the qualifications of the people who sign Winchester batch records - operators and QPs known from wstep
-- and wrel - in wopr_qual (NEW), checked before a step or certification is signed.  Discards other workers'
-- qualifications (other factories, depots, clinical records) and Austin/EKG workers.

UPDATE incoming_worker_qualification SET discard_reason = 'Austin or EKG worker' WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker_qualification q SET discard_reason = 'does not sign Winchester batch records'
 WHERE q.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM winch_mfg_control.wstep s WHERE s.opr_psn = q.worker_pseudonym_identifier)
   AND NOT EXISTS (SELECT 1 FROM winch_mfg_control.wrel r WHERE r.qp_psn = q.worker_pseudonym_identifier);

INSERT INTO winch_mfg_control.wopr_qual (psn_ref, comp_cd, comp_nm, start_dt, exp_dt, qual_sts, trn_ref, cert_no, role_cd)
SELECT q.worker_pseudonym_identifier, q.competency_code, q.competency_name, q.qualification_start_date, q.qualification_expiry_date,
       q.qualification_current_status, q.training_completion_identifier, q.certificate_identifier, q.role_code
  FROM incoming_worker_qualification q
 WHERE q.discard_reason IS NULL
ON CONFLICT (psn_ref, comp_cd) DO UPDATE SET comp_nm = EXCLUDED.comp_nm, start_dt = EXCLUDED.start_dt, exp_dt = EXCLUDED.exp_dt,
       qual_sts = EXCLUDED.qual_sts, trn_ref = EXCLUDED.trn_ref, cert_no = EXCLUDED.cert_no, role_cd = EXCLUDED.role_cd;
