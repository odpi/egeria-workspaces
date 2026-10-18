-- Subscription: coco_eddepot01__worker_qualifications - Edmonton Depot Management System (Coco core) receives Worker Qualifications
-- Destination: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (certificated signatory)
-- Keeps the road dangerous goods qualification (DG-ROAD, the TDG certificate) of the depot's registered signers:
-- tdg_signer.tdg_cert_no and cert_expiry are refreshed from it, matched on the HRIM pseudonym (the consignment
-- extract reads the certificate from the shipment, not from tdg_signer).  Discards other qualifications (Edmonton
-- ships by road under TDG only), workers who are not registered TDG signers here, and Austin/EKG workers.

UPDATE incoming_worker_qualification SET discard_reason = 'Austin or EKG worker' WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker_qualification q SET discard_reason = 'not a registered TDG signer at the Edmonton depot'
 WHERE q.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM eddepot01.tdg_signer s WHERE s.worker_ref = q.worker_pseudonym_identifier);
UPDATE incoming_worker_qualification SET discard_reason = 'not a road dangerous goods (TDG) certificate'
 WHERE discard_reason IS NULL AND (competency_code <> 'DG-ROAD' OR certificate_identifier IS NULL);

UPDATE eddepot01.tdg_signer s SET tdg_cert_no = q.certificate_identifier, cert_expiry = q.qualification_expiry_date
  FROM incoming_worker_qualification q
 WHERE q.discard_reason IS NULL AND q.worker_pseudonym_identifier = s.worker_ref
   AND (s.tdg_cert_no, s.cert_expiry) IS DISTINCT FROM (q.certificate_identifier, q.qualification_expiry_date);
