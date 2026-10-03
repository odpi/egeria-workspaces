-- Extract: Global Manufacturing Planning (Coco core) -> Personalised Manufacturing Schedule / manufacturing_slot
-- Source: coco_pharma.manufacturing_planning (System::manufacturing-planning)
-- Target: coco_data_hub.personalised_manufacturing_schedule.manufacturing_slot
-- plnord filtered to ord_typ PERS joined to plnord_pers; ord_sts translated to scheduled / in progress / complete / cancelled.
SELECT
  o.batch_no::varchar(40)                       AS batch_identifier,
  p.cust_ord_ref::varchar(40)                   AS order_identifier,
  p.patient_ref::varchar(40)                    AS patient_pseudonym_identifier,
  o.matnr::varchar(20)                          AS product_code,
  o.sched_start                                 AS slot_start_timestamp,
  o.sched_end                                   AS slot_end_timestamp,
  p.param_text                                  AS patient_parameter_description,
  (CASE o.ord_sts WHEN 'FIRM' THEN 'scheduled' WHEN 'REL' THEN 'scheduled' WHEN 'ACT' THEN 'in progress'
                  WHEN 'CMPL' THEN 'complete' WHEN 'CNCL' THEN 'cancelled' END)::varchar(20) AS slot_status
FROM manufacturing_planning.plnord o
JOIN manufacturing_planning.plnord_pers p ON p.plnord_no = o.plnord_no
WHERE o.ord_typ = 'PERS'
  AND o.batch_no IS NOT NULL
