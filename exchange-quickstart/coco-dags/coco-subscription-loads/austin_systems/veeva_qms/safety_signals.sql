-- Subscription: aus_veeva_qms__safety_signals - Veeva Vault QMS (Austin) receives Safety Signals
-- Destination: austin_systems.veeva_qms (SoftwareServer::AUS-SYS-025::SN-QMS-AU-20190901)
-- Why it subscribes: Deviations And CAPAs depends on it (signal referred to quality)
-- Keeps the safety signals on products made at Austin as NEW signal_referral__c records, from which the quality
-- owner decides whether a quality event (deviation) is needed; quality_event__qdm is not written here. Exposure
-- denominators and signals on other products are discarded.

UPDATE incoming_safety_signal i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
INSERT INTO veeva_qms.signal_referral__c
       (id, name__v, detected_date__c, product__c, adverse_event_code__c, case_count__c, description__c,
        signal_status__c, referral_type__c)
SELECT ('0SG' || upper(substr(md5(i.signal_identifier), 1, 11))), i.signal_identifier, i.signal_detected_date, p.id, i.adverse_event_code,
       i.signal_contributing_count, i.signal_description, i.signal_current_status, i.signal_referral_type
  FROM incoming_safety_signal i
  LEFT JOIN veeva_qms.product__v p ON p.product_code__c = i.product_code
 WHERE i.discard_reason IS NULL
ON CONFLICT (id) DO UPDATE SET
       name__v = EXCLUDED.name__v, detected_date__c = EXCLUDED.detected_date__c, product__c = EXCLUDED.product__c,
       adverse_event_code__c = EXCLUDED.adverse_event_code__c, case_count__c = EXCLUDED.case_count__c,
       description__c = EXCLUDED.description__c, signal_status__c = EXCLUDED.signal_status__c,
       referral_type__c = EXCLUDED.referral_type__c;

UPDATE incoming_exposure_denominator SET discard_reason = 'exposure denominators not used by QMS';
