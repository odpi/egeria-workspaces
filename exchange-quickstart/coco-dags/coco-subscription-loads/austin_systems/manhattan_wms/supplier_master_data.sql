-- Subscription: aus_manhattan_wms__supplier_master_data - Manhattan WMS (Austin) receives Supplier Master Data
-- Destination: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Why it subscribes: Goods Receipts depends on it (approved supplier)
-- Keeps the Austin suppliers (SAP vendor numbers, the business partner IDs on its ASNs) in the NEW business_partner
-- table with their approval and status, so receiving can refuse ASNs from unapproved suppliers. Risk and bank
-- details (not WMS business) and Coco and EKG suppliers are discarded.

UPDATE incoming_supplier i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO manhattan_wms.business_partner
       (business_partner_id, description, bp_type, country_code, approved_flag, approved_date, bp_status)
SELECT i.supplier_identifier, i.supplier_name, i.supplier_type, i.supplier_country,
       CASE WHEN i.supplier_approved_flag THEN 'Y' ELSE 'N' END, i.supplier_approved_date, i.supplier_current_status
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (business_partner_id) DO UPDATE SET
       description = EXCLUDED.description, bp_type = EXCLUDED.bp_type, country_code = EXCLUDED.country_code,
       approved_flag = EXCLUDED.approved_flag, approved_date = EXCLUDED.approved_date, bp_status = EXCLUDED.bp_status;

UPDATE incoming_supplier_risk_status SET discard_reason = 'supplier risk not kept by the WMS';
UPDATE incoming_supplier_payment_details SET discard_reason = 'supplier bank details not kept by the WMS';
