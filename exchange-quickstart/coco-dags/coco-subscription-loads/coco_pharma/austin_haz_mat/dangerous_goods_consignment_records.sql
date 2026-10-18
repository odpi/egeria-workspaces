-- Subscription: coco_austin_haz_mat__dangerous_goods_consignment_records - Austin HazMat Inventory (Coco core) receives Dangerous Goods Consignment Records
-- Destination: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Why it subscribes: Hazardous Material Holdings depends on it (consignment record)
-- Keeps nothing: no consignment in the product leaves Coco-managed stock at the Austin site.  Coco's
-- consignments are despatched from its depots (reconciled by Coco HazMat Inventory); the SH- shipments are
-- Austin's own distribution of its share of stock, which is outside the manufacturing integration and covered
-- by Austin's own EHS systems; EXP- shipments are EKG's.

UPDATE incoming_consignment_declaration SET discard_reason = 'despatched from a Coco depot - reconciled by Coco HazMat Inventory'
 WHERE declaration_signatory_identifier LIKE 'CW-%';
UPDATE incoming_consignment_declaration SET discard_reason = 'EKG shipment - another estate'
 WHERE discard_reason IS NULL AND certificate_identifier LIKE '%EKG%';
UPDATE incoming_consignment_declaration SET discard_reason = 'Austin''s own distribution - not Coco-managed stock'
 WHERE discard_reason IS NULL;

UPDATE incoming_consignment_document SET discard_reason = 'consignment documents are kept by the shipper';
