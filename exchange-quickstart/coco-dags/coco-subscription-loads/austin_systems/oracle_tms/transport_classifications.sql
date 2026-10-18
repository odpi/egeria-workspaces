-- Subscription: aus_oracle_tms__transport_classifications - Oracle TMS (Austin) receives Transport Classifications
-- Destination: austin_systems.oracle_tms (SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (classification and requirements)
-- Keeps the classifications from Coco's Austin HazMat Inventory (DOT-A-), which covers the substances held at the
-- Austin site and Cisplatin 9000 made there - treated as part of the manufacturing integration. The Coco sites'
-- classifications (TC-C-) are discarded. They go to the NEW hazmat_item table that shipment building reads.

UPDATE incoming_transport_classification i SET discard_reason = 'other estate: Coco site classification'
 WHERE i.transport_classification_identifier NOT LIKE 'DOT-A-%';
INSERT INTO oracle_tms.hazmat_item
       (hazmat_item_gid, substance_code, product_code, item_description, un_number, packing_group, hazard_class,
        labels, documentation, effective_date)
SELECT 'AUS.' || i.transport_classification_identifier, i.substance_code, i.product_code,
       i.substance_form_description, i.transport_classification_code, i.transport_classification_packing_group_code,
       i.transport_classification_hazard_class_code, i.transport_classification_labelling_description,
       i.transport_classification_documentation_description, i.transport_classification_date
  FROM incoming_transport_classification i
 WHERE i.discard_reason IS NULL
ON CONFLICT (hazmat_item_gid) DO UPDATE SET
       substance_code = EXCLUDED.substance_code, product_code = EXCLUDED.product_code,
       item_description = EXCLUDED.item_description, un_number = EXCLUDED.un_number,
       packing_group = EXCLUDED.packing_group, hazard_class = EXCLUDED.hazard_class, labels = EXCLUDED.labels,
       documentation = EXCLUDED.documentation, effective_date = EXCLUDED.effective_date;
