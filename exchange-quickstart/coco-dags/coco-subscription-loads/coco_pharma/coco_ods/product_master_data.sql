-- Subscription: coco_ods__product_master_data - Coco Pharmaceuticals Operational Data Store (Coco core) receives Product Master Data
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills products, categories
-- Keeps Coco products (four-digit codes) in products: name, strength as unit_dosage (where it fits ten
-- characters), discontinued from the status, and the smallest pack size as quantity_per_unit (stock figures held
-- are rescaled to it); new products are added without supplier or category.  categories is not touched: the
-- master's product_type is not the ODS's therapeutic category.  Discards Austin's own products (AU- codes),
-- handling requirements and market authorisations, which the ODS does not hold.

UPDATE incoming_product_definition SET discard_reason = 'Austin product - not in Coco''s product range'
 WHERE product_code !~ '^[0-9]{1,4}$';

INSERT INTO coco_ods.products (product_id, product_name, discontinued, unit_dosage)
SELECT d.product_code::smallint, left(d.product_name, 40),
       (CASE WHEN d.product_current_status IN ('withdrawn', 'discontinued') THEN 1 ELSE 0 END),
       (CASE WHEN length(replace(d.product_strength, ' ', '')) <= 10 THEN replace(d.product_strength, ' ', '') END)
  FROM incoming_product_definition d
 WHERE d.discard_reason IS NULL
ON CONFLICT (product_id) DO UPDATE SET product_name = EXCLUDED.product_name, discontinued = EXCLUDED.discontinued,
       unit_dosage = coalesce(EXCLUDED.unit_dosage, coco_ods.products.unit_dosage);

UPDATE incoming_pack_configuration p SET discard_reason = 'pack of a product not in the ODS'
 WHERE p.product_code !~ '^[0-9]{1,4}$'
    OR NOT EXISTS (SELECT 1 FROM coco_ods.products o WHERE o.product_id::text = p.product_code);

-- A new pack size changes the sales unit, so the stock figures already held are rescaled to it.
UPDATE coco_ods.products o
   SET quantity_per_unit = k.qpu,
       units_in_stock = (CASE WHEN o.units_in_stock IS NOT NULL THEN
                          least(round(o.units_in_stock * coalesce(nullif(substring(o.quantity_per_unit FROM '^[0-9]+'), '')::numeric, 1)
                                      / k.qpu::numeric), 32767) END),
       reorder_level = (CASE WHEN o.reorder_level IS NOT NULL THEN
                         least(round(o.reorder_level * coalesce(nullif(substring(o.quantity_per_unit FROM '^[0-9]+'), '')::numeric, 1)
                                     / k.qpu::numeric), 32767) END)
  FROM (SELECT product_code::smallint AS product_id, min(pack_quantity)::text AS qpu
          FROM incoming_pack_configuration WHERE discard_reason IS NULL GROUP BY product_code) k
 WHERE k.product_id = o.product_id AND o.quantity_per_unit IS DISTINCT FROM k.qpu;

UPDATE incoming_handling_requirement SET discard_reason = 'the ODS holds no storage or handling conditions';
UPDATE incoming_authorised_market_assignment SET discard_reason = 'the ODS holds no market authorisations';
