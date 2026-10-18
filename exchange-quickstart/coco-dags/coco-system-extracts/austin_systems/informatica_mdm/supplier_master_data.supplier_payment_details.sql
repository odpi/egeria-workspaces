-- Extract: Informatica MDM (Austin) -> Supplier Master Data / supplier_payment_details
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.supplier_master_data.supplier_payment_details
-- Current c_b_party_bank_acct per supplier joined to the SAP cross-reference.
SELECT
  x.pkey_src_object::varchar(40) AS supplier_identifier,
  b.bank_acct_key::varchar(40) AS bank_account_current_identifier,
  b.bank_nm::varchar(120) AS bank_account_provider_name,
  b.bank_country_cd::varchar(60) AS bank_account_country,
  b.change_request_ref::varchar(40) AS payment_detail_change_identifier,
  b.verified_dt AS payment_detail_verified_date
FROM informatica_mdm.c_b_party_bank_acct b
JOIN informatica_mdm.c_b_party_xref x ON x.rowid_object = b.rowid_party AND x.rowid_system = 'SAP_S4'
WHERE b.hub_state_ind = 1 AND b.eff_end_dt IS NULL
