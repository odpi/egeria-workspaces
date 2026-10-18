-- Extract: Rockwell FactoryTalk (Bucharest) -> Process Parameter Time Series / process_parameter_reading
-- Source: bucharest_systems.factorytalk (SoftwareServer::SYS-015::Rockwell FactoryTalk)
-- Target: coco_data_hub.process_parameter_time_series.process_parameter_reading
-- floattable joined to tagtable and hmitag; local data-log time converted from Europe/Bucharest to UTC; the batch is
-- the unit's BatchID string tag value in force at the reading time (empty = no batch); alarm limits give the minimum
-- and maximum.
WITH batch_tag AS (
  SELECT split_part(t.tagname, '\', 1) AS unit, s.dateandtime AS since,
         lead(s.dateandtime, 1, 'infinity'::timestamp) OVER (PARTITION BY s.tagindex ORDER BY s.dateandtime) AS until,
         nullif(trim(s.val), '') AS batchid
  FROM factorytalk.stringtable s
  JOIN factorytalk.tagtable t ON t.tagindex = s.tagindex
  WHERE t.tagname LIKE '%\BatchID'
)
SELECT
  split_part(t.tagname, '\', 1)::varchar(40) AS equipment_identifier,
  split_part(t.tagname, '\', 2)::varchar(40) AS process_parameter_code,
  ((f.dateandtime + f.millitm * interval '1 millisecond') AT TIME ZONE 'Europe/Bucharest') AS process_parameter_timestamp,
  b.batchid::varchar(40) AS batch_identifier,
  f.val AS process_parameter_value,
  m.units::varchar(20) AS process_parameter_unit,
  m.alarm_lo AS process_parameter_minimum_value,
  m.alarm_hi AS process_parameter_maximum_value
FROM factorytalk.floattable f
JOIN factorytalk.tagtable t ON t.tagindex = f.tagindex
JOIN factorytalk.hmitag m ON m.tagname = t.tagname
LEFT JOIN batch_tag b ON b.unit = split_part(t.tagname, '\', 1) AND f.dateandtime >= b.since AND f.dateandtime < b.until
