-- Extract: Edmonton Depot Management System (Coco core) -> Dangerous Goods Consignment Records / consignment_document
-- Source: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_document
-- tdg_document; document id is shipment/doc number, kinds mapped to the product's document types.
SELECT
  d.shipment_no::varchar(40)        AS shipment_identifier,
  (d.shipment_no || '/' || d.doc_no)::varchar(60) AS document_identifier,
  (CASE d.doc_kind WHEN 'TDG Shipping Document' THEN 'declaration' WHEN 'Safety Data Sheet' THEN 'safety data sheet'
                   WHEN 'Handling Instructions' THEN 'handling instructions' ELSE 'other' END)::varchar(40) AS document_type,
  d.doc_date                        AS document_date
FROM eddepot01.tdg_document d
