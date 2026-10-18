-- Extract: Siemens Opcenter MES (Austin) -> Batch Execution Records / execution_step
-- Source: austin_systems.opcenter_mes (SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601)
-- Target: coco_data_hub.batch_execution_records.execution_step
-- Completed historymainline rows joined to container, spec and employee; performer pseudonymised from the Workday
-- employee number; signature assembled from the verifier and signing time; txnstatus mapped to the product's status
-- words.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  h.stepsequence AS execution_step_number,
  sp.specname::varchar(40) AS execution_step_code,
  h.moveindate AS execution_step_start_timestamp,
  h.moveoutdate AS execution_step_end_timestamp,
  ('WP-' || upper(substr(md5('AUS:' || e.employeenumber), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  (e.employeename || ' performed; ' || v.employeename || ' ' || lower(h.esigmeaning) || ' at '
     || to_char(h.esigdate AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"'))::varchar(200) AS execution_step_signature,
  (CASE h.txnstatus WHEN 'Completed' THEN 'complete' WHEN 'CompletedWithException' THEN 'complete with deviation'
        ELSE 'aborted' END)::varchar(100) AS execution_step_status
FROM opcenter_mes.historymainline h
JOIN opcenter_mes.container c ON c.containerid = h.containerid
JOIN opcenter_mes.spec sp ON sp.specid = h.specid
JOIN opcenter_mes.employee e ON e.employeeid = h.employeeid
JOIN opcenter_mes.employee v ON v.employeeid = h.esigemployeeid
WHERE h.moveoutdate IS NOT NULL
