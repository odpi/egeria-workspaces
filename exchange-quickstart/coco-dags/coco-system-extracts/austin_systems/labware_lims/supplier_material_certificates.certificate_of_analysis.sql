-- Extract: LabWare Enterprise LIMS (Austin) -> Supplier Material Certificates / certificate_of_analysis
-- Source: austin_systems.labware_lims (SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820)
-- Target: coco_data_hub.supplier_material_certificates.certificate_of_analysis
-- SUPPLIER_COA samples joined to lot and vendor; supplier identifier is the SAP vendor number; COA/COC to words.
SELECT
  s.c_supplier_cert_no::varchar(40) AS certificate_identifier,
  v.c_sap_vendor_no::varchar(40) AS supplier_identifier,
  l.product::varchar(20) AS raw_material_code,
  l.lot_name::varchar(40) AS lot_identifier,
  (CASE s.c_cert_type WHEN 'COC' THEN 'certificate of conformity' ELSE 'certificate of analysis' END)::varchar(40) AS certificate_type,
  s.sampled_date::date AS certificate_date,
  (s.c_declared_conform = 'T') AS certificate_conformity_flag
FROM labware_lims.sample s
JOIN labware_lims.lot l ON l.lot_number = s.lot
JOIN labware_lims.vendor v ON v.name = l.vendor
WHERE s.sample_type = 'SUPPLIER_COA'
