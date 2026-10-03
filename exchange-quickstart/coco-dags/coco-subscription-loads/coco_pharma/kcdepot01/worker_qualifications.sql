-- Subscription: coco_kcdepot01__worker_qualifications - Kansas City Depot Management System (Coco core) receives Worker Qualifications
-- Destination: coco_pharma.kcdepot01 (System::KCDEPOT01)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (certificated signatory)
-- Keeps the road dangerous goods qualification (DG-ROAD, the 49 CFR hazmat certificate) of the employees who may
-- sign shipping papers: hazmat_employee.hm_cert_nbr and hm_cert_exp (NEW column) are refreshed from it, matched on
-- the HRIM pseudonym (the consignment extract reads the certificate from the shipment).  Discards other
-- qualifications (only the DOT certificate is recorded), workers who are not registered hazmat employees here,
-- and Austin/EKG workers.

UPDATE incoming_worker_qualification SET discard_reason = 'Austin or EKG worker' WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker_qualification q SET discard_reason = 'not a registered hazmat employee at Kansas City'
 WHERE q.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM kcdepot01.hazmat_employee e WHERE e.worker_ref = q.worker_pseudonym_identifier);
UPDATE incoming_worker_qualification SET discard_reason = 'not the DOT (49 CFR) road hazmat certificate'
 WHERE discard_reason IS NULL AND (competency_code <> 'DG-ROAD' OR certificate_identifier IS NULL);

UPDATE kcdepot01.hazmat_employee e SET hm_cert_nbr = q.certificate_identifier, hm_cert_exp = q.qualification_expiry_date
  FROM incoming_worker_qualification q
 WHERE q.discard_reason IS NULL AND q.worker_pseudonym_identifier = e.worker_ref
   AND (e.hm_cert_nbr, e.hm_cert_exp) IS DISTINCT FROM (q.certificate_identifier, q.qualification_expiry_date);
