-- Extract: Warehouse Management System (WMS) (Bucharest) -> Material Quarantine Dispositions / quarantine_record
-- Source: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Target: coco_data_hub.material_quarantine_dispositions.quarantine_record
-- carantina joined to receptii; local-time text to UTC; state codes translated.
SELECT
  c.lot_intern::varchar(40) AS lot_identifier,
  r.cod_art::varchar(20) AS raw_material_code,
  r.sap_doc_mat::varchar(40) AS goods_receipt_identifier,
  (c.data_intrare::timestamp AT TIME ZONE 'Europe/Bucharest') AS lot_quarantine_start_timestamp,
  ('RO10-' || c.depozit)::varchar(20) AS warehouse_code,
  c.cant AS lot_quantity,
  c.nr_proba::varchar(40) AS sample_identifier,
  (CASE c.stare WHEN 'C' THEN 'quarantined' WHEN 'E' THEN 'released' WHEN 'R' THEN 'rejected' ELSE 'blocked' END)::varchar(20) AS lot_quarantine_status
FROM ekg_wms.carantina c
JOIN ekg_wms.receptii r ON r.nr_rec = c.nr_rec
