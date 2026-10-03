-- Extract: Veeva Vault QMS (Austin) -> Deviations And CAPAs / corrective_action
-- Source: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Target: coco_data_hub.deviations_and_capas.corrective_action
-- capa_action__qdm joined to its quality event and owner; lifecycle states translated.
SELECT
  c.name__v::varchar(40) AS corrective_action_identifier,
  q.name__v::varchar(40) AS deviation_identifier,
  replace(c.action_type__c, '__c', '')::varchar(20) AS corrective_action_type,
  c.description__c AS corrective_action_description,
  coalesce(split_part(u.username__sys, '@', 1), c.owner__c)::varchar(40) AS corrective_action_owner_identifier,
  c.due_date__c AS corrective_action_due_date,
  (CASE c.state__v WHEN 'open_state__c' THEN 'open' WHEN 'complete_state__c' THEN 'complete' ELSE 'verified' END)::varchar(20) AS corrective_action_current_status
FROM veeva_qms.capa_action__qdm c
JOIN veeva_qms.quality_event__qdm q ON q.id = c.quality_event__c
LEFT JOIN veeva_qms.user__sys u ON u.id = c.owner__c
