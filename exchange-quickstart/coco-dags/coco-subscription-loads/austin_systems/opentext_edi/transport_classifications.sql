-- Subscription: aus_opentext_edi__transport_classifications - OpenText Trading Grid EDI (Austin) receives Transport Classifications
-- Destination: austin_systems.opentext_edi (SoftwareServer::AUS-SYS-015::SN-EDI-AU-20190620)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (classification and requirements)
-- Keeps the classifications from Coco's Austin HazMat Inventory (DOT-A-), which covers the substances held at the
-- Austin site and Cisplatin 9000 made there - treated as part of the manufacturing integration. The Coco sites'
-- classifications (TC-C-) are discarded. They go to the NEW tg_xref_dg_class cross-reference used to map the IFTDGN
-- dangerous goods segments.

UPDATE incoming_transport_classification i SET discard_reason = 'other estate: Coco site classification'
 WHERE i.transport_classification_identifier NOT LIKE 'DOT-A-%';
INSERT INTO opentext_edi.tg_xref_dg_class
       (xref_key, substance_ref, product_ref, un_number, hazard_class, packing_group, label_text, document_text,
        effective_date)
SELECT i.transport_classification_identifier, i.substance_code, i.product_code, i.transport_classification_code,
       i.transport_classification_hazard_class_code, i.transport_classification_packing_group_code,
       i.transport_classification_labelling_description, i.transport_classification_documentation_description,
       i.transport_classification_date
  FROM incoming_transport_classification i
 WHERE i.discard_reason IS NULL
ON CONFLICT (xref_key) DO UPDATE SET
       substance_ref = EXCLUDED.substance_ref, product_ref = EXCLUDED.product_ref, un_number = EXCLUDED.un_number,
       hazard_class = EXCLUDED.hazard_class, packing_group = EXCLUDED.packing_group,
       label_text = EXCLUDED.label_text, document_text = EXCLUDED.document_text,
       effective_date = EXCLUDED.effective_date;
