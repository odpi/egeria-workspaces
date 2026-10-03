-- Extract: Coco Ledgers (Coco core) -> Manual Journal Approvals / journal_entry
-- Source: coco_pharma.coco_ledgers (System::coco-ledgers)
-- Target: coco_data_hub.manual_journal_approvals.journal_entry
-- gl_journal manual entries at or above the 50,000 materiality threshold; control total at or above the 50,000 materiality threshold; period text to YYYY-MM; preparer email to pseudonym via fm_user.
SELECT
  j.je_id::varchar(40)           AS journal_entry_identifier,
  to_char(to_date(j.period_name, 'Mon-YY'), 'YYYY-MM')::varchar(10) AS accounting_period_code,
  j.entity_id::varchar(10)       AS legal_entity_code,
  j.control_total::numeric(18,2)  AS journal_entry_amount,
  j.description                  AS journal_entry_description,
  u.worker_ref::varchar(40)      AS journal_entry_preparer_identifier,
  j.submitted_at                 AS journal_entry_submitted_timestamp
FROM coco_ledgers.gl_journal j
JOIN coco_ledgers.fm_user u ON u.user_email = j.prepared_by
WHERE j.je_source = 'MAN' AND j.control_total >= 50000
