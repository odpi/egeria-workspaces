-- Subscription: aus_informatica_mdm__supplier_payment_detail_changes - Informatica MDM (Austin) receives Supplier Payment Detail Changes
-- Destination: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Why it subscribes: Supplier Master Data depends on it (verified bank details)
-- Keeps the Austin bank-detail changes (SAP Ariba requests) not yet applied to a golden bank account in the
-- C_L_PARTY_BANK_ACCT landing table, where the data steward's verification task picks them up. Changes already
-- applied (change reference on C_B_PARTY_BANK_ACCT), MDM's own verification evidence and other estates' changes are
-- discarded.

UPDATE incoming_payment_detail_change i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
UPDATE incoming_payment_detail_change i SET discard_reason = 'already applied to the golden bank account'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_party_bank_acct b
                WHERE b.change_request_ref = i.payment_detail_change_identifier);
INSERT INTO informatica_mdm.c_l_party_bank_acct
       (rowid_system, pkey_src_object, party_src_key, bank_acct_key, prev_bank_acct_key, requested_ts, requester_txt,
        change_status_cd)
SELECT 'DATA_HUB', i.payment_detail_change_identifier, i.supplier_identifier, i.bank_account_current_identifier,
       i.bank_account_previous_identifier, i.payment_detail_change_requested_timestamp,
       i.payment_detail_change_requester_identifier, upper(i.payment_detail_change_status)
  FROM incoming_payment_detail_change i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       party_src_key = EXCLUDED.party_src_key, bank_acct_key = EXCLUDED.bank_acct_key,
       prev_bank_acct_key = EXCLUDED.prev_bank_acct_key, requested_ts = EXCLUDED.requested_ts,
       requester_txt = EXCLUDED.requester_txt, change_status_cd = EXCLUDED.change_status_cd;

UPDATE incoming_verification_evidence i SET discard_reason = 'already held: verification recorded in MDM'
 WHERE EXISTS (SELECT 1 FROM informatica_mdm.c_b_party_bank_verif v
                WHERE v.change_request_ref = i.payment_detail_change_identifier);
UPDATE incoming_verification_evidence SET discard_reason = 'other estate: not an MDM verification'
 WHERE discard_reason IS NULL;
