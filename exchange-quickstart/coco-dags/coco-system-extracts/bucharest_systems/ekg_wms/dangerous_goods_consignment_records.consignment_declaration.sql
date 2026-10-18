-- Extract: Warehouse Management System (WMS) (Bucharest) -> Dangerous Goods Consignment Records / consignment_declaration
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_declaration
-- Despatches carrying dangerous goods (nr_onu set); carrier = SAP vendor number; local-time text to UTC.
SELECT
  e.nr_exp::varchar(40) AS shipment_identifier,
  (to_timestamp(e.data_exp, 'DD.MM.YYYY HH24:MI')::timestamp AT TIME ZONE 'Europe/Bucharest')::date AS shipment_dispatch_date,
  e.cod_transportator::varchar(40) AS carrier_identifier,
  e.adresa_livrare AS shipment_ship_to_address,
  e.nr_onu::varchar(20) AS transport_classification_code,
  e.cant_adr::double precision AS shipment_quantity,
  e.um_adr::varchar(20) AS shipment_unit,
  e.semnatar::varchar(40) AS declaration_signatory_identifier,
  (to_timestamp(e.data_semnare, 'DD.MM.YYYY HH24:MI')::timestamp AT TIME ZONE 'Europe/Bucharest') AS declaration_signed_timestamp,
  e.nr_cert_semnatar::varchar(40) AS certificate_identifier
FROM ekg_wms.expeditii e
WHERE e.nr_onu IS NOT NULL
