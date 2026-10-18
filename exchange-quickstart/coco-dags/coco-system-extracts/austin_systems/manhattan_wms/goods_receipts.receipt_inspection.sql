-- Extract: Manhattan WMS (Austin) -> Goods Receipts / receipt_inspection
-- Source: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Target: coco_data_hub.goods_receipts.receipt_inspection
-- qc_inspection; status codes to accepted / rejected / held.
SELECT
  q.tc_asn_id::varchar(40) AS goods_receipt_identifier,
  q.inspection_dttm::date AS goods_receipt_inspection_date,
  q.inspected_by::varchar(40) AS goods_receipt_inspector_identifier,
  (CASE q.inspection_status WHEN 'A' THEN 'accepted' WHEN 'R' THEN 'rejected' ELSE 'held' END)::varchar(20) AS goods_receipt_inspection_status,
  q.comments AS goods_receipt_inspection_notes
FROM manhattan_wms.qc_inspection q
