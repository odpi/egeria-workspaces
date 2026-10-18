-- Subscription: buc_sap_s4hana__goods_receipts - SAP ERP S/4HANA (Bucharest) receives Goods Receipts
-- Destination: bucharest_systems.sap_s4hana (SoftwareServer::SYS-001::SAP ERP S/4HANA)
-- Why it subscribes: Material Quarantine Dispositions depends on it (place in quarantine)
-- Places an EKG goods receipt in quarantine the SAP way: a goods-receipt inspection lot (qals, origin 01, number 01 + the
-- material document, quantity converted from the WMS base unit to the unit of the material's earlier lots) is created
-- for a receipt of an EKG vendor that has none yet.  A lot without a usage decision is not read by the extracts.
-- Receipts that already have their inspection lot are discarded, as is the WMS's own receiving check; Coco and Austin
-- receipts are discarded (EKG is not yet integrated).
UPDATE incoming_goods_receipt i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE NOT EXISTS (SELECT 1 FROM sap_s4hana.lfa1 v WHERE v.mandt = '300' AND v.lifnr = lpad(i.supplier_identifier, 10, '0'));
UPDATE incoming_goods_receipt i SET discard_reason = 'inspection lot already exists for this receipt'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM sap_s4hana.qals q WHERE q.mandt = '300' AND q.art = '01'
                AND (q.ktextlos = 'Recepție ' || i.goods_receipt_identifier OR q.charg = i.lot_identifier));
UPDATE incoming_receipt_inspection r SET discard_reason = 'WMS receiving check - not an SAP QM record'
 WHERE EXISTS (SELECT 1 FROM incoming_goods_receipt g WHERE g.goods_receipt_identifier = r.goods_receipt_identifier
                AND (g.discard_reason IS NULL OR g.discard_reason <> 'Coco group data - EKG not yet integrated'));
UPDATE incoming_receipt_inspection SET discard_reason = 'Coco group data - EKG not yet integrated' WHERE discard_reason IS NULL;

WITH unit AS (
  SELECT DISTINCT ON (matnr) matnr, mengeneinh FROM sap_s4hana.qals WHERE mandt = '300' ORDER BY matnr, prueflos DESC
)
INSERT INTO sap_s4hana.qals (mandt, prueflos, werk, art, matnr, charg, lifnr, ebeln, enstehdat, entstezeit, losmenge,
                             mengeneinh, lmenge01, ktextlos)
SELECT '300', '01' || lpad(right(regexp_replace(i.goods_receipt_identifier, '[^0-9]', '', 'g'), 10), 10, '0'), 'RO10', '01',
       i.raw_material_code, left(i.lot_identifier, 10), lpad(i.supplier_identifier, 10, '0'), left(i.order_identifier, 10),
       to_char(i.goods_receipt_date, 'YYYYMMDD'), '000000',
       round(coalesce(i.goods_receipt_quantity, 0)::numeric / (CASE coalesce(u.mengeneinh, 'ST') WHEN 'KG' THEN 1000 WHEN 'G' THEN 1000 WHEN 'L' THEN 1000 ELSE 1 END), 3),
       coalesce(u.mengeneinh, 'ST'), NULL, left('Recepție ' || i.goods_receipt_identifier, 40)
  FROM incoming_goods_receipt i
  LEFT JOIN unit u ON u.matnr = i.raw_material_code
 WHERE i.discard_reason IS NULL AND i.raw_material_code IS NOT NULL AND i.lot_identifier IS NOT NULL
ON CONFLICT (mandt, prueflos) DO NOTHING;
