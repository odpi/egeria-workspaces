-- Subscription: coco_winch_mfg_control__personalised_manufacturing_schedule - Winchester Manufacturing Control System (Coco core) receives Personalised Manufacturing Schedule
-- Destination: coco_pharma.winch_mfg_control (System::winch-mfg-control)
-- Why it subscribes: Electronic Batch Records depends on it (open batch)
-- Keeps the personalised manufacturing slots Global Manufacturing Planning schedules at Winchester (Cocolecel,
-- product 9100, W- batch numbers) in wsched (NEW); the wbatch header is opened from the slot when manufacture
-- starts, so wbatch is not written from the plan.  Discards Austin's and EKG's personalised schedules (AU-7710,
-- PF-9101), which are made and recorded at their own sites.  Patient material receipts are discarded: they are
-- booked in by planning and the cell suite, not by the control system.

UPDATE incoming_manufacturing_slot s SET discard_reason = 'not a Winchester personalised batch - made at the acquired estate''s own site'
 WHERE NOT (EXISTS (SELECT 1 FROM winch_mfg_control.wbatch b WHERE b.batch_no = s.batch_identifier) OR s.batch_identifier ~ '^W[0-9]{2}-');

INSERT INTO winch_mfg_control.wsched (batch_no, cust_ord, psn_ref, prd_cd, slot_st, slot_en, pt_params, slot_sts)
SELECT s.batch_identifier, s.order_identifier, s.patient_pseudonym_identifier, s.product_code, s.slot_start_timestamp,
       s.slot_end_timestamp, s.patient_parameter_description, s.slot_status
  FROM incoming_manufacturing_slot s
 WHERE s.discard_reason IS NULL
ON CONFLICT (batch_no) DO UPDATE SET cust_ord = EXCLUDED.cust_ord, psn_ref = EXCLUDED.psn_ref, prd_cd = EXCLUDED.prd_cd,
       slot_st = EXCLUDED.slot_st, slot_en = EXCLUDED.slot_en, pt_params = EXCLUDED.pt_params, slot_sts = EXCLUDED.slot_sts;

UPDATE incoming_patient_material_receipt SET discard_reason = 'patient material is booked in by planning and the cell suite, not the control system';
