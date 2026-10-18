-- Subscription: buc_veeva_rim__pharmacovigilance_cases - Veeva Vault RIM (Bucharest) receives Pharmacovigilance Cases
-- Destination: bucharest_systems.veeva_rim (SoftwareServer::SYS-021::Veeva Vault RIM)
-- Why it subscribes: Regulatory Safety Submissions depends on it (submit report)
-- Keeps safety cases on EKG products (known in RIM's product__v) in the new custom object safety_case__c, from which
-- the regulatory team prepares the expedited submission (submission__v.safety_case_reference__c) by the reporting due
-- date.  Narratives and follow-ups stay in the safety database; other products' cases are discarded (Coco group data -
-- EKG is not yet integrated).  The product has no source yet.
UPDATE incoming_safety_case i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_rim.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_case_narrative n SET discard_reason = 'narratives stay in the safety database'
 WHERE EXISTS (SELECT 1 FROM incoming_safety_case c WHERE c.safety_case_identifier = n.safety_case_identifier AND c.discard_reason IS NULL)
    OR EXISTS (SELECT 1 FROM veeva_rim.safety_case__c s WHERE s.name__v = n.safety_case_identifier);
UPDATE incoming_case_narrative SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_case_follow_up f SET discard_reason = 'follow-ups stay in the safety database'
 WHERE EXISTS (SELECT 1 FROM incoming_safety_case c WHERE c.safety_case_identifier = f.safety_case_identifier AND c.discard_reason IS NULL)
    OR EXISTS (SELECT 1 FROM veeva_rim.safety_case__c s WHERE s.name__v = f.safety_case_identifier);
UPDATE incoming_case_follow_up SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO veeva_rim.safety_case__c (id, name__v, product__v, report_reference__c, received_date__c, seriousness__c,
                                      expectedness__c, causality__c, reporting_due_date__c, case_status__c, modified_date__v)
SELECT left('SC-' || i.safety_case_identifier, 20), i.safety_case_identifier, p.id, i.safety_report_identifier,
       i.safety_case_received_timestamp, i.safety_case_seriousness_code, i.safety_case_expectedness_code,
       i.safety_case_causality_code, i.safety_case_reporting_due_date, i.safety_case_current_status, now()
  FROM incoming_safety_case i JOIN veeva_rim.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE
   SET product__v = EXCLUDED.product__v, report_reference__c = EXCLUDED.report_reference__c,
       received_date__c = EXCLUDED.received_date__c, seriousness__c = EXCLUDED.seriousness__c,
       expectedness__c = EXCLUDED.expectedness__c, causality__c = EXCLUDED.causality__c,
       reporting_due_date__c = EXCLUDED.reporting_due_date__c, case_status__c = EXCLUDED.case_status__c, modified_date__v = now()
 WHERE (veeva_rim.safety_case__c.product__v, veeva_rim.safety_case__c.report_reference__c, veeva_rim.safety_case__c.received_date__c,
        veeva_rim.safety_case__c.seriousness__c, veeva_rim.safety_case__c.expectedness__c, veeva_rim.safety_case__c.causality__c,
        veeva_rim.safety_case__c.reporting_due_date__c, veeva_rim.safety_case__c.case_status__c)
       IS DISTINCT FROM (EXCLUDED.product__v, EXCLUDED.report_reference__c, EXCLUDED.received_date__c, EXCLUDED.seriousness__c,
                         EXCLUDED.expectedness__c, EXCLUDED.causality__c, EXCLUDED.reporting_due_date__c, EXCLUDED.case_status__c);
