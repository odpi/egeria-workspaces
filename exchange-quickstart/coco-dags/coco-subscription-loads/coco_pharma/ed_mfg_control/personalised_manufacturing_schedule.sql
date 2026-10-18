-- Subscription: coco_ed_mfg_control__personalised_manufacturing_schedule - Edmonton Manufacturing Control System (Coco core) receives Personalised Manufacturing Schedule
-- Destination: coco_pharma.ed_mfg_control (System::ed-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (open batch)
-- Keeps nothing: Edmonton makes only standard tablets (Norvasc, Toprol-XL), so no personalised slot is ever
-- scheduled there - Coco's Cocolecel slots are Winchester's and the other slots belong to the Austin and EKG
-- sites.  Patient material receipts are likewise for those sites.

UPDATE incoming_manufacturing_slot SET discard_reason = 'Edmonton makes no personalised therapies';
UPDATE incoming_patient_material_receipt SET discard_reason = 'Edmonton makes no personalised therapies';
