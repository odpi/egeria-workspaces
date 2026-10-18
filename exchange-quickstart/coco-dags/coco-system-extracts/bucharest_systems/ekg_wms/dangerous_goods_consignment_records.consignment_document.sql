-- Extract: Warehouse Management System (WMS) (Bucharest) -> Dangerous Goods Consignment Records / consignment_document
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.dangerous_goods_consignment_records.consignment_document
-- documente_exp of dangerous goods despatches; document type codes translated.
SELECT
  d.nr_exp::varchar(40) AS shipment_identifier,
  d.nr_doc::varchar(60) AS document_identifier,
  (CASE d.tip_doc WHEN 'DECLARATIE_ADR' THEN 'dangerous goods declaration' WHEN 'AVIZ_INSOTIRE' THEN 'delivery note'
        WHEN 'FISA_TEMPERATURA' THEN 'temperature record' ELSE lower(d.tip_doc) END)::varchar(40) AS document_type,
  d.data_doc AS document_date
FROM ekg_wms.documente_exp d
JOIN ekg_wms.expeditii e ON e.nr_exp = d.nr_exp
WHERE e.nr_onu IS NOT NULL
