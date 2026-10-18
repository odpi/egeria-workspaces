-- Extract: SAP ERP S/4HANA (Bucharest) -> Supplier Payments / payment_instruction
-- Source: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Target: coco_data_hub.supplier_payments.payment_instruction
-- Payment run items (reguh/regup) released in BCM (bnk_batch_header); payee bank as IBAN or country-bank-account;
-- screening status C/R/B translated; cost coding is the first G/L line of the paid invoice document.
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
JOIN LATERAL (SELECT a.racct FROM sap_s4hana.acdoca a
              WHERE a.rclnt = p.mandt AND a.rbukrs = p.bukrs AND a.gjahr = p.gjahr AND a.belnr = p.belnr
                AND a.rldnr = '0L' AND a.koart = 'S' ORDER BY a.docln LIMIT 1) c ON true
WHERE h.mandt = '300' AND h.xvorl = '' AND b.status = 'IBC11'
