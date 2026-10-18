-- Extract: Siemens Opcenter MES (Bucharest) -> Electronic Batch Records / batch_record
-- Source: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Target: coco_data_hub.electronic_batch_records.batch_record
-- container joined to product and ebrheader; reviewcompleteflag 0/1 to boolean; QP status to the product's
-- certification status words.
SELECT
  c.containername::varchar(40) AS batch_identifier,
  p.productname::varchar(20) AS product_code,
  c.patientpseudonym::varchar(40) AS patient_pseudonym_identifier,
  c.startdate AS batch_start_timestamp,
  c.enddate AS batch_end_timestamp,
  c.qty::integer AS batch_quantity,
  (e.reviewcompleteflag = 1) AS batch_record_complete_flag,
  (CASE e.qpcertstatus WHEN 'Certified' THEN 'certified' WHEN 'Deferred' THEN 'deferred'
        WHEN 'Pending' THEN 'pending' ELSE 'not started' END)::varchar(20) AS batch_certification_status
FROM opcenter_mes.container c
JOIN opcenter_mes.product p ON p.productid = c.productid
JOIN opcenter_mes.ebrheader e ON e.containerid = c.containerid
