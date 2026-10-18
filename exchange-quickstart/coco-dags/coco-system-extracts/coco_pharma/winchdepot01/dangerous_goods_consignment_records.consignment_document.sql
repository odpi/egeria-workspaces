-- Extract: Winchester Depot Management System (Coco core) -> Dangerous Goods Consignment Records / consignment_document
-- Source: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_document
-- dg_docs; document type codes expanded.
SELECT
  d.cons_no::varchar(40)            AS shipment_identifier,
  d.doc_ref::varchar(60)            AS document_identifier,
  (CASE d.doc_typ WHEN 'DGD' THEN 'declaration' WHEN 'SDS' THEN 'safety data sheet'
                  WHEN 'HI' THEN 'handling instructions' ELSE 'other' END)::varchar(40) AS document_type,
  d.doc_dt                          AS document_date
FROM winchdepot01.dg_docs d
