-- Extract: Veeva Vault QMS (Bucharest) -> Deviations And CAPAs / investigation
-- Source: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Target: coco_data_hub.deviations_and_capas.investigation
-- Completed investigation__qdm joined to its quality event and investigator; investigator = the Vault user's federated
-- id (AD login).
SELECT
  q.name__v::varchar(40) AS deviation_identifier,
  u.federated_id__sys::varchar(40) AS deviation_investigator_identifier,
  i.completed_date__c AS deviation_investigation_completed_date,
  i.root_cause__c AS deviation_root_cause_description,
  i.impact_assessment__c AS deviation_impact_description,
  (CASE i.disposition__c WHEN 'no_impact__c' THEN 'no impact' WHEN 'rework__c' THEN 'rework' WHEN 'reject__c' THEN 'reject'
        ELSE 'release with justification' END)::varchar(40) AS deviation_disposition_status
FROM veeva_qms.investigation__qdm i
JOIN veeva_qms.quality_event__qdm q ON q.id = i.quality_event__c
JOIN veeva_qms.user__sys u ON u.id = i.investigator__c
WHERE i.state__v = 'complete_state__c'
