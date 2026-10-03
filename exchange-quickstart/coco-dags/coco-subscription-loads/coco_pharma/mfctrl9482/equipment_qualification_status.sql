-- Subscription: coco_mfctrl9482__equipment_qualification_status - Austin Manufacturing Control System (Coco core) receives Equipment Qualification Status
-- Destination: coco_pharma.mfctrl9482 (System::MFCTRL9482)
-- Why it subscribes: Batch Execution Records depends on it (qualification status)
-- Keeps the Austin site's equipment (US10- numbers from Austin's maintenance system, and any AUS- tags of its
-- own) with its qualification and calibration status in mfc_equipment_qual (NEW): the shared Coco batches run
-- on this equipment.  Discards EKG's equipment (RO10), which is another estate's site.

UPDATE incoming_equipment SET discard_reason = 'not Austin site equipment'
 WHERE equipment_identifier NOT LIKE 'US10-%' AND equipment_identifier NOT LIKE 'AUS-%';
UPDATE incoming_qualification_status SET discard_reason = 'not Austin site equipment'
 WHERE equipment_identifier NOT LIKE 'US10-%' AND equipment_identifier NOT LIKE 'AUS-%';
UPDATE incoming_qualification_status q SET discard_reason = 'equipment not in the Austin site register'
 WHERE q.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM incoming_equipment e WHERE e.discard_reason IS NULL AND e.equipment_identifier = q.equipment_identifier)
   AND NOT EXISTS (SELECT 1 FROM mfctrl9482.mfc_equipment_qual m WHERE m.equip_id = q.equipment_identifier);

INSERT INTO mfctrl9482.mfc_equipment_qual (equip_id, equip_name, equip_type, site, equip_status)
SELECT e.equipment_identifier, e.equipment_name, e.equipment_type, e.site_code, upper(e.equipment_current_status)
  FROM incoming_equipment e
 WHERE e.discard_reason IS NULL
ON CONFLICT (equip_id) DO UPDATE SET equip_name = EXCLUDED.equip_name, equip_type = EXCLUDED.equip_type, site = EXCLUDED.site,
       equip_status = EXCLUDED.equip_status;

UPDATE mfctrl9482.mfc_equipment_qual m
   SET qual_status = upper(q.equipment_qualified_status), qualified_on = q.equipment_qualified_date,
       requal_due = q.equipment_qualified_end_date, calibrated_on = q.equipment_calibration_date,
       cal_expiry = q.equipment_calibration_end_date
  FROM incoming_qualification_status q
 WHERE q.discard_reason IS NULL AND q.equipment_identifier = m.equip_id;
