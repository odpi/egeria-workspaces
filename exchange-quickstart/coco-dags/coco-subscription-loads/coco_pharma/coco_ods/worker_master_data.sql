-- Subscription: coco_ods__worker_master_data - Coco Pharmaceuticals Operational Data Store (Coco core) receives Worker Master Data
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills employees (employment details)
-- Keeps nothing: coco_ods.employees is keyed by the HR employee number, and Worker Master Data identifies workers
-- only by pseudonym, by design - mapping pseudonyms back to employee numbers stays with HR and is not in any
-- product.  Hire and leave dates, status, site and cost centre therefore cannot be attached to an employee.
-- Austin and EKG workers are not Coco employees anyway.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - not a Coco employee'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker SET discard_reason = 'pseudonymised worker - cannot be mapped to an employees.employee_id'
 WHERE discard_reason IS NULL;
UPDATE incoming_worker_assignment SET discard_reason = 'Austin or EKG worker - not a Coco employee'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker_assignment SET discard_reason = 'pseudonymised worker - cannot be mapped to an employees.employee_id'
 WHERE discard_reason IS NULL;
