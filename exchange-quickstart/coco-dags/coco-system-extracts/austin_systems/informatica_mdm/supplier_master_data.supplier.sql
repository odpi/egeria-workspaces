-- Extract: Informatica MDM (Austin) -> Supplier Master Data / supplier
-- Source: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Target: coco_data_hub.supplier_master_data.supplier
-- Active c_b_party suppliers identified by their SAP vendor number (c_b_party_xref); class and status codes
-- translated.
SELECT
  x.pkey_src_object::varchar(40) AS supplier_identifier,
  p.org_nm::varchar(200) AS supplier_name,
  (CASE p.supplier_class_cd WHEN 'MATERIAL' THEN 'material supplier' WHEN 'SERVICE' THEN 'service provider' ELSE 'other' END)::varchar(40) AS supplier_type,
  p.country_cd::varchar(60) AS supplier_country,
  (p.onboarding_approved_ind = 'Y') AS supplier_approved_flag,
  p.onboarding_approved_dt AS supplier_approved_date,
  (CASE p.status_cd WHEN 'A' THEN 'active' WHEN 'S' THEN 'suspended' ELSE 'closed' END)::varchar(20) AS supplier_current_status
FROM informatica_mdm.c_b_party p
JOIN informatica_mdm.c_b_party_xref x ON x.rowid_object = p.rowid_object AND x.rowid_system = 'SAP_S4'
WHERE p.party_type_cd = 'SUPPLIER' AND p.hub_state_ind = 1
