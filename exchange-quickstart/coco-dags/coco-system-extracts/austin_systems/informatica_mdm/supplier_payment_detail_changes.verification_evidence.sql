-- Extract: Informatica MDM (Austin) -> Supplier Payment Detail Changes / verification_evidence
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.supplier_payment_detail_changes.verification_evidence
-- c_b_party_bank_verif steps recorded by the data steward for each bank change request.
SELECT
  v.change_request_ref::varchar(40) AS payment_detail_change_identifier,
  v.verified_ts AS payment_detail_change_verified_timestamp,
  v.verifier_user::varchar(40) AS payment_detail_change_verifier_identifier,
  v.channel_desc::varchar(40) AS payment_detail_change_channel_type,
  v.notes_txt AS payment_detail_change_verified_notes
FROM informatica_mdm.c_b_party_bank_verif v
