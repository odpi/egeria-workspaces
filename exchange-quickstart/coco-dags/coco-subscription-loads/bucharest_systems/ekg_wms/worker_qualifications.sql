-- Subscription: buc_ekg_wms__worker_qualifications - Warehouse Management System (WMS) (Bucharest) receives Worker Qualifications
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (certificated signatory)
-- The WMS has no worker identifiers it can match a pseudonym to (operators are logins), and the ADR 1.3 certificate of
-- the signatory is recorded on each despatch (expeditii.nr_cert_semnatar), so nothing is written.  Coco workers are
-- discarded as Coco group data (EKG is not yet integrated); the rest as unresolvable.
UPDATE incoming_worker_qualification SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker_qualification
   SET discard_reason = 'WMS cannot resolve worker pseudonyms - the signatory certificate is kept on the despatch'
 WHERE discard_reason IS NULL;
