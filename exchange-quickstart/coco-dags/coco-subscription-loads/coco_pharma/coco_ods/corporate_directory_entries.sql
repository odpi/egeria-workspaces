-- Subscription: coco_ods__corporate_directory_entries - Coco Pharmaceuticals Operational Data Store (Coco core) receives Corporate Directory Entries
-- Destination: coco_pharma.coco_ods (System::coco-ods (not in the archive))
-- Why it subscribes: reporting: fills employees (names, titles, phones), units_by_location
-- Keeps Coco directory entries (CW- pseudonyms): each entry's department is added to units_by_location for its
-- site (department_number is not supplied), and where an existing employee has the same first and last name
-- their title, work phone and location are refreshed.  No employee is created - employees needs the HR employee
-- number, which the directory does not carry - and the manager is not set (reports_to cannot be derived from a
-- pseudonym).  Discards Austin and EKG directory entries, which are not Coco employees.

UPDATE incoming_directory_entry SET discard_reason = 'Austin or EKG worker - not a Coco employee'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';

UPDATE coco_ods.employees e
   SET title = left(d.role_name, 30), work_phone = left(d.person_work_phone_number, 20),
       location_code = (CASE d.site_code WHEN 'AMS' THEN 1 WHEN 'LON' THEN 2 WHEN 'NYC' THEN 3 WHEN 'AUS' THEN 5 WHEN 'WIN' THEN 6
                             WHEN 'KCY' THEN 7 WHEN 'EDM' THEN 8 ELSE e.location_code END)
  FROM incoming_directory_entry d
 WHERE d.discard_reason IS NULL
   AND lower(e.first_name) = lower(left(d.person_first_name, 10)) AND lower(e.last_name) = lower(left(d.person_last_name, 20))
   AND (e.title, e.work_phone, e.location_code) IS DISTINCT FROM
       (left(d.role_name, 30), left(d.person_work_phone_number, 20),
        (CASE d.site_code WHEN 'AMS' THEN 1 WHEN 'LON' THEN 2 WHEN 'NYC' THEN 3 WHEN 'AUS' THEN 5 WHEN 'WIN' THEN 6
                          WHEN 'KCY' THEN 7 WHEN 'EDM' THEN 8 ELSE e.location_code END));

INSERT INTO coco_ods.units_by_location (location_id, department_name)
SELECT DISTINCT l.location_id, left(d.department_name, 32)
  FROM incoming_directory_entry d
  JOIN coco_ods.coco_locations l
    ON l.location_id = (CASE d.site_code WHEN 'AMS' THEN 1 WHEN 'LON' THEN 2 WHEN 'NYC' THEN 3 WHEN 'AUS' THEN 5 WHEN 'WIN' THEN 6
                                         WHEN 'KCY' THEN 7 WHEN 'EDM' THEN 8 END)
 WHERE d.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM coco_ods.units_by_location u
                    WHERE u.location_id = l.location_id AND u.department_name = left(d.department_name, 32));
