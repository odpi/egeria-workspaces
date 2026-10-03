-- Subscription: coco_mfctrl9482__personalised_manufacturing_schedule - Austin Manufacturing Control System (Coco core) receives Personalised Manufacturing Schedule
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Electronic Batch Records depends on it (open batch)
-- Keeps nothing: Coco's only personalised therapy (Cocolecel) is made at Winchester, and the personalised
-- batches made at the Austin site are Austin's own cell therapy (AU-7710), not shared Coco batches, so they are
-- not recorded in MFCTRL9482; EKG's slots are another estate's.  Patient material receipts likewise.

UPDATE incoming_manufacturing_slot SET discard_reason = 'personalised batches are not shared Coco batches - Cocolecel is made at Winchester, AU-7710 is Austin''s own';
UPDATE incoming_patient_material_receipt SET discard_reason = 'personalised batches are not shared Coco batches - Cocolecel is made at Winchester, AU-7710 is Austin''s own';
