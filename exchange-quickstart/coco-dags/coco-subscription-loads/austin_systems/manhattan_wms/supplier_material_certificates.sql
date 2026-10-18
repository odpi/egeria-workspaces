-- Subscription: aus_manhattan_wms__supplier_material_certificates - Manhattan WMS (Austin) receives Supplier Material Certificates
-- Destination: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Why it subscribes: Goods Receipts depends on it (certificate of analysis)
-- Keeps the supplier certificates for Austin suppliers in the NEW supplier_cert table, matched at receipt against
-- the certificate number on the ASN line (ref_field_1). Certificate test values (checked by the laboratory, not the
-- WMS) and EKG suppliers' certificates are discarded.

UPDATE incoming_certificate_of_analysis i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO manhattan_wms.supplier_cert
       (cert_nbr, business_partner_id, item_name, vendor_batch_nbr, cert_type, cert_date, conforming)
SELECT i.certificate_identifier, i.supplier_identifier, i.raw_material_code, i.lot_identifier, i.certificate_type,
       i.certificate_date, CASE WHEN i.certificate_conformity_flag THEN 'Y' ELSE 'N' END
  FROM incoming_certificate_of_analysis i
 WHERE i.discard_reason IS NULL
ON CONFLICT (cert_nbr) DO UPDATE SET
       business_partner_id = EXCLUDED.business_partner_id, item_name = EXCLUDED.item_name,
       vendor_batch_nbr = EXCLUDED.vendor_batch_nbr, cert_type = EXCLUDED.cert_type,
       cert_date = EXCLUDED.cert_date, conforming = EXCLUDED.conforming;

UPDATE incoming_certificate_test_result SET discard_reason = 'certificate test values not kept by the WMS';
