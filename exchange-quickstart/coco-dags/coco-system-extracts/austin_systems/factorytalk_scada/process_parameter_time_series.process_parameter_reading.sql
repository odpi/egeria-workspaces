-- Extract: Rockwell FactoryTalk SCADA (Austin) -> Process Parameter Time Series / process_parameter_reading
-- Source: austin_systems.factorytalk_scada (SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610)
-- Target: coco_data_hub.process_parameter_time_series.process_parameter_reading
-- picomp2 values joined to pipoint; the batch is the FactoryTalk Batch unit occupancy (Unit Acquired..Unit Released)
-- covering the reading time; alarm limits give the minimum and maximum.
WITH occupancy AS (
  SELECT a.batchid, a.unit, a.gmt AS acquired,
         coalesce((SELECT min(r.gmt) FROM factorytalk_scada.batch_event_journal r
                   WHERE r.unit = a.unit AND r.batchid = a.batchid AND r.event = 'Unit Released' AND r.gmt >= a.gmt),
                  'infinity'::timestamptz) AS released
  FROM factorytalk_scada.batch_event_journal a
  WHERE a.event = 'Unit Acquired'
)
SELECT
  p.unit_name::varchar(40) AS equipment_identifier,
  split_part(split_part(p.tag, ':', 2), '.', 1)::varchar(40) AS process_parameter_code,
  v.time AS process_parameter_timestamp,
  o.batchid::varchar(40) AS batch_identifier,
  v.value AS process_parameter_value,
  p.engunits::varchar(20) AS process_parameter_unit,
  p.lo_alarm_limit AS process_parameter_minimum_value,
  p.hi_alarm_limit AS process_parameter_maximum_value
FROM factorytalk_scada.picomp2 v
JOIN factorytalk_scada.pipoint p ON p.tag = v.tag
LEFT JOIN occupancy o ON o.unit = p.unit_name AND v.time >= o.acquired AND v.time < o.released
WHERE v.status = 0
