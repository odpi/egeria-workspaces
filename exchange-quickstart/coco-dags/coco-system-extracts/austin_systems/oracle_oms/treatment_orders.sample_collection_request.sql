-- Extract: Oracle Order Management (Austin) -> Treatment Orders / sample_collection_request
-- Source: austin_systems.oracle_oms (SoftwareServer::AUS-SYS-011::SN-OMS-AU-20200310)
-- Target: coco_data_hub.treatment_orders.sample_collection_request
-- doo_headers_all with the PatientTherapy flexfield context (collection site, window, material).
SELECT
  h.source_order_number::varchar(40) AS order_identifier,
  e.attribute_char3::varchar(40) AS sample_collection_location,
  e.attribute_date1 AS sample_collection_start_date,
  e.attribute_date2 AS sample_collection_end_date,
  e.attribute_char4::varchar(60) AS sample_material_type
FROM oracle_oms.doo_headers_all h
JOIN oracle_oms.doo_headers_eff_b e ON e.header_id = h.header_id AND e.context_code = 'PatientTherapy'
WHERE h.source_order_system = 'SFDC'
