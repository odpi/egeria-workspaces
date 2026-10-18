-- Subscription: coco_ods__goods_receipts - Coco Pharmaceuticals Operational Data Store (Coco core) receives Goods Receipts
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills supplier_invoice_details (delivery dates and quantities received)
-- Keeps nothing: supplier_invoice_details rows need an invoice number, line number and item amount (all NOT
-- NULL), and a goods receipt carries none of them - it names the order, not the invoice, and receipts cannot be
-- matched to invoice lines without the order lines no product supplies.  Austin's and EKG's receipts are not
-- Coco's anyway.

UPDATE incoming_goods_receipt SET discard_reason = 'Austin or EKG receipt - not Coco''s'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$' OR warehouse_code IN ('AUS1', 'AUS2');
UPDATE incoming_goods_receipt SET discard_reason = 'supplier_invoice_details needs the invoice number, line and amount, which a receipt does not carry'
 WHERE discard_reason IS NULL;
UPDATE incoming_receipt_inspection SET discard_reason = 'the ODS holds no receipt inspections';
