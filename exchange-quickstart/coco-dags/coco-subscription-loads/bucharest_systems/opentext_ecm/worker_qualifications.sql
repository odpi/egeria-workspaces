-- Subscription: buc_opentext_ecm__worker_qualifications - OpenText ECM (Bucharest) receives Worker Qualifications
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Electronic Batch Records depends on it (signature authority)
-- The ECM has no worker identifiers it can match a pseudonym to (only Content Server logins), and training records are
-- not archived here, so nothing is written.  Coco workers are discarded as Coco group data (EKG is not yet integrated);
-- the rest as unresolvable.
UPDATE incoming_worker_qualification SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker_qualification
   SET discard_reason = 'ECM cannot resolve worker pseudonyms - training records are not archived here'
 WHERE discard_reason IS NULL;
