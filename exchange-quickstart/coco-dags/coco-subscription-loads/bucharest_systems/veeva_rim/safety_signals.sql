-- Subscription: buc_veeva_rim__safety_signals - Veeva Vault RIM (Bucharest) receives Safety Signals
-- Destination: bucharest_systems.veeva_rim (SoftwareServer::SYS-021::Veeva Vault RIM)
-- Why it subscribes: Market Authorisations depends on it (label or authorisation change)
-- Keeps safety signals on EKG products (known in RIM's product__v) that are referred to the authorisation register in
-- the new custom object safety_signal__c, from which a label variation is raised (registration__v.related_signal__c
-- is set by the regulatory team, not here, because the market authorisation extract reads it).  Signals not referred
-- to authorisation and exposure estimates are not RIM data; other products' signals are discarded (Coco group data -
-- EKG is not yet integrated).  The product has no source yet.
UPDATE incoming_safety_signal i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_rim.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_safety_signal SET discard_reason = 'signal not referred to the authorisation register'
 WHERE discard_reason IS NULL AND coalesce(signal_referral_type, '') NOT IN ('authorisation', 'both', 'referred to authorisation');
UPDATE incoming_exposure_denominator i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM veeva_rim.product__v p WHERE p.product_code__c = i.product_code);
UPDATE incoming_exposure_denominator SET discard_reason = 'exposure estimates are not kept in RIM' WHERE discard_reason IS NULL;

INSERT INTO veeva_rim.safety_signal__c (id, name__v, product__v, detected_date__c, event_term__c, case_count__c, description__c,
                                        signal_status__c, referral__c, modified_date__v)
SELECT left('SIG-' || i.signal_identifier, 20), i.signal_identifier, p.id, i.signal_detected_date, i.adverse_event_code,
       i.signal_contributing_count, i.signal_description, i.signal_current_status, i.signal_referral_type, now()
  FROM incoming_safety_signal i JOIN veeva_rim.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE
   SET product__v = EXCLUDED.product__v, detected_date__c = EXCLUDED.detected_date__c, event_term__c = EXCLUDED.event_term__c,
       case_count__c = EXCLUDED.case_count__c, description__c = EXCLUDED.description__c,
       signal_status__c = EXCLUDED.signal_status__c, referral__c = EXCLUDED.referral__c, modified_date__v = now()
 WHERE (veeva_rim.safety_signal__c.product__v, veeva_rim.safety_signal__c.detected_date__c, veeva_rim.safety_signal__c.event_term__c,
        veeva_rim.safety_signal__c.case_count__c, veeva_rim.safety_signal__c.description__c,
        veeva_rim.safety_signal__c.signal_status__c, veeva_rim.safety_signal__c.referral__c)
       IS DISTINCT FROM (EXCLUDED.product__v, EXCLUDED.detected_date__c, EXCLUDED.event_term__c, EXCLUDED.case_count__c,
                         EXCLUDED.description__c, EXCLUDED.signal_status__c, EXCLUDED.referral__c);
