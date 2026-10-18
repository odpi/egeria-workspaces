-- Subscription: aus_ukg_dimensions__worker_master_data - UKG Dimensions (Austin) receives Worker Master Data
-- Destination: austin_systems.ukg_dimensions (SoftwareServer::AUS-SYS-021::SN-TNA-AU-20190305)
-- Why it subscribes: Payroll Results depends on it (payroll record)
-- Keeps the employment status and home labour account of the Austin hourly workers it already has timecards for
-- (person, matched on the Workday employee ID behind the pseudonym). Salaried Austin staff have no UKG person and
-- are discarded, as are Coco and EKG workers. pay_statement, which feeds Payroll Results, is untouched.

UPDATE incoming_worker i SET discard_reason = 'other estate: not an Austin (US01) worker'
 WHERE i.legal_entity_code IS DISTINCT FROM 'US01';
UPDATE incoming_worker i SET discard_reason = 'no UKG timecard: not an hourly plant worker'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM ukg_dimensions.person p WHERE 'WP-' || upper(substr(md5('AUS:' || p.person_number), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE ukg_dimensions.person p
   SET employment_status = s.status,
       employment_status_date = CASE WHEN s.status = 'Terminated' THEN coalesce(s.leave_date, p.employment_status_date)
                                     ELSE p.employment_status_date END
  FROM (SELECT i.worker_pseudonym_identifier AS pseudonym, i.worker_leave_date AS leave_date,
               CASE i.worker_current_status WHEN 'left' THEN 'Terminated' WHEN 'on leave' THEN 'Inactive'
                    ELSE 'Active' END AS status
          FROM incoming_worker i WHERE i.discard_reason IS NULL) s
 WHERE 'WP-' || upper(substr(md5('AUS:' || p.person_number), 1, 12)) = s.pseudonym
   AND (p.employment_status IS DISTINCT FROM s.status
        OR (s.status = 'Terminated' AND p.employment_status_date IS DISTINCT FROM coalesce(s.leave_date, p.employment_status_date)));

UPDATE incoming_worker_assignment i SET discard_reason = 'no UKG timecard: not an Austin hourly plant worker'
 WHERE NOT EXISTS (SELECT 1 FROM ukg_dimensions.person p WHERE 'WP-' || upper(substr(md5('AUS:' || p.person_number), 1, 12)) = i.worker_pseudonym_identifier);

UPDATE ukg_dimensions.person p
   SET home_labor_account = split_part(p.home_labor_account, '/', 1) || '/' || i.cost_centre_code || '/' || i.role_code
  FROM incoming_worker_assignment i
 WHERE i.discard_reason IS NULL AND 'WP-' || upper(substr(md5('AUS:' || p.person_number), 1, 12)) = i.worker_pseudonym_identifier
   AND p.home_labor_account IS DISTINCT FROM split_part(p.home_labor_account, '/', 1) || '/' || i.cost_centre_code || '/' || i.role_code;
