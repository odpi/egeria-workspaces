-- Extract: Edmonton Depot Management System (Coco core) -> Dangerous Goods Consignment Records / consignment_declaration
-- Source: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_declaration
-- tdg_shipment; carrier name to Coco shipper id, local signing time to timestamptz, signatory to pseudonym via tdg_signer.
SELECT
  t.shipment_no::varchar(40)        AS shipment_identifier,
  t.ship_date                       AS shipment_dispatch_date,
  (CASE t.carrier_name WHEN 'Speedy Express' THEN '1' WHEN 'United Package' THEN '2' WHEN 'Federal Shipping' THEN '3'
                       WHEN 'Alliance Shippers' THEN '4' WHEN 'UPS' THEN '5' WHEN 'DHL' THEN '6' ELSE t.carrier_name END)::varchar(40) AS carrier_identifier,
  t.consignee_addr                  AS shipment_ship_to_address,
  t.un_number::varchar(20)          AS transport_classification_code,
  t.qty::double precision           AS shipment_quantity,
  (CASE t.unit WHEN 'L' THEN 'L' ELSE lower(t.unit) END)::varchar(20) AS shipment_unit,
  s.worker_ref::varchar(40)         AS declaration_signatory_identifier,
  (t.signed_at::timestamp AT TIME ZONE 'America/Edmonton') AS declaration_signed_timestamp,
  t.tdg_cert_no::varchar(40)        AS certificate_identifier
FROM eddepot01.tdg_shipment t
JOIN eddepot01.tdg_signer s ON s.emp_no = t.signatory
