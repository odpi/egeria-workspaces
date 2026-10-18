-- Extract: Coco Pharmaceuticals Procurement (Coco core) -> Supplier Master Data / supplier_risk_status
-- Source: coco_pharma.procurement01 (System::procurement01)
-- Target: coco_data_hub.supplier_master_data.supplier_risk_status
-- latest completed vendor_screening per vendor, with any open vendor_anomaly.
WITH latest AS (
  SELECT DISTINCT ON (s.vendor_no) s.*
  FROM procurement01.vendor_screening s
  WHERE s.vendor_no IS NOT NULL AND s.result IS NOT NULL
  ORDER BY s.vendor_no, s.requested_ts DESC
)
SELECT
  l.vendor_no::varchar(40)       AS supplier_identifier,
  (CASE l.result WHEN 'CLEAR' THEN 'clear' WHEN 'REVIEW' THEN 'match under review' ELSE 'blocked' END)::varchar(20) AS supplier_screened_status,
  l.result_dt                    AS supplier_screened_date,
  (CASE l.risk_rating WHEN 'LOW' THEN 'low' WHEN 'MED' THEN 'medium' WHEN 'HIGH' THEN 'high' ELSE 'unrated' END)::varchar(20) AS supplier_rating,
  l.screen_ref::varchar(40)      AS screening_identifier,
  (SELECT max(a.anomaly_ref) FROM procurement01.vendor_anomaly a
    WHERE a.vendor_no = l.vendor_no AND a.anomaly_status = 'OPEN')::varchar(40) AS anomaly_identifier
FROM latest l
