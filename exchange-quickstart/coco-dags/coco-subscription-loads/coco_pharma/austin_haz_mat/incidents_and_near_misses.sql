-- Subscription: coco_austin_haz_mat__incidents_and_near_misses - Austin HazMat Inventory (Coco core) receives Incidents And Near Misses
-- Destination: coco_pharma.austin_haz_mat (System::austin-haz-mat)
-- Why it subscribes: Occupational Exposure Bands depends on it (assessment feedback)
-- Keeps incidents and near misses involving a chemical held at the Austin site (chemical), with their
-- investigation findings, in ehs_incident (NEW), reviewed when a band is revised.  Discards incidents with no
-- chemical or with substances held elsewhere.  No system supplies this product yet.

UPDATE incoming_incident i SET discard_reason = 'no chemical held in Austin HazMat Inventory'
 WHERE i.substance_code IS NULL OR NOT EXISTS (SELECT 1 FROM austin_haz_mat.chemical c WHERE c.chem_id = i.substance_code);

INSERT INTO austin_haz_mat.ehs_incident (incident_no, incident_type, occurred_at, reported_at, site, area, chem_id, worker_psn,
       description, severity)
SELECT i.incident_identifier, i.incident_type, i.incident_timestamp, i.incident_reported_timestamp, i.site_code, i.incident_location,
       i.substance_code, i.worker_pseudonym_identifier, i.incident_description, i.incident_severity
  FROM incoming_incident i
 WHERE i.discard_reason IS NULL
ON CONFLICT (incident_no) DO UPDATE SET incident_type = EXCLUDED.incident_type, occurred_at = EXCLUDED.occurred_at,
       reported_at = EXCLUDED.reported_at, site = EXCLUDED.site, area = EXCLUDED.area, chem_id = EXCLUDED.chem_id,
       worker_psn = EXCLUDED.worker_psn, description = EXCLUDED.description, severity = EXCLUDED.severity;

UPDATE incoming_incident_investigation_finding f SET discard_reason = 'finding of an incident Austin HazMat Inventory does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM austin_haz_mat.ehs_incident i WHERE i.incident_no = f.incident_identifier);

UPDATE austin_haz_mat.ehs_incident i SET findings = f.findings
  FROM (SELECT incident_identifier,
               string_agg(incident_finding_number || '. ' || incident_finding_description
                          || coalesce(' Action: ' || incident_finding_action_description, ''), E'\n' ORDER BY incident_finding_number) AS findings
          FROM incoming_incident_investigation_finding
         WHERE discard_reason IS NULL
         GROUP BY incident_identifier) f
 WHERE f.incident_identifier = i.incident_no AND i.findings IS DISTINCT FROM f.findings;
