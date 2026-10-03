-- Extract: Trackwise Digital (Bucharest) -> Deviations And CAPAs / investigation
-- Source: bucharest_systems.trackwise (SoftwareServer::SYS-005::Trackwise Digital)
-- Target: coco_data_hub.deviations_and_capas.investigation
-- Complete investigations of Trackwise-originated events; investigator = SSO federation identifier (AD login).
SELECT
  e.name::varchar(40) AS deviation_identifier,
  u.federationidentifier::varchar(40) AS deviation_investigator_identifier,
  i.cmpl123qms__completed_date__c AS deviation_investigation_completed_date,
  i.cmpl123qms__root_cause__c AS deviation_root_cause_description,
  i.cmpl123qms__impact_assessment__c AS deviation_impact_description,
  lower(i.cmpl123qms__disposition__c)::varchar(40) AS deviation_disposition_status
FROM trackwise.cmpl123qms__investigation__c i
JOIN trackwise.cmpl123qms__quality_event__c e ON e.sfid = i.cmpl123qms__quality_event__c
JOIN trackwise.users u ON u.sfid = i.cmpl123qms__investigator__c
WHERE NOT i.isdeleted AND i.cmpl123qms__status__c = 'Complete' AND e.cmpl123qms__origin_system__c = 'Trackwise'
