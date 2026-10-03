-- Extract: SAP S/4HANA (Austin) -> Supplier Payments / payment_instruction
-- Source: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Target: coco_data_hub.supplier_payments.payment_instruction
-- Payment run items (reguh/regup) released in BCM (bnk_batch_header); payee bank as IBAN or country-bank-account; SPL
-- status C/R/B translated; cost coding is the G/L line of the paid invoice document.
SELECT
  h.vblnr::varchar(40) AS payment_identifier,
  ltrim(h.lifnr, '0')::varchar(40) AS supplier_identifier,
  p.xblnr::varchar(40) AS invoice_number,
  p.dmbtr::numeric(18,2) AS payment_amount,
  h.waers::varchar(3) AS payment_currency_code,
  lower(b.chusr)::varchar(40) AS payment_authoriser_identifier,
  ((to_date(b.chdate, 'YYYYMMDD') + b.chtime::time) AT TIME ZONE 'UTC') AS payment_authorised_timestamp,
  (CASE h.zz_spl_status WHEN 'C' THEN 'clear' WHEN 'R' THEN 'match under review' ELSE 'blocked' END)::varchar(20) AS supplier_screened_status,
  coalesce(nullif(h.ziban, ''), h.zbnks || '-' || h.zbnky || '-' || h.zbnkn)::varchar(40) AS bank_account_current_identifier,
  ltrim(c.racct, '0')::varchar(20) AS ledger_account_code
FROM sap_s4hana.reguh h
JOIN sap_s4hana.regup p ON p.mandt = h.mandt AND p.laufd = h.laufd AND p.laufi = h.laufi AND p.xvorl = h.xvorl
                       AND p.zbukr = h.zbukr AND p.lifnr = h.lifnr AND p.vblnr = h.vblnr
JOIN sap_s4hana.bnk_batch_header b ON b.mandt = h.mandt AND b.laufd = h.laufd AND b.laufi = h.laufi AND b.zbukr = h.zbukr
JOIN sap_s4hana.acdoca c ON c.rclnt = p.mandt AND c.rbukrs = p.bukrs AND c.gjahr = p.gjahr AND c.belnr = p.belnr
                        AND c.rldnr = '0L' AND c.koart = 'S'
WHERE h.mandt = '100' AND h.xvorl = '' AND b.status = 'IBC11'
