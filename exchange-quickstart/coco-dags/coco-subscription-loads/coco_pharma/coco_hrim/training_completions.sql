-- Subscription: coco_hrim__training_completions - Human Resources Information Manager (HRIM) (Coco core) receives Training Completions
-- Destination: coco_pharma.coco_hrim (System::coco-hrim)
-- Why it subscribes: Worker Qualifications depends on it (completion and assessment)
-- Keeps completions and assessment results for Coco workers (CW- pseudonyms) in lms_completion (NEW), from which
-- the skills administrator records competencies in emp_competency (not written directly: it feeds Worker
-- Qualifications).  Discards Austin/EKG workers' training (their own LMS and HR), and refresher schedules,
-- because HRIM plans refreshers itself from competency.refresh_mths.

UPDATE incoming_training_completion SET discard_reason = 'Austin or EKG worker - training is recorded in the acquired estate''s own systems'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';

INSERT INTO coco_hrim.lms_completion (completion_ref, worker_ref, course_cd, comp_cd, completed_dt, expiry_dt)
SELECT c.training_completion_identifier, c.worker_pseudonym_identifier, c.training_course_code, c.competency_code,
       c.training_completed_date, c.training_expiry_date
  FROM incoming_training_completion c
 WHERE c.discard_reason IS NULL
ON CONFLICT (completion_ref) DO UPDATE SET worker_ref = EXCLUDED.worker_ref, course_cd = EXCLUDED.course_cd,
       comp_cd = EXCLUDED.comp_cd, completed_dt = EXCLUDED.completed_dt, expiry_dt = EXCLUDED.expiry_dt;

UPDATE incoming_assessment_result r SET discard_reason = 'assessment for a training completion HRIM does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_hrim.lms_completion c WHERE c.completion_ref = r.training_completion_identifier);

-- The latest assessment of each completion is kept.
UPDATE coco_hrim.lms_completion c
   SET assess_dt = r.training_assessment_date, assess_score = r.training_assessment_value,
       pass_mark = r.training_assessment_minimum_value, passed_yn = (CASE WHEN r.training_assessment_passed_flag THEN 'Y' ELSE 'N' END)
  FROM (SELECT DISTINCT ON (training_completion_identifier) *
          FROM incoming_assessment_result
         WHERE discard_reason IS NULL
         ORDER BY training_completion_identifier, training_assessment_date DESC) r
 WHERE r.training_completion_identifier = c.completion_ref
   AND (c.assess_dt IS NULL OR c.assess_dt <= r.training_assessment_date);

UPDATE incoming_refresher_schedule SET discard_reason = 'Austin or EKG worker - training is recorded in the acquired estate''s own systems'
 WHERE worker_pseudonym_identifier NOT LIKE 'CW-%';
UPDATE incoming_refresher_schedule SET discard_reason = 'HRIM schedules refreshers itself from the competency refresh period'
 WHERE discard_reason IS NULL;
