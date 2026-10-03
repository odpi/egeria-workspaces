-- Subscription: aus_labware_lims__supplier_master_data - LabWare Enterprise LIMS (Austin) receives Supplier Master Data
-- Destination: austin_systems.labware_lims (SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820)
-- Why it subscribes: Supplier Material Certificates depends on it (supplier documentation)
-- Keeps the Austin material suppliers in the vendor table (name V + SAP vendor number, approved flag), adding new
-- ones and refreshing names and approval; the certificate extract only reads the vendor number, which never changes.
-- Non-material suppliers, risk and bank details (not LIMS business) and Coco and EKG suppliers are discarded.

UPDATE incoming_supplier i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
UPDATE incoming_supplier i SET discard_reason = 'not a material supplier'
 WHERE i.discard_reason IS NULL AND i.supplier_type <> 'material supplier';
INSERT INTO labware_lims.vendor AS v (name, description, c_sap_vendor_no, approved)
SELECT 'V' || i.supplier_identifier, left(i.supplier_name, 200), i.supplier_identifier,
       CASE WHEN i.supplier_approved_flag AND i.supplier_current_status = 'active' THEN 'T' ELSE 'F' END
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description, approved = EXCLUDED.approved
 WHERE (v.description, v.approved)
       IS DISTINCT FROM (EXCLUDED.description, EXCLUDED.approved);

UPDATE incoming_supplier_risk_status SET discard_reason = 'supplier risk not kept by LIMS';
UPDATE incoming_supplier_payment_details SET discard_reason = 'supplier bank details not kept by LIMS';
