-- Subscription: aus_informatica_mdm__market_authorisations - Informatica MDM (Austin) receives Market Authorisations
-- Destination: austin_systems.informatica_mdm (SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301)
-- Why it subscribes: Product Master Data depends on it (authorised markets)
-- Keeps the marketing authorisations of products made at Austin in the C_L_PRODUCT_MKT_AUTH landing table for the
-- stage job to merge into the product's authorised markets. Today every authorisation is EKG's (Veeva RIM, PF-
-- products) and is discarded; authorisation conditions are not mastered in MDM.

UPDATE incoming_market_authorisation i SET discard_reason = 'other estate: product not made at Austin'
 WHERE NOT (i.product_code LIKE 'AU-%' OR i.product_code IN ('3000', '2050', '9000'));
INSERT INTO informatica_mdm.c_l_product_mkt_auth
       (rowid_system, pkey_src_object, product_cd, market_cd, authorisation_no, regulator_cd, start_dt, end_dt,
        status_cd)
SELECT 'DATA_HUB', i.authorisation_identifier, i.product_code, i.market_code, i.authorisation_identifier,
       i.authorisation_regulator_code, i.authorisation_start_date, i.authorisation_end_date,
       upper(i.authorisation_current_status)
  FROM incoming_market_authorisation i
 WHERE i.discard_reason IS NULL
ON CONFLICT (rowid_system, pkey_src_object) DO UPDATE SET
       product_cd = EXCLUDED.product_cd, market_cd = EXCLUDED.market_cd,
       authorisation_no = EXCLUDED.authorisation_no, regulator_cd = EXCLUDED.regulator_cd,
       start_dt = EXCLUDED.start_dt, end_dt = EXCLUDED.end_dt, status_cd = EXCLUDED.status_cd;

UPDATE incoming_authorisation_condition SET discard_reason = 'authorisation conditions not mastered in MDM';
