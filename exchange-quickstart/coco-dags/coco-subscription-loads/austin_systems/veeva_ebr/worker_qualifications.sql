-- Subscription: aus_veeva_ebr__worker_qualifications - Veeva Vault EBR (Austin) receives Worker Qualifications
-- Destination: austin_systems.veeva_ebr (SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301)
-- Why it subscribes: Electronic Batch Records depends on it (signature authority)
-- Keeps the qualifications of Austin workers (WP- pseudonyms; Cornerstone is the only Austin source) as NEW
-- signature_qualification__c records that the signature authority check reads. The vault holds users by Entra UPN
-- and cannot resolve a pseudonym, so it keeps the pseudonym as delivered. Coco (CW-) workers are discarded.

UPDATE incoming_worker_qualification i SET discard_reason = 'other estate: not an Austin worker'
 WHERE i.worker_pseudonym_identifier NOT LIKE 'WP-%';
INSERT INTO veeva_ebr.signature_qualification__c
       (id, worker_pseudonym__c, competency__c, competency_name__c, qualified_from__c, qualified_to__c,
        status__c, training_record__c, certificate__c, role__c)
SELECT ('0SQ' || upper(substr(md5(i.worker_pseudonym_identifier || '|' || i.competency_code), 1, 11))), i.worker_pseudonym_identifier,
       i.competency_code, i.competency_name, i.qualification_start_date, i.qualification_expiry_date,
       i.qualification_current_status, i.training_completion_identifier, i.certificate_identifier, i.role_code
  FROM incoming_worker_qualification i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       worker_pseudonym__c = EXCLUDED.worker_pseudonym__c, competency__c = EXCLUDED.competency__c,
       competency_name__c = EXCLUDED.competency_name__c, qualified_from__c = EXCLUDED.qualified_from__c,
       qualified_to__c = EXCLUDED.qualified_to__c, status__c = EXCLUDED.status__c,
       training_record__c = EXCLUDED.training_record__c, certificate__c = EXCLUDED.certificate__c,
       role__c = EXCLUDED.role__c;
