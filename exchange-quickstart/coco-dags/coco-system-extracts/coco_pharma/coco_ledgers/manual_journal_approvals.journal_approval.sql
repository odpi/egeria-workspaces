-- Extract: Coco Ledgers (Coco core) -> Manual Journal Approvals / journal_approval
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.manual_journal_approvals.journal_approval
-- gl_je_review of manual journals above the materiality threshold; reviewer to pseudonym, actions to status words.
SELECT
  r.je_id::varchar(40)           AS journal_entry_identifier,
  r.action_at                    AS journal_entry_approval_timestamp,
  u.worker_ref::varchar(40)      AS journal_entry_approver_identifier,
  (CASE r.action WHEN 'APPROVE' THEN 'approved' WHEN 'REJECT' THEN 'rejected' ELSE 'returned for change' END)::varchar(20) AS journal_entry_approval_status,
  r.comments                     AS journal_entry_approval_notes
FROM coco_ledgers.gl_je_review r
JOIN coco_ledgers.fm_user u ON u.user_email = r.action_by
JOIN coco_ledgers.gl_journal j ON j.je_id = r.je_id
WHERE j.je_source = 'MAN' AND j.control_total >= 50000
