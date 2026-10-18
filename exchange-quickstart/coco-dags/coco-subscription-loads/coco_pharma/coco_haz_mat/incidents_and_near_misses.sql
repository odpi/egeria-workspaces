-- Subscription: coco_haz_mat__incidents_and_near_misses - Coco HazMat Inventory (Coco core) receives Incidents And Near Misses
-- Destination: coco_pharma.coco_haz_mat (System::coco-haz-mat)
-- Why it subscribes: Occupational Exposure Bands depends on it (assessment feedback)
-- Keeps incidents and near misses involving a substance this inventory holds (hm_subst), with their investigation
-- findings, in hm_incid (NEW), reviewed when the substance's exposure band is reassessed.  Discards incidents
-- with no substance or with substances held elsewhere.  No system supplies this product yet.

UPDATE incoming_incident i SET discard_reason = 'no substance held in Coco HazMat Inventory'
 WHERE i.substance_code IS NULL OR NOT EXISTS (SELECT 1 FROM coco_haz_mat.hm_subst s WHERE s.subst_cd = i.substance_code);

INSERT INTO coco_haz_mat.hm_incid (inc_ref, inc_typ, inc_ts, rpt_ts, site_cd, inc_loc, subst_cd, worker_ref, inc_desc, sev)
SELECT i.incident_identifier, i.incident_type, i.incident_timestamp, i.incident_reported_timestamp, i.site_code, i.incident_location,
       i.substance_code, i.worker_pseudonym_identifier, i.incident_description, i.incident_severity
  FROM incoming_incident i
 WHERE i.discard_reason IS NULL
ON CONFLICT (inc_ref) DO UPDATE SET inc_typ = EXCLUDED.inc_typ, inc_ts = EXCLUDED.inc_ts, rpt_ts = EXCLUDED.rpt_ts,
       site_cd = EXCLUDED.site_cd, inc_loc = EXCLUDED.inc_loc, subst_cd = EXCLUDED.subst_cd, worker_ref = EXCLUDED.worker_ref,
       inc_desc = EXCLUDED.inc_desc, sev = EXCLUDED.sev;

UPDATE incoming_incident_investigation_finding f SET discard_reason = 'finding of an incident Coco HazMat Inventory does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_haz_mat.hm_incid i WHERE i.inc_ref = f.incident_identifier);

UPDATE coco_haz_mat.hm_incid i SET findings = f.findings
  FROM (SELECT incident_identifier,
               string_agg(incident_finding_number || '. ' || incident_finding_description
                          || coalesce(' Action: ' || incident_finding_action_description, ''), E'\n' ORDER BY incident_finding_number) AS findings
          FROM incoming_incident_investigation_finding
         WHERE discard_reason IS NULL
         GROUP BY incident_identifier) f
 WHERE f.incident_identifier = i.inc_ref AND i.findings IS DISTINCT FROM f.findings;
