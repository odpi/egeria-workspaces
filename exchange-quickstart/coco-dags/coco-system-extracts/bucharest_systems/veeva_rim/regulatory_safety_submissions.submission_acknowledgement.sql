-- Extract: Veeva Vault RIM (Bucharest) -> Regulatory Safety Submissions / submission_acknowledgement
-- Source: bucharest_systems.veeva_rim (SoftwareServer::SYS-021::Veeva Vault RIM)
-- Target: coco_data_hub.regulatory_safety_submissions.submission_acknowledgement
-- submission_acknowledgement__c joined to its submission; status API names to words.
SELECT
  a.acknowledgement_reference__c::varchar(60) AS submission_acknowledgement_identifier,
  s.name__v::varchar(40) AS submission_identifier,
  a.received_date__c AS submission_acknowledged_timestamp,
  replace(a.ack_status__c, '__c', '')::varchar(20) AS submission_acknowledgement_status
FROM veeva_rim.submission_acknowledgement__c a
JOIN veeva_rim.submission__v s ON s.id = a.submission__v
