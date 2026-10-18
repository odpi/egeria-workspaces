-- Subscription: buc_veeva_qms__safety_signals - Veeva Vault QMS (Bucharest) receives Safety Signals
-- Destination: bucharest_systems.veeva_qms (SoftwareServer::SYS-002::Veeva Vault QMS)
-- Why it subscribes: Deviations And CAPAs depends on it (signal referred to quality)
-- Keeps safety signals on EKG products (known in product__v) that are referred to quality in the new custom object
-- safety_signal__c, from which QA opens a deviation of source safety signal (creating the quality event here would feed
-- back into Deviations And CAPAs).  Signals not referred to quality and exposure estimates are not QMS data; other
-- products' signals are discarded (Coco group data - EKG is not yet integrated).  The product has no source yet.
UPDATE incoming_safety_signal i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_safety_signal SET discard_reason = 'signal not referred to quality'
 WHERE discard_reason IS NULL AND coalesce(signal_referral_type, '') NOT IN ('quality', 'both', 'referred to quality');
UPDATE incoming_exposure_denominator i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_qms.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_exposure_denominator SET discard_reason = 'exposure estimates are not kept in the QMS' WHERE discard_reason IS NULL;

INSERT INTO veeva_qms.safety_signal__c (id, name__v, product__c, detected_date__c, event_term__c, case_count__c, description__c,
                                        signal_status__c, referral__c, modified_date__v)
SELECT left('SIG-' || i.signal_identifier, 20), i.signal_identifier, p.id, i.signal_detected_date, i.adverse_event_code,
       i.signal_contributing_count, i.signal_description, i.signal_current_status, i.signal_referral_type, now()
  FROM incoming_safety_signal i JOIN veeva_qms.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE
   SET product__c = EXCLUDED.product__c, detected_date__c = EXCLUDED.detected_date__c, event_term__c = EXCLUDED.event_term__c,
       case_count__c = EXCLUDED.case_count__c, description__c = EXCLUDED.description__c,
       signal_status__c = EXCLUDED.signal_status__c, referral__c = EXCLUDED.referral__c, modified_date__v = now()
 WHERE (veeva_qms.safety_signal__c.product__c, veeva_qms.safety_signal__c.detected_date__c, veeva_qms.safety_signal__c.event_term__c,
        veeva_qms.safety_signal__c.case_count__c, veeva_qms.safety_signal__c.description__c,
        veeva_qms.safety_signal__c.signal_status__c, veeva_qms.safety_signal__c.referral__c)
       IS DISTINCT FROM (EXCLUDED.product__c, EXCLUDED.detected_date__c, EXCLUDED.event_term__c, EXCLUDED.case_count__c,
                         EXCLUDED.description__c, EXCLUDED.signal_status__c, EXCLUDED.referral__c);
