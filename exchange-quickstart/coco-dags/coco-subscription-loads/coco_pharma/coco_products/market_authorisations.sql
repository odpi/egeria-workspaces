-- Subscription: coco_products__market_authorisations - Coco Product Management (Coco core) receives Market Authorisations
-- Destination: coco_pharma.coco_products (System::cocoProducts)
-- Why it subscribes: Product Master Data depends on it (authorised markets)
-- Keeps authorisations of Coco products (product code in prd_mstr) and their conditions in prd_ma_rcvd and
-- prd_ma_cond (both NEW, market GB written as UK), from which the product manager maintains prd_mkt_auth -
-- not written directly because it feeds Product Master Data.  Discards authorisations of products Coco does
-- not define: today all rows are EKG's own Romanian and regional authorisations (PF- products).

UPDATE incoming_market_authorisation a SET discard_reason = 'not a Coco product - authorisation held by the acquired estate that markets it'
 WHERE NOT EXISTS (SELECT 1 FROM coco_products.prd_mstr p WHERE p.prd_cd = a.product_code);

INSERT INTO coco_products.prd_ma_rcvd (ma_no, prd_cd, mkt, rgltr_cd, start_dt, end_dt, ma_sts, sgnl_ref)
SELECT a.authorisation_identifier, a.product_code, (CASE a.market_code WHEN 'GB' THEN 'UK' ELSE a.market_code END),
       a.authorisation_regulator_code, a.authorisation_start_date, a.authorisation_end_date,
       upper(a.authorisation_current_status), a.signal_identifier
  FROM incoming_market_authorisation a
 WHERE a.discard_reason IS NULL
ON CONFLICT (ma_no) DO UPDATE SET prd_cd = EXCLUDED.prd_cd, mkt = EXCLUDED.mkt, rgltr_cd = EXCLUDED.rgltr_cd,
       start_dt = EXCLUDED.start_dt, end_dt = EXCLUDED.end_dt, ma_sts = EXCLUDED.ma_sts, sgnl_ref = EXCLUDED.sgnl_ref;

UPDATE incoming_authorisation_condition c SET discard_reason = 'condition of an authorisation Coco Product Management does not keep'
 WHERE NOT EXISTS (SELECT 1 FROM coco_products.prd_ma_rcvd r WHERE r.ma_no = c.authorisation_identifier);

INSERT INTO coco_products.prd_ma_cond (ma_no, cond_no, cond_typ, cond_txt, start_dt)
SELECT c.authorisation_identifier, c.authorisation_requirement_number, c.authorisation_requirement_type,
       c.authorisation_requirement_description, c.authorisation_requirement_start_date
  FROM incoming_authorisation_condition c
 WHERE c.discard_reason IS NULL
ON CONFLICT (ma_no, cond_no) DO UPDATE SET cond_typ = EXCLUDED.cond_typ, cond_txt = EXCLUDED.cond_txt, start_dt = EXCLUDED.start_dt;
