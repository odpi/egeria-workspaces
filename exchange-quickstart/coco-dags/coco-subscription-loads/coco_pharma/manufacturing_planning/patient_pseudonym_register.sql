-- Subscription: coco_manufacturing_planning__patient_pseudonym_register - Global Manufacturing Planning (Coco core) receives Patient Pseudonym Register
-- Destination: coco_pharma.manufacturing_planning (System::manufacturing-planning)
-- Why it subscribes: Personalised Manufacturing Schedule depends on it (identified manufacturing instruction)
-- Keeps the pseudonym links of Coco's personalised orders (globalCRM SO- orders) in pers_psn_reg (NEW), from which
-- the planner creates the PERS planned order and its plnord_pers row.  Discards administration records - they
-- come after manufacture and are not a planning event - and Austin/EKG patients' links (TO- and numeric orders),
-- whose therapies are planned in the acquired estates.  No system supplies this product yet.

UPDATE incoming_patient_pseudonym_link SET discard_reason = 'Austin or EKG personalised order - planned in the acquired estate'
 WHERE order_identifier NOT LIKE 'SO-%';

INSERT INTO manufacturing_planning.pers_psn_reg (patient_ref, cust_ord_ref, matnr, issued_ts, param_text)
SELECT l.patient_pseudonym_identifier, l.order_identifier, l.product_code, l.patient_pseudonym_issued_timestamp,
       l.patient_parameter_description
  FROM incoming_patient_pseudonym_link l
 WHERE l.discard_reason IS NULL
ON CONFLICT (patient_ref) DO UPDATE SET cust_ord_ref = EXCLUDED.cust_ord_ref, matnr = EXCLUDED.matnr,
       issued_ts = EXCLUDED.issued_ts, param_text = EXCLUDED.param_text;

UPDATE incoming_administration_record SET discard_reason = 'administration is after manufacture - not a planning event';
