-- Subscription: coco_winchdepot01__transport_classifications - Winchester Depot Management System (Coco core) receives Transport Classifications
-- Destination: coco_pharma.winchdepot01 (System::WINCHDEPOT01)
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (classification and requirements)
-- Keeps every transport classification - all come from Coco's two HazMat inventories, including Cocolecel
-- (UN3245) that Winchester despatches - in dg_class (NEW), used to prepare the dangerous goods declaration and
-- pack.  Nothing is discarded: the classifications are Coco-wide reference data.

INSERT INTO winchdepot01.dg_class (class_ref, un_no, subst_cd, prd_cd, form_desc, pkg_grp, haz_cls, lbl_desc, docs_desc, class_dt)
SELECT t.transport_classification_identifier, t.transport_classification_code, t.substance_code, t.product_code,
       t.substance_form_description, t.transport_classification_packing_group_code, t.transport_classification_hazard_class_code,
       t.transport_classification_labelling_description, t.transport_classification_documentation_description,
       t.transport_classification_date
  FROM incoming_transport_classification t
 WHERE t.discard_reason IS NULL
ON CONFLICT (class_ref) DO UPDATE SET un_no = EXCLUDED.un_no, subst_cd = EXCLUDED.subst_cd, prd_cd = EXCLUDED.prd_cd,
       form_desc = EXCLUDED.form_desc, pkg_grp = EXCLUDED.pkg_grp, haz_cls = EXCLUDED.haz_cls, lbl_desc = EXCLUDED.lbl_desc,
       docs_desc = EXCLUDED.docs_desc, class_dt = EXCLUDED.class_dt;
