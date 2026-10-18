-- Subscription: buc_ekg_wms__transport_classifications - Warehouse Management System (WMS) (Bucharest) receives Transport Classifications
-- Destination: bucharest_systems.ekg_wms (SoftwareServer::SYS-019::Warehouse Management System (WMS))
-- Why it subscribes: Dangerous Goods Consignment Records depends on it (classification and requirements)
-- Keeps the ADR classification of EKG articles (product code known in articole) in the new table clasificari_adr (UN
-- number, packing group, class, labels and documents), used to prepare dangerous goods despatches.  Today only Coco
-- and Austin products are classified in the product, and they are discarded (EKG is not yet integrated); EKG's dry-ice
-- UN number is still keyed on the despatch.
UPDATE incoming_transport_classification i SET discard_reason = 'Coco group data - EKG not yet integrated'
 WHERE i.product_code IS NULL OR NOT EXISTS (SELECT 1 FROM ekg_wms.articole a WHERE a.cod_art = i.product_code);

INSERT INTO ekg_wms.clasificari_adr (id_clasif, cod_art, nr_onu, grupa_amb, clasa, etichetare, documente, data_clasif)
SELECT i.transport_classification_identifier, i.product_code, coalesce(i.transport_classification_code, '-'),
       i.transport_classification_packing_group_code, i.transport_classification_hazard_class_code,
       i.transport_classification_labelling_description, i.transport_classification_documentation_description,
       i.transport_classification_date
  FROM incoming_transport_classification i
 WHERE i.discard_reason IS NULL
ON CONFLICT (id_clasif) DO UPDATE
   SET cod_art = EXCLUDED.cod_art, nr_onu = EXCLUDED.nr_onu, grupa_amb = EXCLUDED.grupa_amb, clasa = EXCLUDED.clasa,
       etichetare = EXCLUDED.etichetare, documente = EXCLUDED.documente, data_clasif = EXCLUDED.data_clasif;
