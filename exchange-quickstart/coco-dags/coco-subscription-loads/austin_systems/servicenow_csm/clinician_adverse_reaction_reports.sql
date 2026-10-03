-- Subscription: aus_servicenow_csm__clinician_adverse_reaction_reports - ServiceNow Customer Service Management (Austin) receives Clinician Adverse Reaction Reports
-- Destination: austin_systems.servicenow_csm (SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601)
-- Why it subscribes: Consolidated Safety Reports depends on it (clinician report)
-- Keeps clinician reaction reports about Austin products or batches (from the Salesforce portal and the Oracle order
-- desk) in the NEW u_imp_clinician_reaction import set table, from which an agent opens an adverse event case;
-- sn_customerservice_case, which the extracts read, is only written when the case is opened. Coco's reports are
-- discarded.

UPDATE incoming_clinician_reaction_report i SET discard_reason = 'other estate: not an Austin product or batch'
 WHERE NOT (i.product_code LIKE 'AU-%' OR coalesce(i.batch_identifier, '') ~ '^A[0-9]{2}-');
INSERT INTO servicenow_csm.u_imp_clinician_reaction
       (u_report_id, u_reported_on, u_patient_ref, u_clinician_npi, u_product_code, u_lot_number, u_description,
        u_severity, sys_import_state)
SELECT i.adverse_event_identifier, i.adverse_event_reported_date, i.patient_pseudonym_identifier,
       i.clinician_identifier, i.product_code, i.batch_identifier, i.adverse_event_description,
       i.adverse_event_reported_severity, 'pending'
  FROM incoming_clinician_reaction_report i
 WHERE i.discard_reason IS NULL
ON CONFLICT (u_report_id) DO UPDATE SET
       u_reported_on = EXCLUDED.u_reported_on, u_patient_ref = EXCLUDED.u_patient_ref,
       u_clinician_npi = EXCLUDED.u_clinician_npi, u_product_code = EXCLUDED.u_product_code,
       u_lot_number = EXCLUDED.u_lot_number, u_description = EXCLUDED.u_description,
       u_severity = EXCLUDED.u_severity;
