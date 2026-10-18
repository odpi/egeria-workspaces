-- Extract: Manhattan WMS (Austin) -> Material Quarantine Dispositions / quarantine_record
-- Source: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Target: coco_data_hub.material_quarantine_dispositions.quarantine_record
-- batch_master for received raw material and packaging lots joined to the receipt; batch status Q/R/X to
-- held/released/rejected.
SELECT
  b.batch_nbr::varchar(40) AS lot_identifier,
  i.item_name::varchar(20) AS raw_material_code,
  a.tc_asn_id::varchar(40) AS goods_receipt_identifier,
  b.quarantine_start_dttm AS lot_quarantine_start_timestamp,
  f.whse::varchar(20) AS warehouse_code,
  d.received_qty AS lot_quantity,
  b.ref_field_1::varchar(40) AS sample_identifier,
  (CASE b.batch_status WHEN 'Q' THEN 'held' WHEN 'R' THEN 'released' ELSE 'rejected' END)::varchar(20) AS lot_quarantine_status
FROM manhattan_wms.batch_master b
JOIN manhattan_wms.item_cbo i ON i.item_id = b.item_id AND i.item_type IN ('RM', 'PK')
JOIN manhattan_wms.asn_detail d ON d.batch_nbr = b.batch_nbr AND d.sku_id = b.item_id
JOIN manhattan_wms.asn a ON a.asn_id = d.asn_id
JOIN manhattan_wms.facility f ON f.facility_id = a.destination_facility_id
