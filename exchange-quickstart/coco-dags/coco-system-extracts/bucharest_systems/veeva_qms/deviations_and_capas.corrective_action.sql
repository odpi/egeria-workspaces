-- Extract: Veeva Vault QMS (Bucharest) -> Deviations And CAPAs / corrective_action
-- Source: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Target: coco_data_hub.deviations_and_capas.corrective_action
-- capa_action__qdm joined to its quality event and owner (AD login); lifecycle states translated.
SELECT
  c.name__v::varchar(40) AS corrective_action_identifier,
  q.name__v::varchar(40) AS deviation_identifier,
  replace(c.action_type__c, '__c', '')::varchar(20) AS corrective_action_type,
  c.description__c AS corrective_action_description,
  u.federated_id__sys::varchar(40) AS corrective_action_owner_identifier,
  c.due_date__c AS corrective_action_due_date,
  (CASE c.state__v WHEN 'open_state__c' THEN 'open' WHEN 'complete_state__c' THEN 'complete' ELSE 'verified' END)::varchar(20) AS corrective_action_current_status
FROM veeva_qms.capa_action__qdm c
JOIN veeva_qms.quality_event__qdm q ON q.id = c.quality_event__c
JOIN veeva_qms.user__sys u ON u.id = c.owner__c
