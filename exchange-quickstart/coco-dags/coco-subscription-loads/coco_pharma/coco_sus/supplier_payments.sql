-- Subscription: coco_sus__supplier_payments - Coco Pharmaceuticals Sustainability Data Marts (Coco core) receives Supplier Payments
-- Destination: coco_pharma.coco_sus (System::coco-sus)
-- Why it subscribes: reporting: fills ghg_emissions.power and transport (energy and fuel invoices)
-- Keeps nothing: ghg_emissions.power and transport hold emissions, which need metered consumption (kWh, litres)
-- and emission factors; the energy suppliers' (6000, 6001, 6002) and the fuel supplier's (4000) invoices carry
-- only amounts.  Other suppliers' invoices have no emissions meaning here, and Austin's and EKG's are outside
-- Coco's emissions reporting.

UPDATE incoming_invoice_match SET discard_reason = 'Austin or EKG supplier - outside Coco''s emissions reporting'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';
UPDATE incoming_invoice_match SET discard_reason = 'energy or fuel spend without metered consumption - emissions cannot be calculated'
 WHERE discard_reason IS NULL AND supplier_identifier IN ('4000', '6000', '6001', '6002');
UPDATE incoming_invoice_match SET discard_reason = 'not an energy or fuel supplier' WHERE discard_reason IS NULL;

UPDATE incoming_payment_instruction SET discard_reason = 'Austin or EKG supplier - outside Coco''s emissions reporting'
 WHERE supplier_identifier !~ '^[0-9]{1,5}$';
UPDATE incoming_payment_instruction SET discard_reason = 'energy or fuel spend without metered consumption - emissions cannot be calculated'
 WHERE discard_reason IS NULL AND supplier_identifier IN ('4000', '6000', '6001', '6002');
UPDATE incoming_payment_instruction SET discard_reason = 'not an energy or fuel supplier' WHERE discard_reason IS NULL;
