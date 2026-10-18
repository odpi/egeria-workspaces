-- Subscription: buc_opcenter_mes__temperature_excursion_assessments - Siemens Opcenter MES (Bucharest) receives Temperature Excursion Assessments
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Electronic Batch Records depends on it (disposition recorded)
-- Keeps the assessment and disposition of each temperature excursion on an EKG batch of this MES (batch, or the
-- monitored shipment's container) as a quality event in extqualityevent (eventtype TemperatureExcursion), shown in the
-- EBR and blocking the batch until dispositioned.  EKG excursions on shipments the MES does not monitor are discarded,
-- as are other companies' (Coco group data - EKG is not yet integrated).  The product has no source yet.
WITH b AS (
  SELECT i.excursion_identifier,
         coalesce((SELECT c.containerid FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier),
                  (SELECT min(m.containerid) FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier)) AS containerid
    FROM incoming_excursion_assessment i
)
UPDATE incoming_excursion_assessment i
   SET discard_reason = (CASE WHEN i.shipment_identifier LIKE 'EXP-%' OR i.batch_identifier ~ '^(EK|SA)[0-9]{2}-[0-9]{4}$'
                              THEN 'no batch or shipment of the MES' ELSE 'Coco group data - EKG not yet integrated' END)
  FROM b
 WHERE b.excursion_identifier = i.excursion_identifier AND b.containerid IS NULL;

INSERT INTO opcenter_mes.extqualityevent (eventname, eventtype, containerid, sourcesystem, raiseddate, eventstatus,
                                          dispositionstatus, dispositiondate, shipmentname, description, lastchangedate)
SELECT i.excursion_identifier, 'TemperatureExcursion',
       coalesce((SELECT c.containerid FROM opcenter_mes.container c WHERE c.containername = i.batch_identifier),
                (SELECT min(m.containerid) FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier)),
       'COLDCHAIN', i.excursion_assessment_timestamp, 'assessed', i.excursion_disposition_status, i.excursion_assessment_timestamp,
       i.shipment_identifier, i.excursion_assessment_notes, now()
  FROM incoming_excursion_assessment i
 WHERE i.discard_reason IS NULL
ON CONFLICT (eventname) DO UPDATE
   SET containerid = EXCLUDED.containerid, raiseddate = EXCLUDED.raiseddate, dispositionstatus = EXCLUDED.dispositionstatus,
       dispositiondate = EXCLUDED.dispositiondate, shipmentname = EXCLUDED.shipmentname, description = EXCLUDED.description,
       lastchangedate = now()
 WHERE (opcenter_mes.extqualityevent.containerid, opcenter_mes.extqualityevent.raiseddate,
        opcenter_mes.extqualityevent.dispositionstatus, opcenter_mes.extqualityevent.dispositiondate,
        opcenter_mes.extqualityevent.shipmentname, opcenter_mes.extqualityevent.description)
       IS DISTINCT FROM (EXCLUDED.containerid, EXCLUDED.raiseddate, EXCLUDED.dispositionstatus, EXCLUDED.dispositiondate,
                         EXCLUDED.shipmentname, EXCLUDED.description);
