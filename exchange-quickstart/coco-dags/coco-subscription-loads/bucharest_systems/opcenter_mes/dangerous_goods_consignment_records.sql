-- Subscription: buc_opcenter_mes__dangerous_goods_consignment_records - Siemens Opcenter MES (Bucharest) receives Dangerous Goods Consignment Records
-- Destination: bucharest_systems.opcenter_mes (SoftwareServer::SYS-003::Siemens Opcenter MES)
-- Why it subscribes: Carrier Transit Events depends on it (consigned to carrier)
-- Keeps the WMS's dangerous goods declaration (dry ice, UN number, quantity, ADR signatory) of each shipment this MES
-- monitors in the new table shipmentconsignment, against which the handover to the carrier is recorded; the
-- accompanying documents are not kept.  EKG despatches the MES does not monitor are discarded, as are other companies'
-- consignments (Coco group data - EKG is not yet integrated).
UPDATE incoming_consignment_declaration i SET discard_reason = 'shipment not monitored by the MES'
 WHERE i.shipment_identifier LIKE 'EXP-%'
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier);
UPDATE incoming_consignment_declaration i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opcenter_mes.shipmentmonitor m WHERE m.shipmentname = i.shipment_identifier);
UPDATE incoming_consignment_document SET discard_reason = 'consignment documents are not kept in the MES'
 WHERE shipment_identifier LIKE 'EXP-%';
UPDATE incoming_consignment_document SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

INSERT INTO opcenter_mes.shipmentconsignment (shipmentname, carriervendor, dispatchdate, shiptoaddress, unnumber, dgqty, dguom,
                                              signatory, signeddate, signatorycertificate, lastchangedate)
SELECT i.shipment_identifier, left(i.carrier_identifier, 10), i.shipment_dispatch_date, i.shipment_ship_to_address,
       i.transport_classification_code, i.shipment_quantity, i.shipment_unit, i.declaration_signatory_identifier,
       i.declaration_signed_timestamp, i.certificate_identifier, now()
  FROM incoming_consignment_declaration i
 WHERE i.discard_reason IS NULL
ON CONFLICT (shipmentname) DO UPDATE
   SET carriervendor = EXCLUDED.carriervendor, dispatchdate = EXCLUDED.dispatchdate, shiptoaddress = EXCLUDED.shiptoaddress,
       unnumber = EXCLUDED.unnumber, dgqty = EXCLUDED.dgqty, dguom = EXCLUDED.dguom, signatory = EXCLUDED.signatory,
       signeddate = EXCLUDED.signeddate, signatorycertificate = EXCLUDED.signatorycertificate, lastchangedate = now()
 WHERE (opcenter_mes.shipmentconsignment.carriervendor, opcenter_mes.shipmentconsignment.dispatchdate,
        opcenter_mes.shipmentconsignment.shiptoaddress, opcenter_mes.shipmentconsignment.unnumber,
        opcenter_mes.shipmentconsignment.dgqty, opcenter_mes.shipmentconsignment.dguom,
        opcenter_mes.shipmentconsignment.signatory, opcenter_mes.shipmentconsignment.signeddate,
        opcenter_mes.shipmentconsignment.signatorycertificate)
       IS DISTINCT FROM (EXCLUDED.carriervendor, EXCLUDED.dispatchdate, EXCLUDED.shiptoaddress, EXCLUDED.unnumber,
                         EXCLUDED.dgqty, EXCLUDED.dguom, EXCLUDED.signatory, EXCLUDED.signeddate, EXCLUDED.signatorycertificate);
