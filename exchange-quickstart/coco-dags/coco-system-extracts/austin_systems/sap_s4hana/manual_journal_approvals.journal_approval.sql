-- Extract: SAP S/4HANA (Austin) -> Manual Journal Approvals / journal_approval
-- Source: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Target: coco_data_hub.manual_journal_approvals.journal_approval
-- Completed approval work items (swwwihead) linked to the parked document through sww_wi2obj; workflow result to
-- approved / rejected / returned for change.
SELECT
  substr(o.instid, 5, 10)::varchar(40) AS journal_entry_identifier,
  ((to_date(w.wi_aed, 'YYYYMMDD') + w.wi_aet::time) AT TIME ZONE 'UTC') AS journal_entry_approval_timestamp,
  lower(w.wi_aagent)::varchar(40) AS journal_entry_approver_identifier,
  (CASE w.wi_result WHEN 'APPROVE' THEN 'approved' WHEN 'REJECT' THEN 'rejected' ELSE 'returned for change' END)::varchar(20) AS journal_entry_approval_status,
  w.wi_result_note AS journal_entry_approval_notes
FROM sap_s4hana.swwwihead w
JOIN sap_s4hana.sww_wi2obj o ON o.wi_id = w.wi_id AND o.typeid = 'FIPP'
WHERE w.wi_rh_task = 'TS78500112' AND w.wi_stat = 'COMPLETED'
