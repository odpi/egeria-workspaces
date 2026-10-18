-- Extract: Siemens Opcenter MES (Bucharest) -> Cold Chain Transit Records / transit_temperature_record
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.cold_chain_transit_records.transit_temperature_record
-- shipmentmonitor joined to container (batch) and product; recordcomplete 0/1 to boolean.
SELECT
  m.shipmentname::varchar(40) AS shipment_identifier,
  p.productname::varchar(20) AS product_code,
  c.containername::varchar(40) AS batch_identifier,
  m.loggerid::varchar(40) AS device_identifier,
  m.departdate AS shipment_transit_start_timestamp,
  m.arrivedate AS shipment_transit_end_timestamp,
  m.mintemp::double precision AS shipment_transit_minimum_temperature,
  m.maxtemp::double precision AS shipment_transit_maximum_temperature,
  (m.recordcomplete = 1) AS shipment_transit_record_complete_flag
FROM opcenter_mes.shipmentmonitor m
JOIN opcenter_mes.container c ON c.containerid = m.containerid
JOIN opcenter_mes.product p ON p.productid = m.productid
