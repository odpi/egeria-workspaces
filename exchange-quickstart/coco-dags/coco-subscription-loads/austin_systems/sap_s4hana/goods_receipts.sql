-- Subscription: aus_sap_s4hana__goods_receipts - SAP S/4HANA (Austin) receives Goods Receipts
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Material Quarantine Dispositions depends on it (place in quarantine)
-- Keeps Austin warehouse receipts SAP has not yet posted as goods movements staged for BAPI_GOODSMVT_CREATE (NEW
-- BAPI2017_GM_HEAD_01 / BAPI2017_GM_ITEM_CREATE: movement 101 into quality inspection stock, which creates the
-- inspection lot). Receipts already posted (an inspection lot exists for the material and batch), receiving
-- inspections (WMS business), Coco's Austin Inventory receipts and EKG receipts are discarded.

UPDATE incoming_goods_receipt i SET discard_reason = 'other estate: not an Austin (Manhattan) warehouse'
 WHERE i.warehouse_code NOT IN ('AUS1', 'AUS2');
UPDATE incoming_goods_receipt i SET discard_reason = 'already held: goods receipt posted (inspection lot exists)'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.qals q WHERE q.mandt = '100' AND q.matnr = i.raw_material_code
                  AND q.charg = i.lot_identifier);
INSERT INTO sap_s4hana.bapi2017_gm_head_01 (mandt, ref_doc_no, gm_code, pstng_date, doc_date, header_txt, zz_status)
SELECT '100', i.goods_receipt_identifier, '01', to_char(i.goods_receipt_date, 'YYYYMMDD'),
       to_char(i.goods_receipt_date, 'YYYYMMDD'), left('WMS receipt ' || i.goods_receipt_identifier, 25), 'R'
  FROM incoming_goods_receipt i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, ref_doc_no) DO UPDATE SET
       gm_code = EXCLUDED.gm_code, pstng_date = EXCLUDED.pstng_date, doc_date = EXCLUDED.doc_date,
       header_txt = EXCLUDED.header_txt;
INSERT INTO sap_s4hana.bapi2017_gm_item_create
       (mandt, ref_doc_no, line_id, material, plant, stge_loc, batch, move_type, stck_type, entry_qnt, po_number,
        vendor, zz_cert_no)
SELECT '100', i.goods_receipt_identifier, '000001', i.raw_material_code, 'US10', i.warehouse_code,
       i.lot_identifier, '101', 'Q', i.goods_receipt_quantity, i.order_identifier,
       lpad(i.supplier_identifier, 10, '0'), i.certificate_identifier
  FROM incoming_goods_receipt i
 WHERE i.discard_reason IS NULL
ON CONFLICT (mandt, ref_doc_no, line_id) DO UPDATE SET
       material = EXCLUDED.material, plant = EXCLUDED.plant, stge_loc = EXCLUDED.stge_loc, batch = EXCLUDED.batch,
       move_type = EXCLUDED.move_type, stck_type = EXCLUDED.stck_type, entry_qnt = EXCLUDED.entry_qnt,
       po_number = EXCLUDED.po_number, vendor = EXCLUDED.vendor, zz_cert_no = EXCLUDED.zz_cert_no;

UPDATE incoming_receipt_inspection SET discard_reason = 'receiving inspection is held in the WMS';
