-- Subscription: coco_procurement01__supplier_payment_detail_changes - Coco Pharmaceuticals Procurement (Coco core) receives Supplier Payment Detail Changes
-- Destination: coco_pharma.procurement01 (System::procurement01)
-- Why it subscribes: Supplier Master Data depends on it (verified bank details)
-- Keeps bank detail changes of Coco vendors (numeric supplier ids below 100000) with their verification in
-- bank_chg_req (NEW); a buyer adds the new vendor_bank row once the change is verified, so vendor_bank (which
-- feeds Supplier Master Data) is not written directly.  Discards Austin (100xxx) and EKG (700xxx) suppliers'
-- changes - all of today's rows come from Austin's own procurement systems.

UPDATE incoming_payment_detail_change SET discard_reason = 'Austin or EKG supplier - not a procurement01 vendor'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';

INSERT INTO procurement01.bank_chg_req (change_ref, vendor_no, requested_ts, requested_by, acct_prev, acct_new, chg_status)
SELECT c.payment_detail_change_identifier, c.supplier_identifier::integer, c.payment_detail_change_requested_timestamp,
       c.payment_detail_change_requester_identifier, c.bank_account_previous_identifier, c.bank_account_current_identifier,
       c.payment_detail_change_status
  FROM incoming_payment_detail_change c
 WHERE c.discard_reason IS NULL
ON CONFLICT (change_ref) DO UPDATE SET vendor_no = EXCLUDED.vendor_no, requested_ts = EXCLUDED.requested_ts,
       requested_by = EXCLUDED.requested_by, acct_prev = EXCLUDED.acct_prev, acct_new = EXCLUDED.acct_new,
       chg_status = EXCLUDED.chg_status;

UPDATE incoming_verification_evidence v SET discard_reason = 'verification of a change procurement01 does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM procurement01.bank_chg_req r WHERE r.change_ref = v.payment_detail_change_identifier);

-- The latest verification of each change is kept.
UPDATE procurement01.bank_chg_req r
   SET verified_ts = v.payment_detail_change_verified_timestamp, verified_by = v.payment_detail_change_verifier_identifier,
       verify_channel = v.payment_detail_change_channel_type, verify_notes = v.payment_detail_change_verified_notes
  FROM (SELECT DISTINCT ON (payment_detail_change_identifier) *
          FROM incoming_verification_evidence
         WHERE discard_reason IS NULL
         ORDER BY payment_detail_change_identifier, payment_detail_change_verified_timestamp DESC) v
 WHERE v.payment_detail_change_identifier = r.change_ref
   AND (r.verified_ts IS NULL OR r.verified_ts <= v.payment_detail_change_verified_timestamp);
