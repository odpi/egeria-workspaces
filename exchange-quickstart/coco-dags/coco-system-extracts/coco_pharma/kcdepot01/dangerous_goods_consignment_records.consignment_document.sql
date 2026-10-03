-- Extract: Kansas City Depot Management System (Coco core) -> Dangerous Goods Consignment Records / consignment_document
-- Source: coco_pharma.kcdepot01 (System::KCDEPOT01)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_document
-- shipment_doc; document id is BOL/type, BOL counted as the declaration.
SELECT
  d.bol_nbr::varchar(40)              AS shipment_identifier,
  (d.bol_nbr || '/' || d.doc_type_cd)::varchar(60) AS document_identifier,
  (CASE d.doc_type_cd WHEN 'BOL' THEN 'declaration' WHEN 'SDS' THEN 'safety data sheet'
                      WHEN 'ERG' THEN 'handling instructions' ELSE 'other' END)::varchar(40) AS document_type,
  d.doc_dt                            AS document_date
FROM kcdepot01.shipment_doc d
