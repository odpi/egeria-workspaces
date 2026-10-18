-- Extract: Warehouse Management System (WMS) (Bucharest) -> Goods Receipts / goods_receipt
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.goods_receipts.goods_receipt
-- receptii; the SAP material document is the receipt identifier; supplier and order are SAP numbers; zone prefixed
-- with the plant.
SELECT
  r.sap_doc_mat::varchar(40) AS goods_receipt_identifier,
  r.nr_comanda::varchar(40) AS order_identifier,
  r.cod_furnizor::varchar(40) AS supplier_identifier,
  r.cod_art::varchar(20) AS raw_material_code,
  r.lot_intern::varchar(40) AS lot_identifier,
  (to_timestamp(r.data_rec, 'DD.MM.YYYY HH24:MI')::timestamp AT TIME ZONE 'Europe/Bucharest')::date AS goods_receipt_date,
  r.cant AS goods_receipt_quantity,
  ('RO10-' || r.depozit)::varchar(20) AS warehouse_code,
  r.nr_certificat::varchar(40) AS certificate_identifier
FROM ekg_wms.receptii r
