-- Extract: Warehouse Management System (WMS) (Bucharest) -> Goods Receipts / receipt_inspection
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.goods_receipts.receipt_inspection
-- inspectii_receptie joined to receptii; Romanian result codes translated.
SELECT
  r.sap_doc_mat::varchar(40) AS goods_receipt_identifier,
  i.data_insp AS goods_receipt_inspection_date,
  i.inspector::varchar(40) AS goods_receipt_inspector_identifier,
  (CASE i.rezultat WHEN 'ACCEPTAT' THEN 'accepted' WHEN 'ACCEPTAT CU OBS' THEN 'accepted'
        WHEN 'IN ASTEPTARE' THEN 'held' ELSE 'rejected' END)::varchar(20) AS goods_receipt_inspection_status,
  i.observatii AS goods_receipt_inspection_notes
FROM ekg_wms.inspectii_receptie i
JOIN ekg_wms.receptii r ON r.nr_rec = i.nr_rec
