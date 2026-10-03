-- Subscription: aus_opentext_edi__worker_qualifications - OpenText Trading Grid EDI (Austin) receives Worker Qualifications
-- Destination: austin_systems.opentext_edi (SoftwareServer::AUS-SYS-015::SN-EDI-AU-20190620)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (certificated signatory)
-- Keeps the dangerous goods qualifications of Austin workers in the NEW tg_xref_signatory cross-reference, which the
-- IFTDGN map uses to check that the declaring signatory holds a current certificate. Other qualifications and Coco
-- workers are discarded.

UPDATE incoming_worker_qualification i SET discard_reason = 'other estate: not an Austin worker'
 WHERE i.worker_pseudonym_identifier NOT LIKE 'WP-%';
UPDATE incoming_worker_qualification i SET discard_reason = 'not a dangerous goods qualification'
 WHERE i.discard_reason IS NULL AND i.competency_code NOT IN ('CMP-DG-SHIP', 'DG-AIR', 'DG-ROAD');
INSERT INTO opentext_edi.tg_xref_signatory
       (signatory_ref, competency_code, certificate_number, valid_from, valid_to, status)
SELECT i.worker_pseudonym_identifier, i.competency_code, i.certificate_identifier, i.qualification_start_date,
       i.qualification_expiry_date, i.qualification_current_status
  FROM incoming_worker_qualification i
 WHERE i.discard_reason IS NULL
ON CONFLICT (signatory_ref, competency_code) DO UPDATE SET
       certificate_number = EXCLUDED.certificate_number, valid_from = EXCLUDED.valid_from,
       valid_to = EXCLUDED.valid_to, status = EXCLUDED.status;
