-- Extract: Winchester Depot Management System (Coco core) -> Dangerous Goods Consignment Records / consignment_declaration
-- Source: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_declaration
-- dg_consign; carrier is the Coco shipper id.
SELECT
  c.cons_no::varchar(40)            AS shipment_identifier,
  c.desp_dt                         AS shipment_dispatch_date,
  c.carr_id::varchar(40)            AS carrier_identifier,
  c.ship_to                         AS shipment_ship_to_address,
  c.un_no::varchar(20)              AS transport_classification_code,
  c.qty::double precision           AS shipment_quantity,
  c.uom::varchar(20)                AS shipment_unit,
  c.signed_by::varchar(40)          AS declaration_signatory_identifier,
  c.signed_ts                       AS declaration_signed_timestamp,
  c.dg_cert::varchar(40)            AS certificate_identifier
FROM winchdepot01.dg_consign c
