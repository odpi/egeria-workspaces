-- Subscription: coco_kcdepot01__transport_classifications - Kansas City Depot Management System (Coco core) receives Transport Classifications
-- Destination: coco_pharma.kcdepot01 (System::KCDEPOT01)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (classification and requirements)
-- Keeps every transport classification - all come from Coco's two HazMat inventories, including the DOT
-- classification of Cisplatin (UN1851) that Kansas City ships - in hazmat_class (NEW, UN/NA number held as a
-- number as in hazmat_shipment).  Discards only classifications without a UN/NA number it can hold.

UPDATE incoming_transport_classification SET discard_reason = 'not a UN/NA numbered classification'
 WHERE transport_classification_code !~ '^(UN|NA)[0-9]{4}$';

INSERT INTO kcdepot01.hazmat_class (class_id, un_na_nbr, substance_cd, sku, shipped_form, packing_grp, hazard_class, label_text,
       shipping_papers, classified_dt)
SELECT t.transport_classification_identifier, substr(t.transport_classification_code, 3)::integer, t.substance_code,
       lower(t.product_code), t.substance_form_description, t.transport_classification_packing_group_code,
       t.transport_classification_hazard_class_code, t.transport_classification_labelling_description,
       t.transport_classification_documentation_description, t.transport_classification_date
  FROM incoming_transport_classification t
 WHERE t.discard_reason IS NULL
ON CONFLICT (class_id) DO UPDATE SET un_na_nbr = EXCLUDED.un_na_nbr, substance_cd = EXCLUDED.substance_cd, sku = EXCLUDED.sku,
       shipped_form = EXCLUDED.shipped_form, packing_grp = EXCLUDED.packing_grp, hazard_class = EXCLUDED.hazard_class,
       label_text = EXCLUDED.label_text, shipping_papers = EXCLUDED.shipping_papers, classified_dt = EXCLUDED.classified_dt;
