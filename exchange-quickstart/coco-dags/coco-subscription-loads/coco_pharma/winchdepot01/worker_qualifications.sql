-- Subscription: coco_winchdepot01__worker_qualifications - Winchester Depot Management System (Coco core) receives Worker Qualifications
-- Destination: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (certificated signatory)
-- Keeps the air and road dangerous goods certificates (DG-AIR as AIR, DG-ROAD as ROAD) of the depot's signatories
-- - the workers who sign Winchester consignments (dg_consign.signed_by) - in dg_signatory (NEW), against which a
-- consignment's certificate is checked.  Discards other qualifications, workers who do not sign Winchester
-- consignments, and Austin/EKG workers.

UPDATE incoming_worker_qualification SET discard_reason = 'Austin or EKG worker' WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker_qualification q SET discard_reason = 'not a Winchester dangerous goods signatory'
 WHERE q.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM winchdepot01.dg_consign c WHERE c.signed_by = q.worker_pseudonym_identifier);
UPDATE incoming_worker_qualification SET discard_reason = 'not a dangerous goods certificate'
 WHERE discard_reason IS NULL AND (competency_code NOT IN ('DG-AIR', 'DG-ROAD') OR certificate_identifier IS NULL);

INSERT INTO winchdepot01.dg_signatory (worker_ref, dg_mode, dg_cert, cert_from, cert_to, cert_sts)
SELECT q.worker_pseudonym_identifier, (CASE q.competency_code WHEN 'DG-AIR' THEN 'AIR' ELSE 'ROAD' END), q.certificate_identifier,
       q.qualification_start_date, q.qualification_expiry_date, upper(q.qualification_current_status)
  FROM incoming_worker_qualification q
 WHERE q.discard_reason IS NULL
ON CONFLICT (worker_ref, dg_mode) DO UPDATE SET dg_cert = EXCLUDED.dg_cert, cert_from = EXCLUDED.cert_from, cert_to = EXCLUDED.cert_to,
       cert_sts = EXCLUDED.cert_sts;
