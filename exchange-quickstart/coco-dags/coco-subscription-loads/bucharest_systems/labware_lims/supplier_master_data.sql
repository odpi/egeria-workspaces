-- Subscription: buc_labware_lims__supplier_master_data - LIMS LabWare Enterprise (Bucharest) receives Supplier Master Data
-- Destination: bucharest_systems.labware_lims (SoftwareServer::SYS-004::LIMS LabWare Enterprise)
-- Why it subscribes: Supplier Material Certificates depends on it (supplier documentation)
-- Keeps EKG's SAP vendors (vendor numbers 7xxxxx) in the LIMS vendor table: the name and approved T/F are refreshed on
-- the vendor carrying that SAP number, and a new vendor (name V + SAP number) is added for one not yet known, so
-- supplier certificates can be logged against it.  Screening results and bank details are not LIMS business.  Coco and
-- Austin suppliers are discarded (EKG is not yet integrated).
UPDATE incoming_supplier SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_risk_status SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_risk_status SET discard_reason = 'supplier screening is not kept in LIMS' WHERE discard_reason IS NULL;
UPDATE incoming_supplier_payment_details SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE supplier_identifier !~ '^7[0-9]{5}$';
UPDATE incoming_supplier_payment_details SET discard_reason = 'bank details are not kept in LIMS' WHERE discard_reason IS NULL;

UPDATE labware_lims.vendor v
   SET description = left(coalesce(i.supplier_name, v.description), 200),
       approved = (CASE WHEN i.supplier_approved_flag AND coalesce(i.supplier_current_status, 'active') = 'active' THEN 'T' ELSE 'F' END)
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL AND v.c_sap_vendor_no = i.supplier_identifier;

INSERT INTO labware_lims.vendor (name, description, c_sap_vendor_no, approved)
SELECT 'V' || i.supplier_identifier, left(coalesce(i.supplier_name, i.supplier_identifier), 200), i.supplier_identifier,
       (CASE WHEN i.supplier_approved_flag AND coalesce(i.supplier_current_status, 'active') = 'active' THEN 'T' ELSE 'F' END)
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM labware_lims.vendor v WHERE v.c_sap_vendor_no = i.supplier_identifier)
ON CONFLICT (name) DO NOTHING;
