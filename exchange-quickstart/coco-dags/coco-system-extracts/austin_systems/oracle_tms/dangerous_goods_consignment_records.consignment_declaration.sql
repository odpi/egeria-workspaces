-- Extract: Oracle TMS (Austin) -> Dangerous Goods Consignment Records / consignment_declaration
-- Source: austin_systems.oracle_tms (SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_declaration
-- Shipments carrying a UN_NUMBER reference; carrier from the service provider GID; address from the destination
-- location; declaration from the DG attributes.
SELECT
  s.shipment_xid::varchar(40) AS shipment_identifier,
  s.start_time::date AS shipment_dispatch_date,
  split_part(s.servprov_gid, '.', 2)::varchar(40) AS carrier_identifier,
  concat_ws(', ', l.location_name, l.address_line1, l.city, l.province_code || ' ' || l.postal_code, l.country_code3_gid) AS shipment_ship_to_address,
  (SELECT r.shipment_refnum_value FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.UN_NUMBER' LIMIT 1)::varchar(20) AS transport_classification_code,
  s.total_net_volume::double precision AS shipment_quantity,
  s.total_net_volume_uom_code::varchar(20) AS shipment_unit,
  s.attribute1::varchar(40) AS declaration_signatory_identifier,
  s.attribute_date1 AS declaration_signed_timestamp,
  s.attribute2::varchar(40) AS certificate_identifier
FROM oracle_tms.shipment s
JOIN oracle_tms.location l ON l.location_gid = s.dest_location_gid
WHERE EXISTS (SELECT 1 FROM oracle_tms.shipment_refnum r WHERE r.shipment_gid = s.shipment_gid AND r.shipment_refnum_qual_gid = 'AUS.UN_NUMBER')
