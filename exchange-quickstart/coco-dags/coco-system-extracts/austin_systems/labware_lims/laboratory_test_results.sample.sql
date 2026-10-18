-- Extract: LabWare Enterprise LIMS (Austin) -> Laboratory Test Results / sample
-- Source: austin_systems.labware_lims (SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820)
-- Target: coco_data_hub.laboratory_test_results.sample
-- sample joined to lot, excluding supplier-certificate samples; sample type and status codes translated; raw lots give
-- the lot, finished/in-process samples the batch.
SELECT
  s.text_id::varchar(40) AS sample_identifier,
  (CASE s.sample_type WHEN 'RAW_MAT' THEN 'raw material' WHEN 'IPC' THEN 'in-process' ELSE 'finished product' END)::varchar(20) AS sample_type,
  (CASE WHEN l.c_lot_type = 'RAW' THEN l.lot_name END)::varchar(40) AS lot_identifier,
  (CASE WHEN l.c_lot_type = 'FINISHED' THEN l.lot_name END)::varchar(40) AS batch_identifier,
  s.sampled_date AS sample_collection_timestamp,
  (CASE s.status WHEN 'U' THEN 'received' WHEN 'I' THEN 'in test' ELSE 'complete' END)::varchar(20) AS sample_current_status
FROM labware_lims.sample s
JOIN labware_lims.lot l ON l.lot_number = s.lot
WHERE s.sample_type <> 'SUPPLIER_COA'
