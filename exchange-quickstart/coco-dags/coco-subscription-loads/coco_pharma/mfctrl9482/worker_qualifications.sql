-- Subscription: coco_mfctrl9482__worker_qualifications - Austin Manufacturing Control System (Coco core) receives Worker Qualifications
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Batch Execution Records (operator qualification) and Electronic Batch Records (signature authority) depend on it
-- Keeps nothing: MFCTRL9482 identifies the Austin site staff who sign by badge, with the site's own AW-
-- pseudonyms (mfc_operator).  Coco workers (CW-) do not sign Austin batch records, and Austin's Workday
-- pseudonyms (WP-) cannot be matched to the badges - the two estates share no worker identifiers.

UPDATE incoming_worker_qualification SET discard_reason = 'Coco worker - does not sign Austin batch records'
 WHERE worker_pseudonym_identifier LIKE 'CW-%';
UPDATE incoming_worker_qualification q SET discard_reason = 'not matched to an Austin site badge (MFCTRL9482 uses AW- pseudonyms)'
 WHERE q.discard_reason IS NULL;
