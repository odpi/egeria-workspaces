-- Subscription: buc_trackwise__safety_signals - Trackwise Digital (Bucharest) receives Safety Signals
-- Destination: bucharest_systems.trackwise (SoftwareServer::SYS-005::Trackwise Digital)
-- Why it subscribes: Deviations And CAPAs depends on it (signal referred to quality)
-- Safety signals referred to quality become deviations of source safety signal in Veeva QMS, not Trackwise events, so
-- signals on EKG products (PF- product codes, as in Trackwise's quality events) are discarded for that reason and other
-- companies' as Coco group data (EKG is not yet integrated).  Nothing is written.  The product has no source yet.
UPDATE incoming_safety_signal SET discard_reason = 'signals referred to quality are raised in Veeva QMS, not Trackwise'
 WHERE product_code LIKE 'PF-%';
UPDATE incoming_safety_signal SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
UPDATE incoming_exposure_denominator SET discard_reason = 'exposure estimates are not kept in Trackwise'
 WHERE product_code LIKE 'PF-%';
UPDATE incoming_exposure_denominator SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;
