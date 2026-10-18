-- Extract: Esri ArcGIS Enterprise (Austin) -> Therapy Delivery Events / delivery_event
-- Source: austin_systems.arcgis (SoftwareServer::AUS-SYS-044::SN-GIS-AU-20230601)
-- Target: coco_data_hub.therapy_delivery_events.delivery_event
-- Each tracker fix is an in-transit event; location is the reverse-geocoded place; storage description reports the
-- logged shipper temperature.
SELECT
  p.batch_no::varchar(40) AS batch_identifier,
  'in transit'::varchar(20) AS shipment_event_type,
  p.fix_time AS shipment_event_timestamp,
  p.patient_ref::varchar(40) AS patient_pseudonym_identifier,
  p.order_no::varchar(40) AS order_identifier,
  (p.place_name || ' (' || round(p.latitude::numeric, 2) || ', ' || round(p.longitude::numeric, 2) || ')')::varchar(120) AS shipment_event_location,
  ('LN2 dry shipper; logger ' || p.logger_temp_c || ' C') AS shipment_storage_description
FROM arcgis.therapy_shipment_track_pts p
WHERE p.batch_no IS NOT NULL AND p.order_no IS NOT NULL AND p.patient_ref IS NOT NULL
