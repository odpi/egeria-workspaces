-- Subscription: aus_sap_s4hana__purchase_orders_and_receipts - SAP S/4HANA (Austin) receives Purchase Orders And Receipts
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Supplier Payments depends on it (order and receipt)
-- Keeps purchase orders with Austin suppliers staged for BAPI_PO_CREATE1 (NEW BAPIMEPOHEADER) and their receipt
-- confirmations staged for BAPI_GOODSMVT_CREATE (BAPI2017_GM_HEAD_01 / BAPI2017_GM_ITEM_CREATE, movement 101 against
-- the order), so invoices can be matched three ways. Orders with other estates' suppliers and receipts for orders it
-- does not hold are discarded.

UPDATE incoming_purchase_order i SET discard_reason = 'other estate: not an Austin supplier'
 WHERE i.supplier_identifier !~ '^10[0-9]{4}$';
INSERT INTO sap_s4hana.bapimepoheader
       (mandt, po_number, comp_code, doc_type, vendor, doc_date, currency, zz_total_amount, zz_approver, zz_status)
SELECT '100', i.order_identifier, 'US01', 'NB', lpad(i.supplier_identifier, 10, '0'),
       to_char(i.order_date, 'YYYYMMDD'), i.order_currency_code, i.order_total_amount,
       left(upper(i.order_approver_identifier), 12), upper(i.order_current_status)
  FROM incoming_purchase_order i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, po_number) DO UPDATE SET
       vendor = EXCLUDED.vendor, doc_date = EXCLUDED.doc_date, currency = EXCLUDED.currency,
       zz_total_amount = EXCLUDED.zz_total_amount, zz_approver = EXCLUDED.zz_approver, zz_status = EXCLUDED.zz_status;

UPDATE incoming_goods_receipt_confirmation i SET discard_reason = 'order not held (other estate)'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.bapimepoheader h WHERE h.mandt = '100' AND h.po_number = i.order_identifier);
INSERT INTO sap_s4hana.bapi2017_gm_head_01 (mandt, ref_doc_no, gm_code, pstng_date, doc_date, header_txt, zz_status)
SELECT DISTINCT ON (i.goods_receipt_identifier) '100', i.goods_receipt_identifier, '01',
       to_char(i.goods_receipt_date, 'YYYYMMDD'), to_char(i.goods_receipt_date, 'YYYYMMDD'),
       left('Receipt ' || i.goods_receipt_identifier, 25), 'R'
  FROM incoming_goods_receipt_confirmation i
 WHERE i.discard_reason IS NULL
 ORDER BY i.goods_receipt_identifier, i.goods_receipt_date
ON CONFLICT (mandt, ref_doc_no) DO UPDATE SET
       pstng_date = EXCLUDED.pstng_date, doc_date = EXCLUDED.doc_date, header_txt = EXCLUDED.header_txt;
INSERT INTO sap_s4hana.bapi2017_gm_item_create
       (mandt, ref_doc_no, line_id, plant, move_type, stck_type, entry_qnt, po_number, po_item, vendor)
SELECT '100', i.goods_receipt_identifier, lpad(i.line_item_number::text, 6, '0'), 'US10', '101', 'Q',
       i.goods_receipt_quantity, i.order_identifier, lpad(i.line_item_number::text, 5, '0'), h.vendor
  FROM incoming_goods_receipt_confirmation i
  JOIN sap_s4hana.bapimepoheader h ON h.mandt = '100' AND h.po_number = i.order_identifier
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, ref_doc_no, line_id) DO UPDATE SET
       entry_qnt = EXCLUDED.entry_qnt, po_number = EXCLUDED.po_number, po_item = EXCLUDED.po_item,
       vendor = EXCLUDED.vendor;
