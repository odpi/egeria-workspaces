-- Subscription: aus_informatica_mdm__third_party_onboarding_cases - Informatica MDM (Austin) receives Third Party Onboarding Cases
-- Destination: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Why it subscribes: Supplier Master Data depends on it (create supplier record)
-- Keeps approved Austin onboarding cases (SAP Ariba supplier requests) whose supplier it does not yet master in the
-- C_L_PARTY landing table, and the screenings of those cases in C_L_PARTY_SCREENING, so the stage job creates the
-- golden supplier. Cases still in progress or rejected, cases whose supplier is already mastered (SAP_S4 cross
-- reference) and Coco's onboarding cases (OB-) are discarded.

UPDATE incoming_onboarding_case i SET discard_reason = 'other estate: not an Austin (Ariba) request'
 WHERE i.onboarding_case_identifier NOT LIKE 'SR-%';
UPDATE incoming_onboarding_case i SET discard_reason = 'onboarding not approved'
 WHERE i.discard_reason IS NULL AND i.onboarding_case_current_status <> 'approved';
UPDATE incoming_onboarding_case i SET discard_reason = 'already held: supplier mastered'
 WHERE i.discard_reason IS NULL
   AND EXISTS (SELECT 1 FROM informatica_mdm.c_b_party_xref x
                WHERE x.rowid_system = 'SAP_S4' AND x.pkey_src_object = i.supplier_identifier);
INSERT INTO informatica_mdm.c_l_party
       (rowid_system, pkey_src_object, org_nm, country_cd, owner_desc, requester_txt, request_dt, status_cd,
        sap_vendor_no)
SELECT 'DATA_HUB', i.onboarding_case_identifier, i.third_party_name, left(i.third_party_country, 2),
       i.third_party_owner_description, i.onboarding_case_requester_identifier, i.onboarding_case_start_date,
       upper(i.onboarding_case_current_status), i.supplier_identifier
  FROM incoming_onboarding_case i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       org_nm = EXCLUDED.org_nm, country_cd = EXCLUDED.country_cd, owner_desc = EXCLUDED.owner_desc,
       requester_txt = EXCLUDED.requester_txt, request_dt = EXCLUDED.request_dt, status_cd = EXCLUDED.status_cd,
       sap_vendor_no = EXCLUDED.sap_vendor_no;

UPDATE incoming_screening_request i SET discard_reason = 'other estate: not an Austin (Ariba) request'
 WHERE i.onboarding_case_identifier NOT LIKE 'SR-%';
UPDATE incoming_screening_request i SET discard_reason = 'case not landed (not approved or supplier mastered)'
 WHERE i.discard_reason IS NULL
   AND NOT EXISTS (SELECT 1 FROM informatica_mdm.c_l_party l
                    WHERE l.rowid_system = 'DATA_HUB' AND l.pkey_src_object = i.onboarding_case_identifier);
INSERT INTO informatica_mdm.c_l_party_screening
       (rowid_system, pkey_src_object, party_src_key, screen_status_cd, screened_dt, risk_rating_cd, screening_ref,
        anomaly_ref, notes_txt)
SELECT 'DATA_HUB', i.screening_identifier, i.onboarding_case_identifier, 'REQ', i.screening_requested_timestamp::date,
       upper(i.supplier_rating), i.screening_identifier, NULL, i.screening_type
  FROM incoming_screening_request i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       party_src_key = EXCLUDED.party_src_key, screened_dt = EXCLUDED.screened_dt,
       risk_rating_cd = EXCLUDED.risk_rating_cd, screening_ref = EXCLUDED.screening_ref,
       notes_txt = EXCLUDED.notes_txt;
