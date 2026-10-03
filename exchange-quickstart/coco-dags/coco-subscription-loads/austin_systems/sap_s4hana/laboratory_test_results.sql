-- Subscription: aus_sap_s4hana__laboratory_test_results - SAP S/4HANA (Austin) receives Laboratory Test Results
-- Destination: austin_systems.sap_s4hana (SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923)
-- Why it subscribes: Material Quarantine Dispositions depends on it (test results)
-- Keeps the LIMS results for Austin raw material lots that have a goods receipt inspection lot (QALS, matched on
-- batch), staged for BAPI_INSPOPER_RECORDRESULTS in the NEW BAPI2045D2 table (one row per lot and test, with the
-- LIMS result number the usage decision already cites). Samples and certificates (held in LIMS), finished-product
-- results (no SAP inspection lot; they go to the batch record) and EKG results are discarded.

UPDATE incoming_sample i SET discard_reason = 'other estate: not an Austin sample'
 WHERE coalesce(i.batch_identifier, i.lot_identifier, '') !~ '^(RM|A)[0-9]{2}-';
UPDATE incoming_sample SET discard_reason = 'samples are held in LIMS' WHERE discard_reason IS NULL;

UPDATE incoming_test_result i SET discard_reason = 'other estate: not an Austin sample'
 WHERE i.sample_identifier !~ '^S[0-9]{2}-0[0-9]{5}$';
UPDATE incoming_test_result i SET discard_reason = 'no SAP inspection lot for this sample'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM incoming_sample s
                     JOIN sap_s4hana.qals q ON q.mandt = '100' AND q.art = '01' AND q.charg = s.lot_identifier
                    WHERE s.sample_identifier = i.sample_identifier);
INSERT INTO sap_s4hana.bapi2045d2
       (mandt, insplot, inspoper, inspchar, mean_value, meas_unit, evaluation, zz_spec_min, zz_spec_max,
        zz_tested_at, inspector, zz_lims_result)
SELECT DISTINCT ON (q.prueflos, i.test_code) '100', q.prueflos, '0010', i.test_code, i.test_value, i.test_unit,
       CASE WHEN i.test_conformity_flag THEN 'A' ELSE 'R' END, i.specification_minimum_value,
       i.specification_maximum_value, i.test_completed_timestamp, left(upper(i.test_analyst_identifier), 12),
       i.test_result_identifier
  FROM incoming_test_result i
  JOIN incoming_sample s ON s.sample_identifier = i.sample_identifier
  JOIN sap_s4hana.qals q ON q.mandt = '100' AND q.art = '01' AND q.charg = s.lot_identifier
 WHERE i.discard_reason IS NULL
 ORDER BY q.prueflos, i.test_code, i.test_completed_timestamp DESC, i.test_result_identifier
ON CONFLICT (mandt, insplot, inspoper, inspchar) DO UPDATE SET
       mean_value = EXCLUDED.mean_value, meas_unit = EXCLUDED.meas_unit, evaluation = EXCLUDED.evaluation,
       zz_spec_min = EXCLUDED.zz_spec_min, zz_spec_max = EXCLUDED.zz_spec_max, zz_tested_at = EXCLUDED.zz_tested_at,
       inspector = EXCLUDED.inspector, zz_lims_result = EXCLUDED.zz_lims_result;

UPDATE incoming_certificate_of_analysis SET discard_reason = 'certificates of analysis are held in LIMS';
