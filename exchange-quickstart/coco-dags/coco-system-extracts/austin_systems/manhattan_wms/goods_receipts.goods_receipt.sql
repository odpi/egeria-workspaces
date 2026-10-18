-- Extract: Manhattan WMS (Austin) -> Goods Receipts / goods_receipt
-- Source: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Target: coco_data_hub.goods_receipts.goods_receipt
-- asn + asn_detail + item_cbo + facility for verified receipts; quantity in base units.
SELECT
  a.tc_asn_id::varchar(40) AS goods_receipt_identifier,
  a.tc_purchase_orders_id::varchar(40) AS order_identifier,
  a.business_partner_id::varchar(40) AS supplier_identifier,
  i.item_name::varchar(20) AS raw_material_code,
  d.batch_nbr::varchar(40) AS lot_identifier,
  a.last_received_dttm::date AS goods_receipt_date,
  d.received_qty AS goods_receipt_quantity,
  f.whse::varchar(20) AS warehouse_code,
  d.ref_field_1::varchar(40) AS certificate_identifier
FROM manhattan_wms.asn a
JOIN manhattan_wms.asn_detail d ON d.asn_id = a.asn_id
JOIN manhattan_wms.item_cbo i ON i.item_id = d.sku_id
JOIN manhattan_wms.facility f ON f.facility_id = a.destination_facility_id
WHERE a.asn_status >= 60
