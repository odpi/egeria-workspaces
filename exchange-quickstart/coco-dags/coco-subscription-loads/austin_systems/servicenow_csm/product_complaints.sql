-- Subscription: aus_servicenow_csm__product_complaints - ServiceNow Customer Service Management (Austin) receives Product Complaints
-- Destination: austin_systems.servicenow_csm (SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601)
-- Why it subscribes: Consolidated Safety Reports depends on it (complaint with safety content)
-- Keeps nothing: ServiceNow is the only source of Product Complaints, so every complaint and safety assessment is
-- its own case coming back (number already in sn_customerservice_case). Anything else would be another estate's and
-- is discarded.

UPDATE incoming_complaint i SET discard_reason = 'already held: supplied by ServiceNow (case)'
 WHERE EXISTS (SELECT 1 FROM servicenow_csm.sn_customerservice_case c WHERE c.number = i.complaint_identifier);
UPDATE incoming_complaint SET discard_reason = 'other estate: not an Austin case' WHERE discard_reason IS NULL;

UPDATE incoming_complaint_safety_assessment i SET discard_reason = 'already held: supplied by ServiceNow (case)'
 WHERE EXISTS (SELECT 1 FROM servicenow_csm.sn_customerservice_case c WHERE c.number = i.complaint_identifier);
UPDATE incoming_complaint_safety_assessment SET discard_reason = 'other estate: not an Austin case'
 WHERE discard_reason IS NULL;
