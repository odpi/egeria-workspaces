-- Subscription: aus_cornerstone_lms__role_competency_requirements - Cornerstone OnDemand LMS (Austin) receives Role Competency Requirements
-- Destination: austin_systems.cornerstone_lms (SoftwareServer::AUS-SYS-020::SN-LMS-AU-20200110)
-- Why it subscribes: Training Completions depends on it (required competencies)
-- Keeps nothing: Cornerstone is the only Austin source of this product, so the Austin requirements (position OU and
-- competency already in ou_competency_requirement) are its own, and the Coco HRIM role codes (CLN-, DEP-, MFG-...)
-- are not Austin positions. All rows are discarded.

UPDATE incoming_role_competency_requirement i SET discard_reason = 'already held: supplied by Cornerstone'
 WHERE EXISTS (SELECT 1 FROM cornerstone_lms.ou_competency_requirement r
                WHERE r.ou_id = i.role_code AND r.competency_id = i.competency_code);
UPDATE incoming_role_competency_requirement i SET discard_reason = 'other estate: not an Austin position'
 WHERE i.discard_reason IS NULL;
