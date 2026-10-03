-- Subscription: buc_opentext_ecm__supplier_master_data - OpenText ECM (Bucharest) receives Supplier Master Data
-- Destination: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Why it subscribes: Supplier Material Certificates depends on it (supplier documentation)
-- Adds the supplier's name to every archived supplier certificate of that EKG vendor (category 3002 Certificat
-- furnizor, new attribute 9 Denumire furnizor; attribute 2 holds the SAP vendor number), so certificates can be searched
-- by supplier name.  EKG vendors with no archived certificates are discarded; screening results and bank details are not
-- archived; other suppliers are discarded (Coco group data - EKG is not yet integrated).
UPDATE incoming_supplier SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier i SET discard_reason = 'no supplier documents archived for this supplier'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM opentext_ecm.llattrdata a WHERE a.defid = 3002 AND a.attrid = 2 AND a.valstr = i.supplier_identifier);
UPDATE incoming_supplier SET discard_reason = 'supplier has no name' WHERE discard_reason IS NULL AND supplier_name IS NULL;
UPDATE incoming_supplier_risk_status SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_risk_status SET discard_reason = 'supplier screening is not archived in the ECM' WHERE discard_reason IS NULL;
UPDATE incoming_supplier_payment_details SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not archived in the ECM' WHERE discard_reason IS NULL;

INSERT INTO opentext_ecm.llattrdata (id, defid, attrid, entrynum, valstr, valdate)
SELECT a.id, 3002, 9, 1, left(i.supplier_name, 255), NULL
  FROM incoming_supplier i
  JOIN opentext_ecm.llattrdata a ON a.defid = 3002 AND a.attrid = 2 AND a.valstr = i.supplier_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (id, defid, attrid, entrynum) DO UPDATE SET valstr = EXCLUDED.valstr
 WHERE opentext_ecm.llattrdata.valstr IS DISTINCT FROM EXCLUDED.valstr;
