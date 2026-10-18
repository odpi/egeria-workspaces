-- Subscription: aus_opcenter_mes__equipment_qualification_status - Siemens Opcenter MES (Austin) receives Equipment Qualification Status
-- Destination: austin_systems.opcenter_mes (SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601)
-- Why it subscribes: Batch Execution Records depends on it (qualification status)
-- Keeps the Maximo asset status and the qualification and calibration dates on the resourcedef of each Austin asset
-- that is an MES resource (resource name = Maximo asset number), in NEW columns that the MES checks before a
-- resource is used; resourceusagehistory, which records the status at use, is not rewritten. Laboratory and other
-- assets the MES does not schedule, and EKG's RO10 assets, are discarded.

UPDATE incoming_equipment i SET discard_reason = 'other estate: not an Austin asset'
 WHERE i.site_code NOT LIKE 'US%';
UPDATE incoming_equipment i SET discard_reason = 'not an MES resource'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.resourcedef r WHERE r.resourcename = i.equipment_identifier);
UPDATE opcenter_mes.resourcedef r SET assetstatus = i.equipment_current_status
  FROM incoming_equipment i
 WHERE i.discard_reason IS NULL AND r.resourcename = i.equipment_identifier
   AND r.assetstatus IS DISTINCT FROM i.equipment_current_status;

UPDATE incoming_qualification_status i SET discard_reason = 'other estate: not an Austin asset'
 WHERE i.equipment_identifier !~ '^US[0-9]{2}-';
UPDATE incoming_qualification_status i SET discard_reason = 'not an MES resource'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.resourcedef r WHERE r.resourcename = i.equipment_identifier);
UPDATE opcenter_mes.resourcedef r
   SET qualificationstatus = i.equipment_qualified_status, qualificationdate = i.equipment_qualified_date,
       qualificationexpirydate = i.equipment_qualified_end_date, calibrationdate = i.equipment_calibration_date,
       calibrationduedate = i.equipment_calibration_end_date
  FROM incoming_qualification_status i
 WHERE i.discard_reason IS NULL AND r.resourcename = i.equipment_identifier
   AND (r.qualificationstatus, r.qualificationdate, r.qualificationexpirydate, r.calibrationdate, r.calibrationduedate)
       IS DISTINCT FROM (i.equipment_qualified_status, i.equipment_qualified_date, i.equipment_qualified_end_date,
                         i.equipment_calibration_date, i.equipment_calibration_end_date);
