-- Extract: Kansas City Depot Management System (Coco core) -> Dangerous Goods Consignment Records / consignment_declaration
-- Source: coco_pharma.kcdepot01 (System::KCDEPOT01)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_declaration
-- hazmat_shipment; SCAC to Coco shipper id, UN number formatted UNnnnn, signer to pseudonym via hazmat_employee.
SELECT
  h.bol_nbr::varchar(40)              AS shipment_identifier,
  h.ship_dt                           AS shipment_dispatch_date,
  (CASE h.carrier_scac WHEN 'SPDX' THEN '1' WHEN 'UPSN' THEN '5' WHEN 'DHLA' THEN '6' ELSE h.carrier_scac END)::varchar(40) AS carrier_identifier,
  (h.ship_to_name || ', ' || h.ship_to_addr)::text AS shipment_ship_to_address,
  ('UN' || lpad(h.un_na_nbr::text, 4, '0'))::varchar(20) AS transport_classification_code,
  h.ship_qty::double precision        AS shipment_quantity,
  lower(h.ship_uom)::varchar(20)      AS shipment_unit,
  e.worker_ref::varchar(40)           AS declaration_signatory_identifier,
  h.signed_ts                         AS declaration_signed_timestamp,
  h.hm_cert_nbr::varchar(40)          AS certificate_identifier
FROM kcdepot01.hazmat_shipment h
JOIN kcdepot01.hazmat_employee e ON e.emp_id = h.signer_emp_id
