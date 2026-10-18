-- Subscription: aus_sap_s4hana__supplier_master_data - SAP S/4HANA (Austin) receives Supplier Master Data
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Supplier Payments depends on it (supplier and payment details)
-- Keeps the Austin suppliers in the NEW standard vendor master tables LFA1 (lifnr = MDM/SAP vendor number padded to
-- 10, with the posting block and the screening result the payment proposal reads) and LFBK (the verified remittance
-- account). Coco and EKG suppliers are discarded.

UPDATE incoming_supplier i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO sap_s4hana.lfa1 (mandt, lifnr, name1, land1, ktokk, sperr, loevm, zz_approved_on)
SELECT '100', lpad(i.supplier_identifier, 10, '0'), left(i.supplier_name, 80), left(i.supplier_country, 3),
       CASE WHEN i.supplier_type = 'material supplier' THEN 'ZMAT' ELSE 'ZOTH' END,
       CASE WHEN i.supplier_approved_flag AND i.supplier_current_status = 'active' THEN '' ELSE 'X' END,
       CASE WHEN i.supplier_current_status = 'closed' THEN 'X' ELSE '' END,
       to_char(i.supplier_approved_date, 'YYYYMMDD')
  FROM incoming_supplier i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, lifnr) DO UPDATE SET
       name1 = EXCLUDED.name1, land1 = EXCLUDED.land1, ktokk = EXCLUDED.ktokk, sperr = EXCLUDED.sperr,
       loevm = EXCLUDED.loevm, zz_approved_on = EXCLUDED.zz_approved_on;

UPDATE incoming_supplier_risk_status i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.lfa1 l WHERE l.mandt = '100'
                      AND l.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE sap_s4hana.lfa1 l
   SET zz_spl_status = s.spl, zz_spl_date = s.dt, zz_risk_rating = s.rating, zz_screening_ref = s.ref,
       zz_anomaly_ref = s.anomaly
  FROM (SELECT lpad(i.supplier_identifier, 10, '0') AS lifnr,
               CASE i.supplier_screened_status WHEN 'clear' THEN 'C' WHEN 'blocked' THEN 'B' ELSE 'R' END AS spl,
               to_char(i.supplier_screened_date, 'YYYYMMDD') AS dt, upper(i.supplier_rating) AS rating,
               i.screening_identifier AS ref, i.anomaly_identifier AS anomaly
          FROM incoming_supplier_risk_status i WHERE i.discard_reason IS NULL) s
 WHERE l.mandt = '100' AND l.lifnr = s.lifnr
   AND (l.zz_spl_status, l.zz_spl_date, l.zz_risk_rating, l.zz_screening_ref, l.zz_anomaly_ref)
       IS DISTINCT FROM (s.spl, s.dt, s.rating, s.ref, s.anomaly);

UPDATE incoming_supplier_payment_details i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.lfa1 l WHERE l.mandt = '100'
                      AND l.lifnr = lpad(i.supplier_identifier, 10, '0'));
INSERT INTO sap_s4hana.lfbk (mandt, lifnr, banks, bvtyp, bankl, bankn, iban, zz_bank_name, zz_change_ref,
                             zz_verified_on)
SELECT '100', lpad(i.supplier_identifier, 10, '0'), left(i.bank_account_country, 3), '0001',
       CASE WHEN i.bank_account_current_identifier ~ '^[A-Z]{2}[0-9]{2}' THEN NULL
            ELSE nullif(split_part(i.bank_account_current_identifier, '-', 2), '') END,
       CASE WHEN i.bank_account_current_identifier ~ '^[A-Z]{2}[0-9]{2}' THEN NULL
            ELSE nullif(split_part(i.bank_account_current_identifier, '-', 3), '') END,
       CASE WHEN i.bank_account_current_identifier ~ '^[A-Z]{2}[0-9]{2}' THEN i.bank_account_current_identifier END,
       left(i.bank_account_provider_name, 60), i.payment_detail_change_identifier,
       to_char(i.payment_detail_verified_date, 'YYYYMMDD')
  FROM incoming_supplier_payment_details i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, lifnr, bvtyp) DO UPDATE SET
       banks = EXCLUDED.banks, bankl = EXCLUDED.bankl, bankn = EXCLUDED.bankn, iban = EXCLUDED.iban,
       zz_bank_name = EXCLUDED.zz_bank_name, zz_change_ref = EXCLUDED.zz_change_ref,
       zz_verified_on = EXCLUDED.zz_verified_on;
