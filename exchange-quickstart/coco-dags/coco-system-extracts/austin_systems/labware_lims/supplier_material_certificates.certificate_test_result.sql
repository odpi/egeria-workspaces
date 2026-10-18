-- Extract: LabWare Enterprise LIMS (Austin) -> Supplier Material Certificates / certificate_test_result
-- Source: austin_systems.labware_lims (SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820)
-- Target: coco_data_hub.supplier_material_certificates.certificate_test_result
-- Results entered from supplier certificates, with the material's specification limits.
SELECT
  s.c_supplier_cert_no::varchar(40) AS certificate_identifier,
  r.name::varchar(40) AS test_code,
  r.formatted_entry::varchar(60) AS test_value,
  r.units::varchar(20) AS test_unit,
  ps.min_value::varchar(60) AS specification_minimum_value,
  ps.max_value::varchar(60) AS specification_maximum_value
FROM labware_lims.result r
JOIN labware_lims.sample s ON s.sample_number = r.sample_number
LEFT JOIN labware_lims.product_spec ps ON ps.product = s.product AND ps.analysis = r.analysis AND ps.component = r.name
WHERE s.sample_type = 'SUPPLIER_COA'
