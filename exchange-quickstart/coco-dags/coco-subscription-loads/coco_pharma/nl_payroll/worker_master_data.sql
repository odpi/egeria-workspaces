-- Subscription: coco_nl_payroll__worker_master_data - Netherlands payroll (Coco core) receives Worker Master Data
-- Destination: coco_pharma.nl_payroll (System::NL payroll)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Keeps the employees of Coco Pharmaceuticals B.V. (COCO-NL): every record goes to the HR mutaties table
-- hr_mutatie (NEW), and medewerkers already on the payroll (matched on the HRIM pseudonym) get their
-- kostenplaats and datum_uit_dienst refreshed.  Discards other Coco legal entities (their own payrolls),
-- contractors and Austin/EKG workers.

UPDATE incoming_worker SET discard_reason = 'Austin or EKG worker - not on a Coco payroll'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_worker SET discard_reason = 'not employed by Coco Pharmaceuticals B.V. - paid by the ' || legal_entity_code || ' payroll'
 WHERE discard_reason IS NULL AND legal_entity_code <> 'COCO-NL';
UPDATE incoming_worker SET discard_reason = 'contractor - not paid through payroll'
 WHERE discard_reason IS NULL AND worker_type <> 'employee';

INSERT INTO nl_payroll.hr_mutatie (worker_ref, werkgever, vestiging, datum_in_dienst, datum_uit_dienst, dienstverband_status)
SELECT w.worker_pseudonym_identifier, w.legal_entity_code, w.site_code, w.worker_hire_date, w.worker_leave_date,
       (CASE w.worker_current_status WHEN 'active' THEN 'actief' WHEN 'left' THEN 'uit dienst' WHEN 'on leave' THEN 'verlof'
             ELSE w.worker_current_status END)
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL
ON CONFLICT (worker_ref) DO UPDATE SET werkgever = EXCLUDED.werkgever, vestiging = EXCLUDED.vestiging,
       datum_in_dienst = EXCLUDED.datum_in_dienst, datum_uit_dienst = EXCLUDED.datum_uit_dienst,
       dienstverband_status = EXCLUDED.dienstverband_status;

UPDATE nl_payroll.medewerker m SET datum_uit_dienst = w.worker_leave_date
  FROM incoming_worker w
 WHERE w.discard_reason IS NULL AND w.worker_pseudonym_identifier = m.worker_ref
   AND m.datum_uit_dienst IS DISTINCT FROM w.worker_leave_date;

UPDATE incoming_worker_assignment a SET discard_reason = 'worker not on the Dutch payroll'
 WHERE NOT EXISTS (SELECT 1 FROM nl_payroll.hr_mutatie f WHERE f.worker_ref = a.worker_pseudonym_identifier);

UPDATE nl_payroll.hr_mutatie f
   SET functie_code = a.role_code, functie_naam = a.role_name, kostenplaats = a.cost_centre_code,
       leidinggevende_ref = a.manager_pseudonym_identifier
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = f.worker_ref;

UPDATE nl_payroll.medewerker m SET kostenplaats = a.cost_centre_code
  FROM incoming_worker_assignment a
 WHERE a.discard_reason IS NULL AND a.worker_pseudonym_identifier = m.worker_ref
   AND m.kostenplaats IS DISTINCT FROM a.cost_centre_code;
