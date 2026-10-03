-- Extract: Trackwise Digital (Bucharest) -> Deviations And CAPAs / corrective_action
-- Source: bucharest_systems.trackwise (SoftwareServer::SYS-005::Trackwise Digital)
-- Target: coco_data_hub.deviations_and_capas.corrective_action
-- CAPAs of Trackwise-originated events; owner = SSO federation identifier; 'Closed - Effective' to verified.
SELECT
  c.name::varchar(40) AS corrective_action_identifier,
  e.name::varchar(40) AS deviation_identifier,
  lower(c.cmpl123qms__type__c)::varchar(20) AS corrective_action_type,
  c.cmpl123qms__description__c AS corrective_action_description,
  u.federationidentifier::varchar(40) AS corrective_action_owner_identifier,
  c.cmpl123qms__due_date__c AS corrective_action_due_date,
  (CASE c.cmpl123qms__status__c WHEN 'Open' THEN 'open' WHEN 'Closed - Effective' THEN 'verified' ELSE 'complete' END)::varchar(20) AS corrective_action_current_status
FROM trackwise.cmpl123qms__capa__c c
JOIN trackwise.cmpl123qms__quality_event__c e ON e.sfid = c.cmpl123qms__quality_event__c
JOIN trackwise.users u ON u.sfid = c.ownerid
WHERE NOT c.isdeleted AND e.cmpl123qms__origin_system__c = 'Trackwise'
