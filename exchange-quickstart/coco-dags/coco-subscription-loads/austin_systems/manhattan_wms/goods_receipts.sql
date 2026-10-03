-- Subscription: aus_manhattan_wms__goods_receipts - Manhattan WMS (Austin) receives Goods Receipts
-- Destination: austin_systems.manhattan_wms (SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315)
-- Why it subscribes: Material Quarantine Dispositions depends on it (place in quarantine)
-- Keeps nothing: Manhattan is the Austin source of Goods Receipts, so the AUS1/AUS2 receipts and inspections are its
-- own ASNs coming back. The other rows are Coco's (depot systems and Coco's Austin Inventory, AUS-RCV-) or EKG's and
-- are discarded.

UPDATE incoming_goods_receipt i SET discard_reason = 'already held: supplied by Manhattan (ASN)'
 WHERE EXISTS (SELECT 1 FROM manhattan_wms.asn a WHERE a.tc_asn_id = i.goods_receipt_identifier);
UPDATE incoming_goods_receipt SET discard_reason = 'other estate: not an Austin warehouse receipt'
 WHERE discard_reason IS NULL;

UPDATE incoming_receipt_inspection i SET discard_reason = 'already held: supplied by Manhattan (QC inspection)'
 WHERE EXISTS (SELECT 1 FROM manhattan_wms.asn a WHERE a.tc_asn_id = i.goods_receipt_identifier);
UPDATE incoming_receipt_inspection SET discard_reason = 'other estate: not an Austin warehouse receipt'
 WHERE discard_reason IS NULL;
