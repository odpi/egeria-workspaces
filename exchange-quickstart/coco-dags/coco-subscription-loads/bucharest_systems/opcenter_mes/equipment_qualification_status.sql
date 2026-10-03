-- Subscription: buc_opcenter_mes__equipment_qualification_status - Siemens Opcenter MES (Bucharest) receives Equipment Qualification Status
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Batch Execution Records depends on it (qualification status)
-- Keeps Maximo's status, qualification and calibration of each production resource of this MES (resourcename = Maximo
-- asset number) in the new table resourcequalification, checked when the resource is used.  EKG assets that are not MES
-- resources (laboratory instruments, utilities) are discarded, as are other sites' assets (Coco group data - EKG not
-- yet integrated).
UPDATE incoming_equipment i SET discard_reason = 'not a production resource in the MES'
 WHERE i.equipment_identifier LIKE 'RO10-%'
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.resourcedef r WHERE r.resourcename = i.equipment_identifier);
UPDATE incoming_equipment i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.resourcedef r WHERE r.resourcename = i.equipment_identifier);
UPDATE incoming_qualification_status i SET discard_reason = 'not a production resource in the MES'
 WHERE i.equipment_identifier LIKE 'RO10-%'
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.resourcedef r WHERE r.resourcename = i.equipment_identifier);
UPDATE incoming_qualification_status i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.resourcedef r WHERE r.resourcename = i.equipment_identifier);

INSERT INTO opcenter_mes.resourcequalification (resourceid, equipmentstatus, lastchangedate)
SELECT r.resourceid, i.equipment_current_status, now()
  FROM incoming_equipment i JOIN opcenter_mes.resourcedef r ON r.resourcename = i.equipment_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (resourceid) DO UPDATE
   SET equipmentstatus = EXCLUDED.equipmentstatus, lastchangedate = now()
 WHERE opcenter_mes.resourcequalification.equipmentstatus IS DISTINCT FROM EXCLUDED.equipmentstatus;

INSERT INTO opcenter_mes.resourcequalification (resourceid, qualstatus, qualdate, qualduedate, calibrationdate,
                                                calibrationduedate, lastchangedate)
SELECT r.resourceid, i.equipment_qualified_status, i.equipment_qualified_date, i.equipment_qualified_end_date,
       i.equipment_calibration_date, i.equipment_calibration_end_date, now()
  FROM incoming_qualification_status i JOIN opcenter_mes.resourcedef r ON r.resourcename = i.equipment_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (resourceid) DO UPDATE
   SET qualstatus = EXCLUDED.qualstatus, qualdate = EXCLUDED.qualdate, qualduedate = EXCLUDED.qualduedate,
       calibrationdate = EXCLUDED.calibrationdate, calibrationduedate = EXCLUDED.calibrationduedate, lastchangedate = now()
 WHERE (opcenter_mes.resourcequalification.qualstatus, opcenter_mes.resourcequalification.qualdate,
        opcenter_mes.resourcequalification.qualduedate, opcenter_mes.resourcequalification.calibrationdate,
        opcenter_mes.resourcequalification.calibrationduedate)
       IS DISTINCT FROM (EXCLUDED.qualstatus, EXCLUDED.qualdate, EXCLUDED.qualduedate, EXCLUDED.calibrationdate,
                         EXCLUDED.calibrationduedate);
