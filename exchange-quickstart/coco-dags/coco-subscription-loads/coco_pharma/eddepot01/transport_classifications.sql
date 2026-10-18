-- Subscription: coco_eddepot01__transport_classifications - Edmonton Depot Management System (Coco core) receives Transport Classifications
-- Destination: coco_pharma.eddepot01 (System::EDDEPOT01)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (classification and requirements)
-- Keeps every transport classification - all come from Coco's two HazMat inventories - in tdg_class (NEW), used
-- to prepare TDG shipping documents for whatever Coco substance or product the depot ships.  Nothing is
-- discarded: the classifications are Coco-wide reference data.

INSERT INTO eddepot01.tdg_class (class_id, un_number, substance, item, shipped_form, packing_group, tdg_class, labels, documents,
       classified_on)
SELECT t.transport_classification_identifier, t.transport_classification_code, t.substance_code, t.product_code,
       t.substance_form_description, t.transport_classification_packing_group_code, t.transport_classification_hazard_class_code,
       t.transport_classification_labelling_description, t.transport_classification_documentation_description,
       t.transport_classification_date
  FROM incoming_transport_classification t
 WHERE t.discard_reason IS NULL
ON CONFLICT (class_id) DO UPDATE SET un_number = EXCLUDED.un_number, substance = EXCLUDED.substance, item = EXCLUDED.item,
       shipped_form = EXCLUDED.shipped_form, packing_group = EXCLUDED.packing_group, tdg_class = EXCLUDED.tdg_class,
       labels = EXCLUDED.labels, documents = EXCLUDED.documents, classified_on = EXCLUDED.classified_on;
