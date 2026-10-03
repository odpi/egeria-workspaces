-- Extract: OpenText Trading Grid EDI (Austin) -> Dangerous Goods Consignment Records / consignment_document
-- Source: austin_systems.opentext_edi (SoftwareServer::AUS-SYS-015::SN-EDI-AU-20190620)
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_document
-- tg_document for shipments; document types translated to declaration / safety data sheet / handling instructions /
-- other.
SELECT
  d.business_ref::varchar(40) AS shipment_identifier,
  d.document_ref_number::varchar(60) AS document_identifier,
  (CASE d.doc_type WHEN 'IFTDGN' THEN 'declaration' WHEN 'SDS' THEN 'safety data sheet'
        WHEN 'IFTMIN' THEN 'handling instructions' ELSE 'other' END)::varchar(40) AS document_type,
  d.document_date AS document_date
FROM opentext_edi.tg_document d
WHERE d.tracking_status IN ('ACCEPTED', 'DELIVERED')
